from abc import ABC, abstractmethod

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.rebuilder.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


class Rebuilder[Info](ABC):
    """
    Key Operations:
    - Decide whether a given asset is up-to-date using information from Info.
    - If the asset is up-to-date, return it together with the Info
    - If the asset is not up-to-date, bring it up-to-date, update Info, and return the new values of both
    """

    @abstractmethod
    def rebuild[A: Asset](
        self, task: Task[A], asset: A | None, fetch: Fetch, wf: WF, info: Info
    ) -> tuple[A, Info]:
        pass
