import numpy as np


class BaseSeries():

    def __init__(self):
        self.values = None

    def __getitem__(self, idx):
        return self.values[idx]

    def __setitem__(self, idx, data):
        self.values[idx] = data

    def save(self, filename):
        np.save(self.values, filename)

    def __len__(self):
        return len(self.values)

    def len(self):
        return len(self.values)

    def asarray(self):
        return self.values


class TimeSeries(BaseSeries):

    def __init__(self, len, dtype=float):
        super().__init__()
        self.type = dtype
        self.values = np.zeros(len, dtype)

    def bloat(self, len):
        self.values = np.pad(
            self.values,
            [(0, len)],
            mode='constant', constant_values=0)

    def finalize(self, tidx):
        """ throw away ending zeros """
        self.values = self.values[:tidx+1]


class TransitionHistory(BaseSeries):

    def __init__(self, len):
        super().__init__()
        self.itemsize = itemsize
        self.values = np.chararray((len, 3), itemsize=itemsize)


    def bloat(self, len):
        new_space = np.empty((len, 3))
        self.values = np.vstack([self.values, new_space])

    def finalize(self, tidx):
        """ throw away ending zeros """
        self.values = self.values[:tidx+1]

class TransitionHistoryInt(BaseSeries):

    def __init__(self, len, itemsize=5):
        super().__init__()
        self.values = np.zeros((len, 3), dtype="int8")

    def bloat(self, len):
        new_space = np.zeros((len, 3), dtype="int8")
        self.values = np.vstack([self.values, new_space])

    def finalize(self, tidx):
        """ throw away ending zeros """
        self.values = self.values[:tidx+1,:]
