from typing import Mapping, Sequence

import emoji
import networkx as nx
import structlog
from loguru import logger

logger = structlog.get_logger()

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.rebuilder.base_rebuilder import Rebuilder
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.rebuilder.metadata_to_path.base_meta_to_path import MetaToPath
from src_new.build_system.scheduler.asset_retrieval import get_asset_if_exists
from src_new.build_system.tasks.base_tasks import Tasks
from src_new.build_system.wf.base_wf import WF


def dependency_graph(tasks: Tasks, targets: Sequence[AssetId]) -> nx.DiGraph:
    G: nx.DiGraph = nx.DiGraph()
    for asset_id, task in tasks.items():
        G.add_node(asset_id)
        for dep in task.deps:
            G.add_edge(dep.asset_id, asset_id)
    reachable = set(targets)
    for target in targets:
        reachable = nx.ancestors(G, target) | reachable
    subgraph = nx.DiGraph(G.subgraph(reachable))
    return subgraph


def get_next_node(
    graph: nx.DiGraph,
) -> AssetId:
    generations = nx.topological_generations(graph)
    list_of_generations = [sorted(gen) for gen in generations]
    return list_of_generations[0][0]


def _get_progress_list(todo: Sequence[AssetId], done: set[AssetId]) -> str:
    s = "\nWork Progress:\n"
    for asset_id in todo:
        if asset_id in done:
            s += f"{asset_id} {emoji.emojize(':check_mark_button:')}\n"
        else:
            s += f"{asset_id}\n"
    return s


def topological[
    Info,
](
    rebuilder: Rebuilder[Info],
    tasks: Tasks,
    targets: Sequence[AssetId],
    wf: WF,
    info: Info,
    meta_to_path: MetaToPath,
) -> tuple[Mapping[AssetId, Asset], Info]:
    """
    A scheduler that builds a dependency graph of tasks, and executes them in topological order.
    Based on
    Mokhov, Andrey, Neil Mitchell, and Simon Peyton Jones.
    "Build systems à la carte: Theory and practice." Journal of Functional Programming 30 (2020): e11.
    """
    G = dependency_graph(tasks, targets)
    todo: list[AssetId] = list(nx.topological_sort(G))
    done: set[AssetId] = set()
    store: dict[AssetId, Asset] = {}

    while len(G) > 0:
        logger.info(_get_progress_list(todo=todo, done=done))
        node = get_next_node(G)
        task = tasks[node]
        maybe_asset = get_asset_if_exists(
            meta=task.meta,
            meta_to_path=meta_to_path,
        )

        class SimpleFetch(Fetch):
            def __call__(self, asset_id: AssetId) -> Asset:
                return store[asset_id]

        new_asset, info = rebuilder.rebuild(
            task=task,
            asset=maybe_asset,
            fetch=SimpleFetch(),
            wf=wf,
            info=info,
            meta_to_path=meta_to_path,
        )
        store[node] = new_asset
        G.remove_node(node)
        done.add(node)
    logger.info(_get_progress_list(todo=todo, done=done))
    return store, info
