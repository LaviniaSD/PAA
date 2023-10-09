import datagrid as dg
import timer
import pandas as pd
import sys
sys.setrecursionlimit(10**6) 

# Método para ver todas as colunas do dataframe
pd.set_option("display.max_columns", None)

# Colunas do datagrid para serem analisadas
columns_datagrid = ["id", "owner_id", "creation_date", "count", "name", "content", "timestamp"]

# Iniciando datagrid vazio
sample = dg.DataGrid()
sample_0 = dg.DataGrid()
sample_1 = dg.DataGrid()
sample_2 = dg.DataGrid()
sample_3 = dg.DataGrid()
sample_4 = dg.DataGrid()
sample_5 = dg.DataGrid()
sample_6 = dg.DataGrid()
sample_7 = dg.DataGrid()
# Populando datagrid
dg.DataGrid.read_csv(sample, "data\sample.csv", separator=",")
dg.DataGrid.read_csv(sample_0, "data\dados_gerados_big.csv", separator=",")
dg.DataGrid.read_csv(sample_1, "data\dados_gerados_big_1.csv", separator=",")
dg.DataGrid.read_csv(sample_2, "data\dados_gerados_big_2.csv", separator=",")
dg.DataGrid.read_csv(sample_3, "data\dados_gerados_big_3.csv", separator=",")
dg.DataGrid.read_csv(sample_4, "data\dados_gerados_big_4.csv", separator=",")
dg.DataGrid.read_csv(sample_5, "data\dados_gerados_big_5.csv", separator=",")
dg.DataGrid.read_csv(sample_6, "data\dados_gerados_big_6.csv", separator=",")
dg.DataGrid.read_csv(sample_7, "data\dados_gerados_big_7.csv", separator=",")
files_datagrid = [sample_0, sample_1, sample_2, sample_3, sample_4, sample_5, sample_6, sample_7]
files = [sample]
def analise_sort(files_datagrid, columns_datagrid, *args):
    # Obtendo tempo de tempo
    for data_file in files_datagrid:
        for column in columns_datagrid:
            for func in args:
                try:
                    func(data_file, column=column, direction="asc")
                except TypeError:
                    pass

analise_sort([sample], columns_datagrid, (dg.DataGrid.insertion_sort,), (dg.DataGrid.selection_sort,), (dg.DataGrid.merge_sort,), (dg.DataGrid.heap_sort,),(dg.DataGrid.quick_sort,),(dg.DataGrid.radix_sort,) )            
timer.get_execution_time(dg.DataGrid.insertion_sort, True)