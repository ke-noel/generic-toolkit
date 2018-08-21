'''
Timer class for Toolkit.
'''
import time as t


class Timer(object):
    def __init__(self):
        self.counter = 0
        self.times = []
        self.time = None

    def start(self):
        self.start_time = t.perf_counter()

    def end(self):
        self.end_time = t.perf_counter()
        self.counter += 1
        self.time = self.end_time - self.start_time
        self.times.append(self.time)

    def get_avg(self):
        return sum(self.times) / self.counter