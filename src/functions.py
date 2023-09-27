import datagrid

#read_csv function  
def read_csv(file,separator = ",",encoding = "utf-8"):
    """
    Transforma um csv em um datagrid.
    
    Retorna uma datagrid cujos elementos são os dicionários criados.

    Args:
        file (str): documento csv com primeira linha "id,owner_id,creation_date,count,name,content"
        separator (str, optional): separador do csv. Defaults to ","
        encoding (str, optional): codificação do arquivo. Defaults to "utf-8"
    Returns:
        DataGrid: datagrid com os valores do csv
    """
    file = open(file, mode = "r", encoding = encoding)
    data_grid = datagrid.DataGrid()
    # Verificando que não estamos na linha com os nomes da coluna do csv.
    key_row = 0
    keys = ['id', 'owner_id', 'creation_date', 'count', 'name', 'content']
    for row in file:
        if key_row != 0:
            # Listando os elementos de cada linha.
            row = row.split(separator)
            # Retirando o "\n" no final do último elementod a lista.
            row[-1] = row[-1].rstrip('\n')           
            dictionary = {}
            element = 0
            # Criando chaves valor do dicionário
            for key in keys:
                # Corrigindo o tipo de dado
                if element == 0 or element == 3:
                    dictionary[key] = int(row[element])
                else:
                    dictionary[key] = row[element]
                element += 1
            data_grid.insert_row(dictionary)
        else:
            key_row = 1
    return data_grid

#show function
def show(start=0,end=100):
    pass

#search function
def search(column,value):
    pass

#sort function
def sort(column, direction='asc'):
    pass

#select count function
def select_count(i,j):
    pass