from cattrs import GenConverter
from cattrs.strategies import configure_tagged_union

import src_new.build_system.meta.gwas_summary_file_meta  # noqa
import src_new.build_system.meta.simple_directory_meta  # noqa
import src_new.build_system.meta.simple_file_meta  # noqa
from src_new.build_system.meta.AnyMeta import AnyMeta

# CONVERTER_FOR_SERIALIZATION = GenConverter(unstruct_strat=cattrs.UnstructureStrategy.AS_TUPLE)
CONVERTER_FOR_SERIALIZATION = GenConverter()
configure_tagged_union(AnyMeta, converter=CONVERTER_FOR_SERIALIZATION)
