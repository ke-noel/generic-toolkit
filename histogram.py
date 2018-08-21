'''
Class to define and write histograms for the Toolkit base class.
'''
import physt


class Histogram(object):
    def __init__(self, name, savedir, bins, vals=None):
        self.name = name
        self.savedir = savedir
        self.bins = bins
        self.vals = [] if vals is None else vals

    def append_vals(self, new_vals):
        if type(new_vals) == list:
            self.vals += new_vals
        else:
            self.vals.append(new_vals)

    def make_hist(self):
        self.hist = physt.histogram(self.vals, name=self.name, bins=self.bins)
        self.hist.to_json(self.savedir + self.name + '.json')
