from pathlib import Path
from typing import Any

import attr
import yaml
from attrs import define, field

from src_new.build_system.meta.meta import Meta
from src_new.build_system.serialization.converter import CONVERTER_FOR_SERIALIZATION

TraceRecord = tuple[str, list[tuple[Meta, str]]]


@define
class VerifyingTraceInfo:
    """
    Stores persistent data relevant to the verifying trace rebuilder
    Note that this is mutable
    trace_store: A map associating metadata objects with:
       - The traces of their corresponding assets
       -  A list of the metadata of the dependencies of these assets, together with the traces of these dependencies
    trace_store is used to decide when an asset needs to be regenerated.  An asset is regenerated
    when its trace, or the traces of its dependencies have changed
    """

    trace_store: dict[Meta, TraceRecord]
    must_rebuild: set[Meta] = field(factory=set)

    @classmethod
    def empty(cls) -> "VerifyingTraceInfo":
        return cls(
            trace_store={},
            must_rebuild=set(),
        )

    def serialize(self, path: Path) -> None:
        to_unstruc = attr.evolve(self, must_rebuild=set())
        conv = CONVERTER_FOR_SERIALIZATION
        unstructured = [
            (
                conv.unstructure(key, unstructure_as=Meta),
                _unstructure_trace_record(value),
            )
            for key, value in to_unstruc.trace_store.items()
        ]
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as outfile:
            yaml.dump(unstructured, outfile, default_flow_style=False)

    @classmethod
    def deserialize(cls, path: Path) -> "VerifyingTraceInfo":
        conv = CONVERTER_FOR_SERIALIZATION
        with open(path) as infile:
            unstructured = yaml.load(infile, Loader=yaml.FullLoader)

        trace_store: Any = {}
        for key, value in unstructured:
            key_recovered: Any = conv.structure(key, cl=Meta)  # type: ignore
            value_recovered: Any = conv.structure(value, cl=TraceRecord)  # type: ignore
            trace_store[key_recovered] = value_recovered

        return cls(trace_store=trace_store, must_rebuild=set())


def _unstructure_trace_record(item: TraceRecord) -> tuple[str, list[tuple[dict, str]]]:
    conv = CONVERTER_FOR_SERIALIZATION
    return item[0], [
        (conv.unstructure(record[0], unstructure_as=Meta), record[1])
        for record in item[1]
    ]


def update_verifying_trace_info_in_place(
    verifying_trace_info: VerifyingTraceInfo,
    meta: Meta,
    new_value_trace: str,
    deps_traced: list[tuple[Meta, str]],
) -> None:
    new_rebuild_set = set(verifying_trace_info.must_rebuild) - {meta}
    new_trace_store = dict(verifying_trace_info.trace_store)
    new_trace_store[meta] = new_value_trace, deps_traced
    verifying_trace_info.must_rebuild = new_rebuild_set
    verifying_trace_info.trace_store = new_trace_store
