# @frozen
# class GWASSummaryStatsFileTask(RemoteFileTask):
#     """
#     A task that fetches GWAS summary statistics from a remote server.
#     """
#
#     url: str
#     md5: str | None
#     _meta: GWASSummaryDataFileMeta
#
#     @property
#     def meta(self) -> GWASSummaryDataFileMeta:
#         return self._meta
#
#     @property
#     def deps(self) -> list[Task]:
#         return []
#
#     def execute(self, scratch_dir: WritablePath, fetch: Fetch, wf: WF) -> FileAsset:
#         local_target = scratch_dir / "target"
#         wf.download_from_url(
#             url=self.url,
#             md5_hash=self.md5,
#             local_path=local_target,
#         )
#         return FileAsset(
#             path=local_target,
#         )
