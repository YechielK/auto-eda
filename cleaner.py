import logging
import pandas as pd
import numpy as np
import scipy.stats as stats
from flask import g
def clean(df):
    g.before_shape = df.shape
    print(df.dtypes)
    # rename cols
    df = col_fix(df)
    # remove duplicates
    df = remove_duplicates(df)
    # remove nulls
    df = remove_nulls(df)
    # remove outliers
    df = remove_outliers(df)
    # reset indexes
    df = df.reset_index(drop=True)
    g.memory = df.memory_usage(deep=True).sum()//1024
    g.after_shape = df.shape
    return df

def col_fix(df):
    return df.rename(columns=name_fix(df), inplace=False)

def name_fix(df):
    cols = list(df.columns)
    newCols = {}
    for col in cols:
        print(col)
        newCols[col] = col.lower().replace(' ', '_')
    return newCols

def remove_nulls(df):
    nulls = df.isnull().sum().sum()
    print('contains ', nulls, ' nulls')
    g.nulls = nulls
    return df.dropna()

def remove_duplicates(df):
    duplicates = df.duplicated().sum()
    print('contains ', duplicates, ' duplicates')
    g.duplicates = duplicates
    return df.drop_duplicates()

def remove_outliers(df):

    # to be added to df
    z_score_cols = []

    # to remove zcols in df
    original_cols = list(df.columns)

    # only find outliers or cols with numbers
    numbered_cols = list(df.select_dtypes(np.number).columns)
    for col in numbered_cols:
        col_zscore = col + '_zscore'
        df[col_zscore] = abs(stats.stats.zscore(df[col]))
        z_score_cols.append(col_zscore)

    print('Before removal of outliers', df.shape)
    before_rows = df.shape[0]
    # row is false when it contains zscore > 3
    condition = (df[z_score_cols] < 3).all(axis=1)
    df = df[condition]

    # remove zscore cols
    df = df[original_cols]
    print('After removal of outliers', df.shape)
    outliers = before_rows - df.shape[0]
    print('contains ', outliers, ' outliers')
    g.outliers = outliers
    return df