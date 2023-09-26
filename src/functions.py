import datagrid

#read_csv function  
def read_csv(file,separator = ","):
    """
    Transforma um csv em um datagrid.
    
    Retorna uma datagrid cujos elementos são os dicionários criados.

    Args:
        file (str): documento csv com primeira linha "id,owner_id,creation_date,count,name,content"
        separator (str, optional): separador do csv. Defaults to ","

    Returns:
        DataGrid: datagrid com os valores do csv
    """
    arquivo = open(file,"r")
    data_grid = datagrid.DataGrid()
    #Verificando que não estamos na linha com os nomes da coluna do csv.
    linha_chave = 0
    chaves = ['id', 'owner_id', 'creation_date', 'count', 'name', 'content']
    for linha in arquivo:
        if linha_chave != 0:
            #Listando os elementos de cada linha.
            linha = linha.split(separator)
            #Retirando o "\n" no final do último elementod a lista.
            linha[-1] = list(linha[-1])
            linha[-1] = linha[-1][:-1]
            linha[-1] = "".join(linha[-1])            
            dicionario = {}
            elemento = 0
            #Criando chaves valor do dicionário
            for chave in chaves:
                if elemento == 0 or elemento == 3:
                    dicionario[chave] = int(linha[elemento])
                else:
                    dicionario[chave] = linha[elemento]
                elemento += 1
            data_grid.insert_row(dicionario)
        linha_chave = 1
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


