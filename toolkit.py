'''
Base algorithm class. It runs a selected tool on given data
and populates histograms and timers as it iterates through.
'''
import tools.linkage
from histogram import Histogram
from writer import  Writer
import os


class GenericToolkit(object):
    tools = {'Linkage': {'class': tools.linkage.Linkage,
                         'config': {'cutoff': None, 'block_on': [], 'exact': [], 'string':[], 'method': 'jarowinkler'}}}  # number and type expected by tool

    def __init__(self, tool, tag, args_dict):
        self.tool = self.tools[tool]
        self.savedir = '../' + tag + '/'

        if not os.path.isdir(self.savedir):
            os.mkdir(self.savedir)

        for key in args_dict:
            if key not in self.tool['config']:
                raise Exception('Invalid argument: %s' %key)
            self.tool['config'][key] = args_dict[key]

        self.instance = self.tool['class'](self.tool['config'])

        self.histograms = {}  # dictionary of histogram objects
        for hist in self.instance.hist_defs:
            new_hist = Histogram(hist, self.savedir, self.instance.hist_defs[hist]['bins'])
            self.histograms.update({hist: new_hist})

    # run tool and timer, and update histograms
    def run(self, data):
        self.instance.run(data)

        for hist in self.histograms:
            self.histograms[hist].append_vals(self.instance.hist_defs[hist]['source'])

    # write histograms to JSON and indicated files to parquet
    def write_hists(self):
        for hist in self.histograms:
            print(self.histograms[hist].vals)
            self.histograms[hist].make_hist()

    def write_files(self):
        for file in self.instance.outfiles:
            writer = Writer(self.instance.outfiles[file], self.savedir + file)
            writer.write()
