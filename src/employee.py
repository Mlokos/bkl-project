from typing import List, Optional
from pandas import DataFrame
from src.utilities import SavAdapter
from pyreadstat._readstat_parser import metadata_container


def get_job_title_generalized(
    job_title: float, generalization: int, specialization: Optional[int]
) -> float:
    str_value = str(job_title)

    jobs_range = (
        generalization + len(str(specialization)) if specialization else generalization
    )
    return float(str_value[:jobs_range])


def get_competencies_list() -> List[str]:
    competencies_keys = ["k0" + str(i) for i in range(1, 10)]
    competencies_keys.extend(["k" + str(i) for i in range(10, 25)])

    return competencies_keys


def get_job_title_to_competencies(
    df: DataFrame,
    df_meta: metadata_container,
    generalization: int,
    specialization: Optional[int],
) -> DataFrame:
    df = df.dropna(subset=["e10_isco"], axis=0)

    if specialization:
        employees_with_specialization_mask = [
            str(x).startswith(str(specialization)) for x in df["e10_isco"]
        ]
        df = df[employees_with_specialization_mask]

    df = df.assign(
        e10_isco_generalized=df["e10_isco"].apply(
            lambda x: get_job_title_generalized(x, generalization, specialization)
        )
    )
    df = df.groupby("e10_isco_generalized").mean()
    df = df.reset_index()

    sad = SavAdapter(metadata=df_meta)
    df = df.assign(
        e10_isco_name=df["e10_isco_generalized"].apply(
            lambda x: sad.get_value_name("e10_isco", x)
        )
    )

    employees_to_competencies = df[["e10_isco_name", *get_competencies_list()]]
    employees_to_competencies = employees_to_competencies.set_index("e10_isco_name")

    return employees_to_competencies
