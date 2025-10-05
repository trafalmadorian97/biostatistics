from pandasgwas import get_studies

from src.data_pull_scripts.data_exploration_other_conditions.utils import (
    check_singletons,
    filter_by_full_pvalue,
)

"""
See: https://www.ebi.ac.uk/gwas/rest/docs/api
"""


def find():
    studies = get_studies(efo_trait="schizophrenia")
    print(f"yo. Found {len(studies)} studies total")
    filtered = filter_by_full_pvalue(studies)
    print(f"After filtering, found {len(filtered)} studies")
    check_singletons(filtered)


if __name__ == "__main__":
    find()
