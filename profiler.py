#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib.pyplot as plt
import argparse


def read_queries(path):
    df = pd.read_csv(path, sep='|',
                       dtype='str', na_filter=False,
                       header = None).iloc[:, 1:-1]
    return df.applymap(lambda x: float(x[:-4]))

def normalize(df):
    return df.reindex(df.mean().sort_values().index, axis=1)

def plot_show(df):
   df.plot(kind='box')
   plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare execution time of mdb queries')

    parser.add_argument('first_file', type=str,
                      help='Name of the first file')
    parser.add_argument('second_file', type=str,
                      help='Name of the second file')
    args = parser.parse_args()


    dffirst = read_queries(args.first_file)
    dfsecond = read_queries(args.second_file)



    diff = dffirst.subtract(dfsecond)
    diff = diff.transpose()
    diff = normalize(diff)

    means = diff.mean()

    mins = diff.min()

    diff_norm = diff.apply(lambda x: x / max(x.min(), x.max(), key=abs))
    diff_norm = normalize(diff_norm)

    div_diff = dffirst.divide(dfsecond)
    div_diff = div_diff.transpose()
    div_diff = normalize(div_diff)

    plot_show(diff)
    plot_show(means)
    plot_show(mins)
    plot_show(diff_norm)
    plot_show(div_diff)
