import argparse
import os
from typing import Optional, Union

import pandas as pd

from life_expectancy.region import Region

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def load_data() -> pd.DataFrame:
    '''Load the raw data for the given country.'''
    df = pd.read_csv(os.path.join(DATA_DIR, 'eu_life_expectancy_raw.tsv'), sep='\t')
    return df


def save_data(df: pd.DataFrame) -> None:
    '''Save the cleaned data to a CSV file.'''
    df.to_csv(os.path.join(DATA_DIR, 'pt_life_expectancy.csv'), index=False)


def clean_data(df: pd.DataFrame, country: Optional[Region]) -> pd.DataFrame:
    '''Clean the raw data.'''
    df_split = df['unit,sex,age,geo\\time'].str.split(',', expand=True)
    df_split.columns = ['unit', 'sex', 'age', 'region']
    df = pd.concat([df_split, df.drop(columns=['unit,sex,age,geo\\time'])], axis=1)
    df = df.melt(id_vars=['unit', 'sex', 'age', 'region'], var_name='year', value_name='value')

    df['year'] = df['year'].astype(int)

    df['value'] = pd.to_numeric(df['value'].str.extract(r'^(\d*\.?\d+)')[0], errors='coerce').astype(float)
    df = df.dropna(subset=['value'])

    if country:
        df = df[df['region'] == country.name]

    return df.reset_index(drop=True)


def main(country: Optional[Union[str, Region]]) -> pd.DataFrame:
    '''Main function.'''
    if isinstance(country, str):
        country = Region[country]
    df = load_data()
    df = clean_data(df, country)
    save_data(df)
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--country', type=str, default='PT', help='Country code to filter the data.')
    args = parser.parse_args()

    main(args.country)
