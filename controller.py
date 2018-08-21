'''
Controls the behaviour of the toolkit class.
'''
from toolkit import GenericToolkit
from timer import Timer
from reader import Reader
import numpy as np


class Controller(object):
    timers = {'job_timer': None,
              'read_timer': None,
              'run_timer': None,
              'write_timer': None}

    mem_usage = []

    def __init__(self, file, dir, tag, tool, **kwargs):
        for timer in self.timers:
            new_timer = Timer()
            self.timers[timer] = new_timer

        self.file = file

        self.timers['job_timer'].start()

        self.toolkit = GenericToolkit(tool, tag, kwargs)

        # TODO configured for record linkage tool, make generic
        self.reader = Reader(dir, rel_cols=['Name', 'SIN', 'DOB', 'Province', 'PhoneNum', 'record_id'])

        self.__exec()

    def __exec(self):
        # TODO modify to pass multiple inputs; set this way for benchmarks
        self.timers['read_timer'].start()
        datum = self.reader.read(self.file)
        self.timers['read_timer'].end()
        self.log_mem_usage(datum)

        # send data to toolkit
        self.timers['run_timer'].start()
        self.toolkit.run([datum, datum])
        self.timers['run_timer'].end()

        self.__end()

    def __end(self):
        # can only be run if more than one file is inputted
        #self.toolkit.write_hists()

        self.timers['write_timer'].start()
        self.toolkit.write_files()
        self.timers['write_timer'].end()

        self.timers['job_timer'].end()

    def log(self):
        read_times = np.array(self.timers['read_timer'].times)
        run_times = np.array(self.timers['run_timer'].times)
        write_times = np.array(self.timers['write_timer'].times)
        df_memory = np.array(self.mem_usage)

        print('Job time: %f seconds' %self.timers['job_timer'].time)
        print('Mean read time: %f seconds, standard deviation: %f\n' %(read_times.mean(), read_times.std()))
        print('Mean run time: %f seconds, standard deviation: %f\n' %(run_times.mean(), run_times.std()))
        print('Mean write time: %f seconds, standard deviation: %f\n' %(write_times.mean(), write_times.std()))
        print('Mean dataframe memory usage: %f MB, standard deviation: %f\n' %(df_memory.mean(), df_memory.std()))

    def log_mem_usage(self,  df):
        b_usage = df.memory_usage(deep=True).sum()
        self.mem_usage.append(b_usage / 1024 ** 2)


if __name__ == '__main__':
    cont = Controller('pq_records/', 'tag', 'Linkage', cutoff=4,
                    block_on=['SIN', 'DOB'],
                    exact=['SIN', 'DOB', 'PhoneNum', 'Province'],
                    string=['Name'])
