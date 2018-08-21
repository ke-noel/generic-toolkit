import numpy as np
import os
import argparse


def get_disk_usage(path):
    l_size = os.stat(path).st_size
    b_size = os.statvfs(path).f_bsize
    disk_usage = ((l_size-1)/b_size+1)*b_size
    return disk_usage / 1000000


# Read benchmarking logs and get mean and standard deviation stats
def get_logs():
    with open('logs/' + arguments.tag + '/job_times.txt', 'r') as f:
        job_times = np.array([float(line.strip()) for line in f])

    with open('logs/' + arguments.tag + '/read_times.txt', 'r') as f:
        read_times = np.array([float(line.strip()) for line in f])

    with open('logs/' + arguments.tag + '/run_times.txt', 'r') as f:
        run_times = np.array([float(line.strip()) for line in f])

    with open('logs/' + arguments.tag + '/write_times.txt', 'r') as f:
        write_times = np.array([float(line.strip()) for line in f])

    with open('logs/' + arguments.tag + '/df_memory.txt', 'r') as f:
        df_memory = np.array([float(line.strip()) for line in f])

    csv_disk = []
    pq_disk = []

    for file in os.listdir('pq_records/'):
        pq_disk.append(get_disk_usage('pq_records/' + file))
    pq_disk = np.array(pq_disk)

    for file in os.listdir('records/'):
        csv_disk.append(get_disk_usage('records/' + file))
    csv_disk = np.array(csv_disk)

    with open('logs/' + arguments.tag + '/full_log.txt', 'w+') as f:
        f.write('Mean job time: %f seconds, standard deviation: %f\n' %(job_times.mean(), job_times.std()))
        f.write('Mean read time: %f seconds, standard deviation: %f\n' %(read_times.mean(), read_times.std()))
        f.write('Mean run time: %f seconds, standard deviation: %f\n' %(run_times.mean(), run_times.std()))
        f.write('Mean write time: %f seconds, standard deviation: %f\n' %(write_times.mean(), write_times.std()))
        f.write('Mean csv disk usage: %f MB, standard deviation: %f\n' %(csv_disk.mean(), csv_disk.std()))
        f.write('Mean parquet disk usage: %f MB, standard deviation: %f\n' %(pq_disk.mean(), pq_disk.std()))
        f.write('Mean dataframe memory usage: %f MB, standard deviation: %f\n' %(df_memory.mean(), df_memory.std()))
        f.close()


parser = argparse.ArgumentParser()

parser.add_argument('-t', '--tag',
                    dest='tag',
                    action='store',
                    required=True,
                    type=str,
                    help='Tag for logging. Must be the one used for benchmarking.')

arguments = parser.parse_args()

get_logs()