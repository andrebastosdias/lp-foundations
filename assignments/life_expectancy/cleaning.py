import argparse
import os

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def clean_data(country: str):
    '''Clean the raw data and save it to a CSV file.'''
    df = pd.read_csv(os.path.join(DATA_DIR, 'eu_life_expectancy_raw.tsv'), sep='\t')

    df_split = df['unit,sex,age,geo\\time'].str.split(',', expand=True)
    df_split.columns = ['unit', 'sex', 'age', 'region']
    df = pd.concat([df_split, df.drop(columns=['unit,sex,age,geo\\time'])], axis=1)
    df = df.melt(id_vars=['unit', 'sex', 'age', 'region'], var_name='year', value_name='value')

    df['year'] = df['year'].astype(int)

    df['value'] = pd.to_numeric(df['value'].str.extract(r'^(\d*\.?\d+)')[0], errors='coerce').astype(float)
    df = df.dropna(subset=['value'])

    df = df[df['region'] == country]

    df.to_csv(os.path.join(DATA_DIR, 'pt_life_expectancy.csv'), index=False)

    print(df.info())
    print(df.describe(include='all'))
    print(df.head())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--country', type=str, default='PT', help='Country code to filter the data.')
    args = parser.parse_args()

    clean_data(args.country)
