from pandasgwas import get_studies


def find():
    studies = get_studies(efo_trait="triple-negative breast cancer")
    print(studies.studies[0:4])


if __name__ == "__main__":
    find()
