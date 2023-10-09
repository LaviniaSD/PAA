import datagrid as dg
import timer
import pandas as pd
import sys
sys.setrecursionlimit(10**6)
sample = dg.DataGrid()

# Populando datagrid
dg.DataGrid.read_csv(sample, "data\sample.csv", separator=",")
dg.DataGrid.radix_sort(sample, pos=0, column="owner_id", lim=20, start=0, end=-1, direction="asc", not_sort=True)