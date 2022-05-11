from typing import List, Optional
from pandas import DataFrame
from src.utilities import SavAdapter
from pyreadstat._readstat_parser import metadata_container


def get_job_title_generalized(
    job_title: int, prefix: Optional[int], depth: Optional[int]
) -> int:
    str_value = str(job_title)

    jobs_range = depth + len(str(prefix)) if prefix else depth
    if jobs_range > len(str_value):
        return int(str_value)
    else:
        return int(str_value[:jobs_range])


def get_competencies_list() -> List[str]:
    competencies_keys = ["k0" + str(i) for i in range(1, 10)]
    competencies_keys.extend(["k" + str(i) for i in range(10, 25)])

    return competencies_keys


def get_job_title_to_competencies(
    df: DataFrame,
    df_meta: metadata_container,
    prefix: Optional[int],
    depth: Optional[int],
) -> DataFrame:
    df = df.dropna(subset=["e10_isco"], axis=0)

    if prefix:
        employees_with_specialization_mask = [
            str(x).startswith(str(prefix)) for x in df["e10_isco"]
        ]
        df = df[employees_with_specialization_mask]

    df = df.assign(
        e10_isco_generalized=df["e10_isco"].apply(
            lambda x: get_job_title_generalized(int(x), prefix, depth)
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
