from cattrs import GenConverter
from cattrs.strategies import configure_tagged_union

from src_new.build_system.meta.meta import Meta

CONVERTER_FOR_SERIALIZATION = GenConverter()
configure_tagged_union(Meta, converter=CONVERTER_FOR_SERIALIZATION)
