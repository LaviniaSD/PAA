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
sample_dados_gerados = dg.DataGrid()

# Populando datagrid
dg.DataGrid.read_csv(sample_dados_gerados, "data\dados_gerados.csv", separator=";")

# Iniciando lista para conter dicionários com tempo de execução
lista_dict_times = []

# Obtendo tempo de execução
for column in columns_datagrid:
    # Adicionando colunas no dataframe
    new_dict = {"File name": "sample_dados_gerados", "File size": sample_dados_gerados.size, "Sorted by": column}
    try:
        dg.DataGrid.quick_sort(sample_dados_gerados, column=column, direction="asc")
        new_dict["quick_sort"] = timer._execution_times["quick_sort"]

    except TypeError:
        new_dict["quick_sort"] = None
    
    # Desordenando DataGrid
    dg.DataGrid.quick_sort(sample_dados_gerados, column=id, direction="desc")
    try:
        dg.DataGrid.insertion_sort(sample_dados_gerados, column=column, direction="asc")
        new_dict["insertion_sort"] = timer._execution_times["insertion_sort"]
    except TypeError:
        new_dict["insertion_sort"] = None

    # Desordenando DataGrid
    dg.DataGrid.quick_sort(sample_dados_gerados, column=id, direction="desc")
    try:
        dg.DataGrid.selection_sort(sample_dados_gerados, column=column, direction="asc")
        new_dict["selection_sort"] = timer._execution_times["selection_sort"]
    except TypeError:
        new_dict["selection_sort"] = None

    # Desordenando DataGrid
    dg.DataGrid.quick_sort(sample_dados_gerados, column=column, direction="desc")
    try:
        dg.DataGrid.merge_sort(sample_dados_gerados, column=column, direction="asc", start=0, end=None)
        new_dict["merge_sort"] = timer._execution_times["merge_sort"]
    except TypeError:
        new_dict["merge_sort"] = None
    
    # Desordenando DataGrid
    dg.DataGrid.quick_sort(sample_dados_gerados, column=id, direction="desc")
    try:
        dg.DataGrid.heap_sort(sample_dados_gerados, sample_dados_gerados.size, column=column, direction="asc")
        new_dict["heap_sort"] = timer._execution_times["heap_sort"]
    except TypeError:
        new_dict["heap_sort"] = None

    # Desordenando DataGrid
    dg.DataGrid.quick_sort(sample_dados_gerados, column=id, direction="desc")
    try:
        dg.DataGrid.radix_sort(sample_dados_gerados, pos=0, column=column, lim=20, start=0, end=-1, direction="asc", not_sort=True)
        new_dict["radix_sort"] = timer._execution_times["radix_sort"]
    except TypeError:
        new_dict["radix_sort"] = None

    lista_dict_times.append(new_dict)

analise_de_tempo=pd.DataFrame(lista_dict_times)

# Analisando apenas as colunas com valores númericos
numeric_columns = analise_de_tempo.select_dtypes(include=['number'])
# Retirando a coluna File size
relevant_columns = numeric_columns.drop(columns=["File size"])

# Função para encontrar o nome da coluna com o maior valor em uma linha
def get_column_with_max_value(row):
    return row.idxmax()

# Função para encontrar o nome da coluna com o menor valor em uma linha
def get_column_with_min_value(row):
    return row.idxmin()

analise_de_tempo["Sort mais demorado"] = relevant_columns.apply(get_column_with_max_value, axis=1)

# Adicionar coluna com o nome da coluna do menor valora
analise_de_tempo["Sort mais rápido"] = relevant_columns.apply(get_column_with_min_value, axis=1)

print(analise_de_tempo)
