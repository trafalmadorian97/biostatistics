import pandas as pd
from pandasgwas import Study


def filter_by_full_pvalue(studies: list[Study]):
    return [study for study in studies if (study.studies["fullPvalueSet"].all())]


def check_singletons(studies: list[Study]):
    for study in studies:
        assert len(study.studies) == 1


def summarize_studies(studies: list[Study]) -> pd.DataFrame:
    pass
    # data = [
    #     {} item for item in studies
    # ]
