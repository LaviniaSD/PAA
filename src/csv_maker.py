# Importe as bibliotecas necessárias
import numpy as np
import pandas as pd
import random
import string
from datetime import datetime
import nltk
# Certifique-se de baixar os recursos necessários do NLTK
nltk.download('words')
from nltk.corpus import words

# Função auxiliar para gerar conteúdo com palavras aleatórias
def gerar_conteudo_com_palavras_aleatorias(num_palavras):
    """Gera conteúdo com palavras aleatórias.
    
    Args:
        num_palavras (int): O número de palavras no conteúdo.
    
    Returns:
        str: O conteúdo gerado com palavras separadas por espaço.
    """
    # Recupere a lista de palavras do NLTK
    lista_de_palavras = words.words()
    
    conteudo = []

    for _ in range(num_palavras):
        palavra_aleatoria = random.choice(lista_de_palavras)
        conteudo.append(palavra_aleatoria)

    return ' '.join(conteudo)

# Função auxiliar para gerar uma data e hora aleatória
def gerar_data_hora_aleatoria():
    """Gera uma data e hora aleatória.

    Returns:
        datetime: Uma data e hora aleatória.
    """
    ano = random.randint(2000, 2023)  
    mes = random.randint(1, 12)
    dia = random.randint(1, 28)  
    hora = random.randint(0, 23)
    minuto = random.randint(0, 59)
    segundo = random.randint(0, 59)
    
    data_hora_aleatoria = datetime(ano, mes, dia, hora, minuto, segundo)
    return data_hora_aleatoria

# Função auxiliar para gerar dados de exemplo
def gerar_dados(num_linhas):
    """Gera dados de exemplo.

    Args:
        num_linhas (int): O número de linhas de dados a serem geradas.
    
    Returns:
        pandas.DataFrame: Um DataFrame com os dados gerados.
    """
    # Gera os IDs únicos e embaralha-os
    ids_unicos = np.arange(1, num_linhas + 1)
    np.random.shuffle(ids_unicos)
    
    # Gera os IDs dos donos
    owner_ids = [''.join(random.choices(string.ascii_letters + string.digits, k=5)) for _ in range(num_linhas)]
    
    # Gera as datas de criação
    creation_dates = [gerar_data_hora_aleatoria().strftime('%Y/%m/%d %H:%M:%S') for _ in range(num_linhas)]
    
    # Gera os valores de 'count'
    counts = np.random.randint(1, 101, size=num_linhas)
    
    # Gera os nomes
    names = [''.join(random.choices(string.ascii_letters, k=random.randint(1, 20))) for _ in range(num_linhas)]
    
    # Gera o conteúdo com 20 palavras aleatórias
    contents = [gerar_conteudo_com_palavras_aleatorias(20) for _ in range(num_linhas)]

    dados = {
        'id': ids_unicos,
        'owner_id': owner_ids,
        'creation_date': creation_dates,
        'count': counts,
        'name': names,
        'content': contents
    }

    return pd.DataFrame(dados)

def criar_arquivo_csv(nome_arquivo, dados, separador=','):
    """Cria um arquivo CSV a partir dos dados fornecidos.

    Args:
        nome_arquivo (str): O nome do arquivo CSV a ser criado.
        dados (pandas.DataFrame): Os dados a serem escritos no arquivo CSV.
        separador (str): O separador a ser usado no arquivo CSV.
    """
    dados.to_csv(nome_arquivo, sep=separador, index=False)

# Exemplo de uso da função para criar um arquivo CSV com um ponto e vírgula como separador
nome_arquivo = './data/dados_gerados_big_4.csv'
num_linhas = 10000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)


nome_arquivo = './data/dados_gerados_big_5.csv'
num_linhas = 10000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_big_6.csv'
num_linhas = 10000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_big_7.csv'
num_linhas = 10000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_big_8.csv'
num_linhas = 10000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)


nome_arquivo = './data/dados_gerados_big_9.csv'
num_linhas = 10000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_big_10.csv'
num_linhas = 10000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_big_11.csv'
num_linhas = 10000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)




nome_arquivo = './data/dados_gerados_1.csv'
num_linhas = 1000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)


nome_arquivo = './data/dados_gerados_2.csv'
num_linhas = 1000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_3.csv'
num_linhas = 1000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)


nome_arquivo = './data/dados_gerados_4.csv'
num_linhas = 1000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)


nome_arquivo = './data/dados_gerados_5.csv'
num_linhas = 1000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_6.csv'
num_linhas = 1000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_7.csv'
num_linhas = 1000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_8.csv'
num_linhas = 1000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)


nome_arquivo = './data/dados_gerados_9.csv'
num_linhas = 1000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_10.csv'
num_linhas = 1000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_11.csv'
num_linhas = 1000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)



nome_arquivo = './data/dados_gerados_big_big_.csv'
num_linhas = 2000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_big_big_1.csv'
num_linhas = 2000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)

nome_arquivo = './data/dados_gerados_big_big_2.csv'
num_linhas = 2000
separador = ','

dados = gerar_dados(num_linhas)
criar_arquivo_csv(nome_arquivo, dados, separador)
