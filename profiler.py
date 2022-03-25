#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib.pyplot as plt
import argparse


def read_queries(path):      # reads file with quesries, returns dataframe
    df = pd.read_csv(path, sep='|',
                       dtype='str', na_filter=False,
                       header = None).iloc[:, 1:-1]
    return df.applymap(lambda x: float(x[:-4]))

def normalize(df):          # sorts quesries in ascending order by their mean value, FIXME
    return df.reindex(df.mean().sort_values().index, axis=1)


def main():
     parser = argparse.ArgumentParser(description='Compare execution time of mdb queries')

     parser.add_argument('baseline', type=str,
                      help='Path to baseline file')
     parser.add_argument('test', type=str,
                      help='Path to test file')
     args = parser.parse_args()


     dffirst = read_queries(args.baseline) # read baseline into dataframe
     dfsecond = read_queries(args.test) # read test into dataframe

     diff = dffirst.subtract(dfsecond) # create difference of quesry times
     diff = diff.transpose()           # transpose it so we can plot it
     diff = normalize(diff)

     means = diff.mean()

     mins = diff.min()

     diff_norm = diff.apply(lambda x: x / max(x.min(), x.max(), key=abs)) # difference normalized by max value
     diff_norm = normalize(diff_norm)

     div_diff = dffirst.divide(dfsecond) # ratio of query times
     div_diff = div_diff.transpose()
     div_diff = normalize(div_diff)

     plt.rcParams["figure.figsize"] = [10.50, 32.0]
     plt.rcParams["figure.autolayout"] = True

     fig, axes = plt.subplots(nrows=5, ncols=1)

     diff.plot(ax=axes[0], kind='box')

     diff_norm.plot(ax=axes[3], kind='box')

     div_diff.plot(ax=axes[4], kind='box')

     means.plot(ax=axes[1], kind='box')
     mins.plot(ax=axes[2], kind='box')

     axes[0].set_title('Raw difference (baseline - test)')
     axes[3].set_title('Normed (by max) difference (baseline - test)')
     axes[4].set_title('Ratio (baseline/test)')
     axes[1].set_title('Means for difference')
     axes[2].set_title('Minimums (best runs) for difference')
     axes[0].set(xlabel="Query number")
     axes[0].set(ylabel="Seconds")
     axes[3].set(xlabel="Query number")
     axes[4].set(xlabel="Query number")
     axes[1].set(ylabel="Seconds")
     axes[2].set(ylabel="Seconds")
     for i in range(5):
        axes[i].axhline(y=0, color='r', linestyle=':')
     #plt.show()
     plt.savefig('Queries_profile.pdf') # It seems pdf gives the best resolution


if __name__ == '__main__':
    main()
