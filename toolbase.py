'''
Base class for the toolkit's tools. Ensures certain
functions and variables are present in a predictable way.
'''
from abc import abstractmethod, abstractproperty


class ToolBase(object):
    # histogram definitions
    @abstractproperty
    def hist_defs(self):
        return {}

    # expected files to return
    @abstractproperty
    def outfiles(self):
        return {}

    @abstractproperty
    def data_format(self):
        raise NotImplementedError

    # based on constructor used by GenericToolkit class
    def __init__(self, d):
        for key in d:
            setattr(self, key, d[key])

    # executed by the GenericToolkit class
    @abstractmethod
    def run(self, *data):
        raise NotImplementedError

    def update_hists(self):
        raise NotImplementedError

    def set_outfiles(self):
        raise NotImplementedError

    def check_type(self, data):
        if len(data[0]) is self.data_format['number']:
            for datum in data[0]:
                if type(datum) is not self.data_format['type']:
                    raise Exception('Error: expected %s, got %s.'
                                    %(self.data_format['type'], type(datum)))
        else:
            raise Exception('Error: expected %d args, got %d.' %(self.data_format['number'], len(data[0])))
