import pandas as pd
import matplotlib.pyplot as plt
dffirst = pd.read_csv("input.txt", sep='|', 
                       dtype='str', na_filter=False,
                       header = None).iloc[:, 1:-1]
dffirst = dffirst.applymap(lambda x: float(x[:-4]))

dfsecond = pd.read_csv("input2.txt", sep='|', 
                      dtype='str', na_filter=False,
                      header = None).iloc[:, 1:-1]
dfsecond = dfsecond.applymap(lambda x: float(x[:-4]))


diff = dffirst.subtract(dfsecond)
diff = diff.transpose()
diff = diff.reindex(diff.mean().sort_values().index, axis=1)
means = diff.mean()
mins = diff.min()


diff.plot(kind='box')

means.plot(kind='box')

mins.plot(kind='box')


diff_norm = diff.apply(lambda x: x / max(x.min(), x.max(), key=abs))
diff_norm = diff_norm.reindex(diff_norm.mean().sort_values().index, axis=1)
diff_norm

diff_norm.plot(kind='box')


div_diff = dffirst.divide(dfsecond)
div_diff = div_diff.transpose()
div_diff = div_diff.reindex(div_diff.mean().sort_values().index, axis=1)

div_diff.plot(kind='box')

