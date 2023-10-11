import sys
import timer

import pandas as pd

import datagrid as dg

from exceptions import InvalidColumnError

sys.setrecursionlimit(10**6) 

# Método para ver todas as colunas do dataframe
pd.set_option("display.max_columns", None)

def analise_sort(datagrids, columns_datagrid, sorts):

    # Inicializa um Pandas DataFrame para armazenar os resultados
    results = pd.DataFrame(columns=["Função", "Coluna", "Tamanho da amostra", "Tempo de execução"])

    # Itera sobre cada datagrid
    for datagrid in datagrids:

        # Cria uma cópia do datagrid para ser usado nas funções de ordenação
        datagrid_copy = datagrid.copy()

        # Itera sobre cada função de ordenação
        for sort_type in sorts:
            # Itera sobre cada coluna do datagrid
            for column in columns_datagrid:
                try:
                    datagrid_copy.sort(column=column, direction="asc", strategy=sort_type)
                    print(f"Função: Sort({sort_type}) | Coluna: {column} | Tempo de execução: {timer.get_execution_time(sort_type)} ns")
                except InvalidColumnError:
                    pass # Erros relacionados a colunas não suportadas são ignorados
                except Exception as error:
                    print(f"Erro inesperado na função: Sort({sort_type}): \n {error}")
                    pass
                else:
                    # Armazena o resultado da execução da função em um Pandas DataFrame
                    results = results._append({"Função": sort_type, "Coluna": column, "Tamanho da amostra": datagrid.size, "Tempo de execução": timer.get_execution_time(sort_type)}, ignore_index=True)

    # Retorna o dataframe com os resultados
    return results

# Datagrids a serem testados
samples = []
samples_paths=["data\dados_gerados_big.csv", 
            #    "data\dados_gerados_big_1.csv", 
            #    "data\dados_gerados_big_2.csv", 
            #    "data\dados_gerados_big_3.csv", 
            #    "data\dados_gerados_big_4.csv", 
            #    "data\dados_gerados_big_5.csv", 
            #    "data\dados_gerados_big_6.csv", 
            #    "data\dados_gerados_big_7.csv"
            ]

# Carrega os datagrids a serem bases para os testes
for file_path in samples_paths:
    sample = dg.DataGrid()
    sample.read_csv(file_path, separator=",")
    samples.append(sample)

# Colunas do datagrid para serem testadas
columns_datagrid = ["id", "owner_id", "creation_date", "count", "name", "content", "timestamp"]

# Estratégias de ordenação a serem testadas
sorts = ["insertion_sort", "selection_sort", "merge_sort", "quick_sort", "heap_sort", "radix_sort"]

results = analise_sort(samples, columns_datagrid, sorts)
print(results)