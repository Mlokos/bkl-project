from typing import List, Optional
from pandas import DataFrame
from src.utilities import SavAdapter
from pyreadstat._readstat_parser import metadata_container
import matplotlib.pyplot as plt


def get_job_title_generalized(
    job_title: int, prefix: Optional[int], depth: Optional[int]
) -> int:
    str_value = str(job_title)

    jobs_range = depth + len(str(prefix)) if prefix else depth
    if jobs_range > len(str_value):
        return int(str_value)
    else:
        return int(str_value[:jobs_range])


def generalize_competencies(
    job_title_column_name: str,
    df: DataFrame,
    df_meta: metadata_container,
    prefix: Optional[int],
    depth: Optional[int],
) -> DataFrame:
    df = df.dropna(subset=[job_title_column_name], axis=0)

    if prefix:
        job_title_with_specialization_mask = [
            str(x).startswith(str(prefix)) for x in df[job_title_column_name]
        ]
        df = df[job_title_with_specialization_mask]

    df = df.assign(
        job_title_generalized=df[job_title_column_name].apply(
            lambda x: get_job_title_generalized(int(x), prefix, depth)
        )
    )
    df = df.groupby("job_title_generalized").mean()
    df = df.reset_index()

    sad = SavAdapter(metadata=df_meta)
    df = df.assign(
        e10_isco_name=df["job_title_generalized"].apply(
            lambda isco_code: "{} ({})".format(sad.get_value_name("e10_isco", isco_code), isco_code)
        )
    )

    return df


def get_competencies_list_employee() -> List[str]:
    competencies_keys = ["k0" + str(i) for i in range(1, 10)]
    competencies_keys.extend(["k" + str(i) for i in range(10, 25)])

    return competencies_keys


def get_job_title_to_competencies_employee(
    df: DataFrame,
    df_meta: metadata_container,
    prefix: Optional[int],
    depth: Optional[int],
) -> DataFrame:
    df = generalize_competencies(
        job_title_column_name="e10_isco",
        df=df,
        df_meta=df_meta,
        prefix=prefix,
        depth=depth,
    )

    job_title_to_competencies = df[["e10_isco_name", *get_competencies_list_employee()]]
    job_title_to_competencies = job_title_to_competencies.set_index("e10_isco_name")

    return job_title_to_competencies


def get_competencies_list_boss() -> List[str]:
    competencies_keys = ["K" + str(i) for i in range(1, 25)]

    return competencies_keys


def get_job_title_to_competencies_boss(
    df: DataFrame,
    df_meta: metadata_container,
    prefix: Optional[int],
    depth: Optional[int],
) -> DataFrame:
    df = generalize_competencies(
        job_title_column_name="P5_isco6",
        df=df,
        df_meta=df_meta,
        prefix=prefix,
        depth=depth,
    )

    job_title_to_competencies = df[["e10_isco_name", *get_competencies_list_boss()]]
    job_title_to_competencies = job_title_to_competencies.set_index("e10_isco_name")

    return job_title_to_competencies


def show_competencies(df: DataFrame) -> None:
    plt.imshow(df, cmap="RdYlGn")
    plt.colorbar()
    plt.yticks(range(len(df)), df.index)
    plt.show()
