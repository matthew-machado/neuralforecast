# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/data_datasets__long_horizon.ipynb (unless otherwise specified).

__all__ = ['ETTh1', 'ETTh2', 'ETTm1', 'ETTm2', 'ECL', 'Exchange', 'Traffic', 'ILI', 'Weather', 'LongHorizonInfo',
           'LongHorizon']

# Cell
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from .utils import download_file, Info

# Cell
@dataclass
class ETTh1:
    freq: str = 'H'
    name: str = 'ETTh1'
    n_ts: int = 1

@dataclass
class ETTh2:
    freq: str = 'H'
    name: str = 'ETTh2'
    n_ts: int = 1

@dataclass
class ETTm1:
    freq: str = '15T'
    name: str = 'ETTm1'
    n_ts: int = 7

@dataclass
class ETTm2:
    freq: str = '15T'
    name: str = 'ETTm2'
    n_ts: int = 7

@dataclass
class ECL:
    freq: str = '15T'
    name: str = 'ECL'
    n_ts: int = 321

@dataclass
class Exchange:
    freq: str = 'D'
    name: str = 'Exchange'
    n_ts: int = 8

@dataclass
class Traffic:
    freq: str = 'H'
    name: str = 'traffic'
    n_ts: int = 862

@dataclass
class ILI:
    freq: str = 'W'
    name: str = 'ili'
    n_ts: int = 7

@dataclass
class Weather:
    freq: str = '10M'
    name: str = 'weather'
    n_ts: int = 21

# Cell
LongHorizonInfo = Info(groups=(
        'ETTh1', 'ETTh2', 'ETTm1', 'ETTm2',
        'ECL', 'Exchange', 'Traffic', 'ILI', 'Weather'
    ),
    class_groups=(
        ETTh1, ETTh2, ETTm1, ETTm2,
        ECL, Exchange, Traffic, ILI, Weather
    )
)

# Cell
@dataclass
class LongHorizon:

    source_url: str = 'https://nhits-experiments.s3.amazonaws.com/datasets.zip'

    @staticmethod
    def load(directory: str,
             group: str,
             cache: bool = True) -> Tuple[pd.DataFrame,
                                          Optional[pd.DataFrame],
                                          Optional[pd.DataFrame]]:
        """Downloads and loads ETT data.

        Parameters
        ----------
        directory: str
            Directory where data will be downloaded.
        group: str
            Group name.
            Allowed groups: 'ETTh1', 'ETTh2',
                            'ETTm1', 'ETTm2',
                            'ECL', 'Exchange',
                            'Traffic', 'Weather', 'ILI'.
        cache: bool
            If `True` saves and loads

        Notes
        -----
        [1] Returns train+val+test sets.
        """
        if group not in LongHorizonInfo.groups:
            raise Exception(f'group not found {group}')

        path = f'{directory}/longhorizon/datasets'
        file_cache = f'{path}/{group}.p'

        if os.path.exists(file_cache) and cache:
            df, X_df, S_df = pd.read_pickle(file_cache)

            return df, X_df, S_df

        LongHorizon.download(directory)
        path = f'{directory}/longhorizon/datasets'

        kind = 'M' if group not in ['ETTh1', 'ETTh2'] else 'S'
        name = LongHorizonInfo[group].name
        y_df = pd.read_csv(f'{path}/{name}/{kind}/df_y.csv')
        y_df = y_df.sort_values(['unique_id', 'ds'], ignore_index=True)
        y_df = y_df[['unique_id', 'ds', 'y']]
        X_df = pd.read_csv(f'{path}/{name}/{kind}/df_x.csv')
        X_df = y_df.drop('y', axis=1).merge(X_df, how='left', on=['ds'])

        S_df = None
        if cache:
            pd.to_pickle((y_df, X_df, S_df), file_cache)

        return y_df, X_df, S_df

    @staticmethod
    def download(directory: str) -> None:
        """Download ETT Dataset."""
        path = f'{directory}/longhorizon/datasets/'
        if not os.path.exists(path):
             download_file(path, LongHorizon.source_url, decompress=True)