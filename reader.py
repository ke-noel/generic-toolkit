'''
Reader class for toolkit. Reads Parquet (designed for Parquet) and CSV files and prepares them for analysis.
'''
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
import os
import itertools


class Reader(object):
    def __init__(self, path, rel_cols=None):
        self.path = path
        self.rel_cols = rel_cols

        self.cross_list = None

    def cross(self):
        files = os.listdir(self.path)
        self.cross_list = list(itertools.product(files, files))

    def read_csv(self, file):
        return pd.read_csv(file).set_index('record_id')

    def read_pq(self, file):
        tbl = pq.read_table(file)
        return pa.Table.to_pandas(tbl)

    def read_cols_csv(self, file):
        df = self.read_csv(file)
        for col in df.columns:
            if col not in self.rel_cols:
                df.drop(col, axis=1, inplace=True)
        return df

    def read_cols_pq(self, file):
        tbl = pq.read_table(file, columns=self.rel_cols)
        return pa.Table.to_pandas(tbl)

    def read(self, file):
        return self.read_csv(file)
