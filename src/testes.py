import datagrid as dg
import timer
import pandas as pd
import sys
sys.setrecursionlimit(10**6)
sample = dg.DataGrid()

# Populando datagrid
dg.DataGrid.read_csv(sample, "data\sample.csv", separator=",")
dg.DataGrid.sort(sample, column="owner_id", direction="desc", strategy="radix_sort")
dg.DataGrid.show(sample)