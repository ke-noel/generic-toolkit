'''
Writer class for Toolkit project. Writes given data
frames and multiindices to parquet.
'''
import pandas as pd


class Writer(object):
    def __init__(self, data, path):
        self.data = data
        self.path = path + '.parquet'

    def write(self):
        type = self.get_type()

        if type is pd.MultiIndex:
            self.mi_to_pq()
        elif type is pd.DataFrame:
            self.df_to_pq()
        else:
            raise Exception('Error: unexpected data type.')

    def get_type(self):
        return type(self.data)

    def df_to_pq(self):
        self.data.to_parquet(self.path)

    def mi_to_pq(self):
        df = pd.DataFrame(index=self.data, columns=[''])
        df.to_parquet(self.path)
