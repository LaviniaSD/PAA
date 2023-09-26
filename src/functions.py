import datagrid

#list_csv function  
def list_csv(file,separator=','):
    """
    Lista linhas do documento csv.
    
    Retorna uma lista cujos elementos são cada linha do csv em forma de lista.

    Parâmetros
    ---
    doc_csv: str

    Retorno
    ---
    return: list
    """
    #Abrir csv como arquivo_csv.
    with open(file, "r") as arquivo_csv:
        #Criar lista vazia para inserir as linhas em forma de lista. 
        arquivo_csv_lista = []
        for linha in arquivo_csv:
            linha += separator 
            #Lista para receber elementos das colunas do csv.
            linha_lista = []
            #Lista para transformar caracteres em palavras.
            palavra = []
            for letra in linha:
                #O caractere "," indica que estamos mudando de coluna.
                if letra != separator:
                    palavra.append(letra)
                else: 
                    #Adicionando a string da lista palavra na linha
                    linha_lista.append("".join(palavra))
                    #Esvaziando a lista, pois já trasnformamos em string a coluna da linha.
                    palavra = []
            linha_lista[-1] = list(linha_lista[-1])
            linha_lista[-1] = linha_lista[-1][:-1]
            linha_lista[-1] = "".join(linha_lista[-1])
            #Adicionando linha no arquivo csv
            arquivo_csv_lista.append(linha_lista)
        
        return arquivo_csv_lista

#read_csv function  
def read_csv(file,separator=','):
    """
    Transforma cada linha do csv em um dicionário cujas chaves são os valores da primeira linha do csv e os valores cada coluna de cada linha, fora a inicial.
    
    Retorna uma datagrid cujos elementos são os dicionários criados.

    Parâmetros
    ---
    doc_csv: str

    Retorno
    ---
    return: list
    """
    arquivo_csv = list_csv(file, separator)
    contador_linha = 0
    chaves = []
    lista_dict = []
    for linha in arquivo_csv:
        if contador_linha == 0:
            chaves = linha
            print(type(chaves))
        else: 
            linha_dicionario = {}
            coluna = 0
            for chave in chaves:
                linha_dicionario[chave] = linha[coluna]
                coluna += 1
            lista_dict.append(linha_dicionario)
        contador_linha += 1
    print(lista_dict)
    data_grid = datagrid.DataGrid()
    for dicionario in lista_dict:
        data_grid.insert_row(dicionario)
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


