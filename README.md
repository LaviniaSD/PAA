# Projeto e Análise de Algoritmos

Este repositório oferece a lógica de negócios de um datagrid, proporcionando funções para busca, ordenação, inserção e deleção de eventos no datagrid.
O trabalho foi desenvolvido pelos alunos da FGV EMAp:

- **Almir Augusto Fonseca**
- **Lavínia Silva Dias**
- **George Dutra**
- **Isabela Yabe Martinez**

## Índice

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Como Usar](#como-usar)

## Visão Geral

O módulo inclui um relatório detalhado `relatorio.ipynb` (e também uma versão em PDF), que oferece análises das funções utilizadas e suas otimizações. O repositório é organizado nas seguintes pastas:

- `data`: Contém arquivos CSV gerados e utilizados nos testes e exemplos do código.
- `data_base2`: Contém arquivos CSV usados nos testes para as funções `select_count`.
- `results_select_count`: Armazena arquivos CSV pós-processados pela função `select_count`.
- `src`: Contém os arquivos essenciais para a geração de dados, criação do datagrid e suas funções auxiliares:
  - `analise_de_tempo.py` e `analise_de_tempo_teste.py` são usados para avaliar o desempenho em termos de tempo de execução das funções.
  - `analise_select_count.ipynb` é um notebook auxiliar para a análise de desempenho da função `select_count`.
  - `csv_maker` gera os CSV utilizados como exemplos.
  - `datagrid.py` é o arquivo principal que contém as classes `Event` e `Datagrid`, juntamente com seus métodos para inserção e remoção de dados, ordenação e busca. Para usar um datagrid, basta inicializá-lo como:
    ```
    datagrid = DataGrid()
    ````
  - `examples.py` oferece exemplos de como utilizar o datagrid e seus métodos internos.
  - `exceptions.py` contém a classe `InvalidColumnError`, uma exceção lançada quando a coluna referenciada é inválida em um método.
  - `timer.py` é utilizado para criar e testar o decorador `@timeit`, que mede o tempo de execução de cada função criada.
  - `utils.py` contém funções auxiliares para manipulação dos dados utilizados na classe datagrid.

Todas as funções em cada arquivo estão devidamente documentadas, e as principais estão referenciadas no relatório.

## Instalação

Para a instalação, basta clonar o repositório e executar o arquivo `requirements.txt` da seguinte forma:

```bash
pip install -r requirements.txt
```

## Como Usar

A utilização do projeto pode ser feita inteiramente através da importação do módulo e manipulação da classe `DataGrid`. Para melhor entendimento do módulo e suas aplicações, é recomendada a leitura do relatório no arquivo 'relatorio.ipynb', onde detalhes de cada função e comparações entre elas podem ser encontrados. Caso haja dúvidas sobre a utilização da classe `Datagrid`, o arquivo `examples.py` pode ser de grande serventia.
