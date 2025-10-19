from typing import Mapping, Sequence, cast

import emoji
import networkx as nx
from loguru import logger

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.rebuilder.base_rebuilder import Rebuilder
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.rebuilder.metadata_to_path.base_meta_to_path import MetaToPath
from src_new.build_system.scheduler.asset_retrieval import get_asset_if_exists
from src_new.build_system.tasks.base_tasks import Tasks
from src_new.build_system.wf.base_wf import WF


def dependency_graph(tasks: Tasks, targets: Sequence[Meta]) -> nx.DiGraph:
    G: nx.DiGraph = nx.DiGraph()
    for meta, task in tasks.items():
        for dep in task.deps:
            G.add_edge(dep.meta, meta)
    reachable = set(targets)
    for target in targets:
        reachable = nx.ancestors(G, target) | reachable
    subgraph = nx.DiGraph(G.subgraph(reachable))
    return subgraph


def get_next_node(
    graph: nx.DiGraph,
) -> Meta:
    generations = nx.topological_generations(graph)
    list_of_generations = [sorted(gen) for gen in generations]
    return list_of_generations[0][0]


def _get_progress_list(todo: Sequence[Meta], done: set[Meta]) -> str:
    s = "\nWork Progress:\n"
    for meta in todo:
        if meta in done:
            s += f"{meta.short_name} {emoji.emojize(':check_mark_button:')}\n"
        else:
            s += f"{meta.short_name}\n"
    return s


def topological[
    Info,
](
    rebuilder: Rebuilder[Info],
    tasks: Tasks,
    targets: Sequence[Meta],
    wf: WF,
    info: Info,
    meta_to_path: MetaToPath,
) -> tuple[Mapping[Meta, Asset], Info]:
    """
    Based on
    Mokhov, Andrey, Neil Mitchell, and Simon Peyton Jones.
    "Build systems à la carte: Theory and practice." Journal of Functional Programming 30 (2020): e11.
    +
    OpenAI
    """
    G = dependency_graph(tasks, targets)
    todo = list(nx.topological_sort(G))
    done: set[Meta] = set()
    store: dict[Meta, Asset] = {}
    while len(G) > 0:
        logger.info(_get_progress_list(todo=todo, done=done))
        node = get_next_node(G)
        task = tasks[node]
        maybe_asset = get_asset_if_exists(
            meta=node,
            meta_to_path=meta_to_path,
        )

        class SimpleFetch(Fetch):
            def __call__[A: Asset](self, m: Meta[A]) -> A:
                return cast(A, store[m])

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
