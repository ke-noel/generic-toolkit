'''
CSV to parquet conversion.
'''
import os
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
import re
import argparse

# create parquet copies of all files in given directory
def csv_to_pq(csv_dir, pq_dir):
    files = os.listdir(csv_dir)

    for file in files:
        df = pd.read_csv(csv_dir + file).set_index('record_id')
        tbl = pa.Table.from_pandas(df)
        pq_name = re.sub('csv', 'parquet', file)
        pq.write_table(tbl, pq_dir + pq_name)


parser = argparse.ArgumentParser()

parser.add_argument('-i', '--indir',
                    dest='indir',
                    action='store',
                    required=True,
                    type=str,
                    help='CSV folder to convert.')

parser.add_argument('-o', '--outdir',
                    dest='outdir',
                    action='store',
                    required=True,
                    type=str,
                    help='Folder to send parquet records to.')

arguments = parser.parse_args()


csv_to_pq(arguments.indir, arguments.outdir)
