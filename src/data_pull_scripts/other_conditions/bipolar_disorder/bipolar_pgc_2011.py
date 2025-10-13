from pathlib import Path, PurePath

from src.data_preprocessing_scripts.file_path_constants import DATA_DEFAULT_ROOT
from src.data_pull_util.data_source import (
    BasicDataSource,
    URLDataRetriever,
    ZipGZipDataExtractor,
)
from src.data_pull_util.data_verifier import FileSizeInDirVerifier

BIPOLAR_PGC_2011_GWAS_RAW_DIR = Path(
    "data/other_conditions/Bipolar_Disorder/PGS_2011/raw"
)
BIPOLAR_PGC_2011_GWAS_RAW_PATH = BIPOLAR_PGC_2011_GWAS_RAW_DIR / "14671995.zip"
"""
https://pubmed.ncbi.nlm.nih.gov/21926972/
Abstract:
We conducted a combined genome-wide association study (GWAS) of 7,481 individuals with bipolar disorder (cases) and 9,250 controls as part of the Psychiatric GWAS Consortium. 
Our replication study tested 34 SNPs in 4,496 independent cases with bipolar disorder and 42,422 independent controls and found that 18 of 34 SNPs had P < 0.05, with 31 of 34 SNPs having signals with the same direction of effect (P = 3.8 × 10(-7)). 
An analysis of all 11,974 bipolar disorder cases and 51,792 controls confirmed genome-wide significant evidence of association 
for CACNA1C and identified a new intronic variant in ODZ4. We identified a pathway comprised of subunits of calcium channels enriched in bipolar disorder association intervals. Finally, a combined GWAS analysis of
 schizophrenia and bipolar disorder yielded strong association evidence for SNPs in CACNA1C and in the region of NEK4-ITIH1-ITIH3-ITIH4. Our replication results imply that increasing sample sizes in bipolar disorder will confirm many additional loci.


"""

BIPOLAR_PGC_2011_DATA_SOURCE = BasicDataSource(
    retriever=URLDataRetriever(
        url="https://figshare.com/ndownloader/articles/14671995/versions/1",
        expected_size=50060674,
    ),
    extractor=ZipGZipDataExtractor(verifier=FileSizeInDirVerifier(".txt", 149848243)),
    path_extension=PurePath("other_conditions/Bipolar_Disorder/PGC_2011"),
    raw_filename="14671995.zip",
    extracted_filename="14671995",
)

if __name__ == "__main__":
    BIPOLAR_PGC_2011_DATA_SOURCE.extracted_path(DATA_DEFAULT_ROOT)
    # print(result)
