from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task


@frozen
class RestrictedFetch(Fetch):
    """
    A Fetch the prevents the retrieval of assets except those on a given list.
    Used to ensure the declared dependencies of a task are accurate.
    """

    inner: Fetch
    meta_deps: frozenset[Meta]

    def __call__[A: Asset](self, m: Meta[A]) -> A:
        if m not in self.meta_deps:
            raise ValueError(
                f"Attempted to fetch asset {m}, but only assets {self.meta_deps} are declared as dependencies."
            )
        return self.inner(m)

    @classmethod
    def from_task(cls, fetch: Fetch, task: Task):
        return cls(fetch, frozenset({dep.meta for dep in task.deps}))
