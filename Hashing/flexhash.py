import sys
import os
import itertools
import statistics
from nltk import ngrams
import hashlib
from itertools import combinations
import numpy as np
import pandas as pd
import multiprocessing
from tqdm import tqdm


class FlexHash:
    def __init__(self, acc_size, window_size, comb_size):

        self.acc_size = acc_size
        self.window_size = window_size

        # set combination size, if bigger than window, take window size instead
        if window_size > comb_size:
            self.comb_size = comb_size
        else:
            self.comb_size = window_size
        self.accumulator = [0] * self.acc_size
        self.window = [-1] * window_size
        self.hash_const = []

        np.random.seed(30)
        hash_const = np.random.choice(range(acc_size), size=acc_size, replace=False)
        for item in hash_const:
            self.hash_const.append(item)

    def hashenator(self, s):
        result = 1
        for item in s:
            result = item * result
        return (result + 3) % self.acc_size

    def calc_digest(self, str1, label):

        counter = 0

        # iterate through string with sliding window of x bytes
        for x in range(counter, len(str1)):
            self.window = str1[x : x + self.window_size]
            counter += 1

            # take each combination of size n
            for combination in itertools.combinations(self.window, self.comb_size):
                # call hash function
                val = self.hashenator(combination)

                # get index of value in hash_const array
                ind = self.hash_const.index(val)

                # increment value at accumulator
                self.accumulator[ind] += 1

        # find median value in accumulator
        median_value = statistics.median(self.accumulator)

        # assign 1 or 0 based on median
        for x in range(0, self.acc_size):
            if self.accumulator[x] <= median_value:
                self.accumulator[x] = 0
            else:
                self.accumulator[x] = 1

        # create list to hold final feature vector
        hash_list = []

        # iterate through each byte and convert to decimal
        for x in range(0, self.acc_size, 8):
            new_string = ""
            this_byte = self.accumulator[x : x + 8]

            for bit in this_byte:
                new_string += str(bit)
            entry = int(new_string, 2)
            hash_list.append(str(entry))

        hash_list.append(label)

        return hash_list
