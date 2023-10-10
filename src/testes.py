import datagrid as dg
import timer
import pandas as pd
import sys
sys.setrecursionlimit(10**6)
sample = dg.DataGrid()

# Populando datagrid
dg.DataGrid.read_csv(sample, "data\sample.csv", separator=",")
dg.DataGrid.insertion_sort(sample, column="id", direction="asc", optimized = True)
dg.DataGrid.show(sample)