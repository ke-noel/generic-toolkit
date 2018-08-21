'''
Basic record linkage between two chunks for use with the Toolkit base class.
'''
import recordlinkage as rl
from toolbase import ToolBase
import random
import pandas as pd


class Linkage(ToolBase):
    hist_defs = {'pairs': {'bins': None, 'source': None},
                 'real_dups': {'bins': None, 'source': None},
                 'dups': {'bins': None, 'source': None}}
    outfiles = {'pairs': None,  # name, source
                'features': None,
                'matches': None}
    data_format = {'number': 2, 'type': pd.DataFrame}

    dfA = None
    dfB = None

    pairs = None
    features = None
    matches = None

    def run(self, *data):
        self.check_type(data)
        self.dfA = data[0][0]
        self.dfB = data[0][1]

        self.pairs = self.get_pairs()
        self.features = self.get_features()
        self.matches = self.get_matches()

        self.update_hists()
        self.set_outfiles()

    def get_pairs(self):
        if not self.block_on:  # if no blocks were set, do a full index
            indexer = rl.index.Full()
            pairs = indexer.index(self.dfA, self.dfB)
        else:
            for block in self.block_on:
                indexer = rl.index.Block(left_on=block, right_on=block)
                pairs = indexer.index(self.dfA, self.dfB)
                try:
                    combined_pairs = last_pairs.union(pairs)
                except:
                    pass
                last_pairs = pairs
        try:  # more than one block
            return combined_pairs
        except:  # one block
            return pairs

    def get_features(self):
        comp = rl.Compare()

        for lbl in self.string:
            comp.string(lbl, lbl, method=self.method, threshold=0.75, label=lbl)
        for lbl in self.exact:
            comp.exact(lbl, lbl, label=lbl)

        return comp.compute(self.pairs, self.dfA, self.dfB)

    def get_matches(self):
        return self.features[self.features.sum(axis=1) > self.cutoff]

    def update_hists(self):
        # TODO find way to automate, then replace base class method
        # TODO replace rand with real data
        self.hist_defs['pairs']['source'] = random.randint(1, 5)
        self.hist_defs['real_dups']['source'] = random.randint(6, 10)
        self.hist_defs['dups']['source'] = random.randint(1, 2)

    def set_outfiles(self):
        # TODO find way to automate, then replace base class method
        self.outfiles['pairs'] = self.pairs
        self.outfiles['features'] = self.features
        self.outfiles['matches'] = self.matches
