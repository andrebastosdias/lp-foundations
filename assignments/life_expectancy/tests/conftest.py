"""Pytest configuration file"""
import shutil

import pandas as pd
import pytest

from . import FIXTURES_DIR, OUTPUT_DIR
from ..cleaning import clean_data


@pytest.fixture(scope="session")
def eu_life_expectancy_raw() -> pd.DataFrame:
    shutil.copy(OUTPUT_DIR / "eu_life_expectancy_raw.tsv", FIXTURES_DIR / "eu_life_expectancy_raw.tsv")
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_raw.tsv", sep="\t")


@pytest.fixture(scope="session")
def eu_life_expectancy_expected() -> pd.DataFrame:
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected.csv")


@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")
