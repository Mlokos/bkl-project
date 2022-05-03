import pickle
from pyreadstat import read_sav
from pandas import DataFrame, read_spss
from typing import Tuple, Union
from pathlib import Path
from dataclasses import dataclass
from pyreadstat._readstat_parser import metadata_container


def load_sav_data() -> Tuple[DataFrame, DataFrame]:
    path_employee_df = Path('bin/employee_sav_df.pkl')
    path_employee_meta = Path('bin/employee_sav_meta.pkl')
    path_boss_df = Path('bin/boss_sav_df.pkl')
    path_boss_meta = Path('bin/boss_sav_meta.pkl')

    employee_sav_df = None
    employee_sav_meta = None
    boss_sav_df = None
    boss_sav_meta = None

    bin_path = Path('bin')
    if not bin_path.exists():
        bin_path.mkdir(exist_ok=False)

    if all([
        path_employee_df.is_file(),
        path_employee_meta.is_file(),
        path_boss_df.is_file(),
        path_boss_meta.is_file()
    ]):
        with open(path_employee_df, 'rb') as file:
            employee_sav_df = pickle.load(file)
        with open(path_employee_meta, 'rb') as file:
            employee_sav_meta = pickle.load(file)
        with open(path_boss_df, 'rb') as file:
            boss_sav_df = pickle.load(file)
        with open(path_boss_meta, 'rb') as file:
            boss_sav_meta = pickle.load(file)
    else:
        employee_sav_df, employee_sav_meta = read_sav('datasets/Baza_danych_z_badania_ludnoci_BKL_edycja_2019.sav')
        boss_sav_df, boss_sav_meta = read_sav('datasets/Baza_danych_z_badania_pracodawcw_BKL_edycja_2019.sav')

        with open(path_employee_df, 'wb') as file:
            pickle.dump(employee_sav_df, file)
        with open(path_employee_meta, 'wb') as file:
            pickle.dump(employee_sav_meta, file)
        with open(path_boss_df, 'wb') as file:
            pickle.dump(boss_sav_df, file)
        with open(path_boss_meta, 'wb') as file:
            pickle.dump(boss_sav_meta, file)

    return employee_sav_df, employee_sav_meta, boss_sav_df, boss_sav_meta
    

def load_spss_data() -> Tuple[DataFrame, DataFrame]:
    path_employee = Path('bin/employee_spss_df.pkl')
    path_boss = Path('bin/boss_spss_df.pkl')

    employee_spss_df = None
    boss_spss_df = None
    
    bin_path = Path('bin')
    if not bin_path.exists():
        bin_path.mkdir(exist_ok=False)
        
    if all([path_employee.is_file(), path_boss.is_file()]):
        with open(path_employee, 'rb') as file:
            employee_spss_df = pickle.load(file)
        with open(path_boss, 'rb') as file:
            boss_spss_df = pickle.load(file)
    else:
        employee_spss_df = read_spss('datasets/Baza_danych_z_badania_ludnoci_BKL_edycja_2019.sav')
        boss_spss_df = read_spss('datasets/Baza_danych_z_badania_pracodawcw_BKL_edycja_2019.sav')

        with open(path_employee, 'wb') as file:
            pickle.dump(employee_spss_df, file)
        with open(path_boss, 'wb') as file:
            pickle.dump(boss_spss_df, file)

    return employee_spss_df, boss_spss_df


@dataclass
class SavAdapter():
    metadata: metadata_container

    def get_column_values_dict(self, column_name: str) -> dict:
        label_name = self.metadata.variable_to_label[column_name]
        label_dict = self.metadata.value_labels[label_name]

        return label_dict

    def get_value_name(self, column_name: str, value: Union[str, float]) -> Union[str, float]:
        label_dict = self.get_column_values_dict(column_name)

        return label_dict[value]