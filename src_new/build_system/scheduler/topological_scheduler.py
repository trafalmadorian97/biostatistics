from typing import Mapping

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.rebuilder.base_rebuilder import Rebuilder
from src_new.build_system.tasks.base_tasks import Tasks
from src_new.build_system.wf.base_wf import WF


def topological[
    Info,
](
    rebuilder: Rebuilder[Info], tasks: Tasks, target: Meta, wf: WF, info: Info
) -> tuple[Mapping[Meta, Asset], Info]:
    pass
