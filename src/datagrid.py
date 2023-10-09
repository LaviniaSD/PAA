import sys

from datetime import datetime

from exceptions import InvalidColumnError
from timer import timeit, get_execution_time

sys.setrecursionlimit(10**6) 

def enumerated_alpha_numeric(char):
    alpha_numeric = {
        "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16, "H": 17, "I": 18, "J": 19,
        "K": 20, "L": 21, "M": 22, "N": 23, "O": 24, "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29,
        "U": 30, "V": 31, "W": 32, "X": 33, "Y": 34, "Z": 35,
        "a": 36, "b": 37, "c": 38, "d": 39, "e": 40, "f": 41, "g": 42, "h": 43, "i": 44, "j": 45,
        "k": 46, "l": 47, "m": 48, "n": 49, "o": 50, "p": 51, "q": 52, "r": 53, "s": 54, "t": 55,
        "u": 56, "v": 57, "w": 58, "x": 59, "y": 60, "z": 61, " ": 62
    }   
    return alpha_numeric[char]
def enumerated_date(char):
    date_type = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, " ": 0, ":": 0, "/": 0}
    return date_type[char]

def date_to_timestamp(date_str):
    """Converte a data no padrão de um objeto Event para uma timestamp.

    Args:
        date_str (str): String padrão de um Event.creation_date

    Returns:
        float: Timestamp converted from passed string
    """
    dtime = datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
    return dtime.timestamp()

def string_lesser(str1, str2, lenght1, lenght2):
    """Verifica se a primeira string vem antes da segunda na "ordem alfabética".

    Args:
        str1 (str): Primeira string, que para retornar True deve vir antes da outra.
        str2 (str): Segunda string, que para retornar True deve vir após a outra.
        lenght1 (int): Size of first string.
        lenght2 (int): Size of second string.

    Returns:
        bool: True se 'str1 < str2'. False caso contrário
    """
    if lenght1 < lenght2: l = lenght1
    else: l = lenght2
    
    for i in range(l):
        if ord(str1[i]) < ord(str2[i]): return True
        if ord(str1[i]) > ord(str2[i]): return False
    
    if lenght1 < lenght2: return True
    return False

class DataGrid():
    """Objeto que armazena um datagrid de negócios
    """
    def __init__(self):
        """Inicializa um DataGrid vazio
        """
        self.list = []
        self.ordered_by = None
        self.direction = None
        self.size = 0

    @timeit
    def read_csv(self, filepath, separator=",",encoding="utf-8"):
        """Carrega os dados de um arquivo CSV para o DataGrid

        Args:
            filepath (str): caminho para o arquivo CSV
            separator (str, optional): separador do CSV. Defaults to ",".
            encoding (str, optional): codificação do arquivo. Defaults to "utf-8".
        
        """
        # Abrindo o arquivo CSV
        try:
            file = open(filepath, mode="r", encoding=encoding)

        except FileNotFoundError:
            print("Arquivo não encontrado. Por favor, verifique o caminho e tente novamente.")

        except OSError:
            print("Ocorreu um erro ao abrir o arquivo. Por favor, verifique o caminho e tente novamente.")

        except Exception as error:
            print("Ocorreu um erro inesperado ao abrir o arquivo. Por favor, verifique o caminho e tente novamente.")
            print("Erro:", error)

        else:
            key_row = 0
            keys = ['id', 'owner_id', 'creation_date', 'count', 'name', 'content']

            for row in file:
                # Verificando que não estamos no cabeçalho (linha com os nomes da coluna) do csv.
                if key_row != 0:
                    # Listando os elementos de cada linha.
                    row = row.split(separator)
                    # Retirando o "\n" no final do último elementod a lista.
                    row[-1] = row[-1].rstrip('\n')
                    
                    row_dict = dict()
                    field_index = 0
                    # Criando chaves valor do dicionário
                    for key in keys:
                        # Corrigindo o tipo de dado
                        if field_index == 0 or field_index == 3:
                            row_dict[key] = int(row[field_index])
                        else:
                            row_dict[key] = row[field_index]
                        
                        field_index += 1
                        
                    self.insert_row(row_dict)
                else:
                    # Caso estejamos no cabeçalho, avançe para a primeira linha de dados
                    key_row = 1
    @timeit
    def insert_row(self, row):
        """Insere uma linha no DataGrid

        Args:
            row (dict/Event): dicionário contendo dados de uma linha do DataGrid, com o nome das colunas como chaves, e as entradas do DataGrid como valores.
        """
        if type(row) != Event:
            event = Event(row)
        else:
            event = row
        self.list.append(event)
        self.size += 1
        self.ordered_by = None
        self.direction = None
    @timeit
    def delete_row(self, column, value):
        """Deleta uma linha do DataGrid

        Args:
            column (str): nome da coluna que será usada para encontrar o valor a ser deletado
            value (any): valor que será usado para encontrar a linha a ser deletada
        """
        new_list = []
        self.size = 0

        if column == "position":
            i = 0
            for event in self.list:
                if i != value:
                    new_list.append(event)
                    self.size += 1
                i += 1
        else:
            for event in self.list:
                if getattr(event, column) != value:
                    new_list.append(event)
                    self.size += 1
        
        self.list = new_list
    
    @timeit     
    def show(self, start=0, end=100):
        """Imprime o conteúdo do DataGrid (segundo o início e fim especificados)

        Args:
            start (int): índice inicial da impressão. 0, por padrão.
            end (int): índice final da impressão. 100, por padrão.
        """
        # Caso o índice inicial seja maior que o tamanho da lista, ou caso o índice inicial seja igual ao índice final, não há eventos para serem impressos
        if (start > self.size or start == end):
            print("Não há eventos para serem impressos")
            return

        # Imprime o cabeçalho da tabela
        print("\n{:<6} | {:<8} | {:<19} | {:<9} | {:<20} | {}".format("ID", "Owner ID", "Creation Date", "Count", "Name", "Content"))

        # Imprime uma linha de separação
        print("="*100)

        # Itera sobre as instâncias de Evento no DataGrid, imprimindo-as
        for event in self.list[start:end]:
            print("{:<6} | {:<8} | {:<19} | {:<9} | {:<20} | {}".format(event.id, event.owner_id, event.creation_date, event.count, event.name, event.content))

        # Imprime uma linha ao final da tabela
        print()
    
    @timeit
    def swap_row(self, row_1, row_2):
        """
        Troca duas linhas na lista do DataGrid com base nos índices fornecidos.

        Args:
            row_1 (int): O índice da primeira linha a ser trocada.
            row_2 (int): O índice da segunda linha a ser trocada.
        """
        # Verifica se os índices são válidos
        if 0 <= row_1 < len(self.list) and 0 <= row_2 < len(self.list):
            # Troca os elementos
            self.list[row_1], self.list[row_2] = self.list[row_2], self.list[row_1]
        else:
            print("Índices fora dos limites da lista")
        
        self.ordered_by = None 
    
    @timeit
    def sort(self, column="id", direction="asc", strategy="quick_sort", optimized = False):
        """
        Ordena o DataGrid usando o algoritmo de ordenação especificado.

        Args:
            column (str, optional): O nome da coluna pela qual o DataGrid será ordenado. Caso nenhuma coluna seja definida, ordena pela "id" (padrão)
            direction (str, optional): A direção da ordenação, "asc" para ascendente (padrão) ou "desc" para descendente.
            strategy (str, optional): O algoritmo de ordenação a ser utilizado, "quick_sort"(padrão), "insertion_sort", "selection_sort", "merge_sort", "heap_sort" ou "radix_sort".
        """

        if strategy == "insertion_sort":
            self.insertion_sort(column, direction, optimized = optimized)
        elif strategy == "selection_sort":
            self.selection_sort(column, direction, optimized = optimized)
        elif strategy == "merge_sort":
             self.merge_sort(column, direction, start = 0, end = None)
        elif strategy == "quick_sort":
            self.quick_sort(column, direction)
        elif strategy == "heap_sort":
            self.heap_sort(column, direction)
        elif strategy == "radix_sort":
            self.radix_sort(column, direction)
        else:
            print("Algoritmo de ordenação inválido")

    @timeit
    def insertion_sort(self, column="id", direction="asc", optimized = False):
        """
        Ordena um datagrid usando o algoritmo de ordenação por inserção.
            
        Na otimização do insertion sort fazemos a verificação da ordenação na coluna, caso esteja ordenado não é executado o algoritmo.
        Args:
            column (str, optional): O nome da coluna pela qual o datagrid será ordenado, "id" para ordenar na coluna ID.
            direction (str, optional): A direção da ordenação, "asc" para ascendente (padrão) ou "desc" para descendente.
            optimized (bool): Define a estratégia adotada pelo algoritmo, False (padrão).
        """
        if column == "owner_id" or column == "creation_date" or column == "name" or column  == "content":
            raise InvalidColumnError(column=column)
        if optimized:
            if self.ordered_by == column and self.direction == direction:
                return
            for i in self.size:
                if getattr(self.list[i],column) > getattr(self.list[i],column) and direction == "asc":
                    pass 
                elif getattr(self.list[i],column) < getattr(self.list[i],column) and direction == "desc":
                    pass 
                else:
                    self.ordered_by == column 
                    self.direction == direction
            if self.ordered_by == column and self.direction == direction:
                return
        # Tamanho da entrada
        n = self.size        
        # Ordenanado em ordem crescente
        # Iniciando loop externo
        for i in range(1,n):
            current_value = self.list[i]
            j = i-1
            # Iniciando loop interno
            if direction == "asc":
              while (getattr(self.list[j], column) > getattr(current_value, column)) and (j >= 0) :
                self.list[j+1] = self.list[j]
                # Atualizando j
                j -= 1
            elif direction == "desc":
              while (getattr(self.list[j], column) < getattr(current_value, column)) and (j >= 0) :
                self.list[j+1] = self.list[j]
                # Atualizando j
                j -= 1
            self.list[j+1] = current_value

        self.direction = direction
        self.ordered_by = column    

    @timeit
    def selection_sort(self, column="id", direction="asc", optimized = False):
        """
        Ordena o DataGrid usando o algoritmo de ordenação por seleção.

        Na otimização do selection sort acrescentamos um index a mais o max index, assim ele faz a troca do menor elemento e do maior elemento para sua posições corretas.
        Args:
            column (str, optional): O nome da coluna pela qual o DataGrid será ordenado, "id" para ordenar na coluna ID.
            direction (str, optional): A direção da ordenação, "asc" para ascendente (padrão) ou "desc" para descendente.
            optimized (bool, optional): (bool): Define a estratégia adotada pelo algoritmo, False (padrão). 
        """
        if column == "owner_id" or column == "creation_date" or column == "name" or column  == "content":
            raise InvalidColumnError(column=column)
        # Tamanho da entrada
        n = self.size
        # Iniciando loope externo
        for i in range(n-1):
            min_inx = i
            if optimized:
                cont = 1
                max_inx = i
            # Iniciando loop interno
            for j in range(i+1,n):
                if direction == "asc":
                    if getattr(self.list[j], column) < getattr(self.list[min_inx], column):
                        min_inx = j
                    elif optimized and getattr(self.list[j], column) > getattr(self.list[max_inx], column):
                        max_inx = j
                if direction == "desc":
                    if getattr(self.list[j], column) > getattr(self.list[min_inx], column):
                        min_inx = j
                    elif optimized and getattr(self.list[j], column) < getattr(self.list[min_inx], column):
                        max_inx = j
            # Realizar troca se necessário
            if i != min_inx:
                self.swap_row(i, min_inx) 
            if optimized:
                if i == max_inx:
                    max_inx = min_inx
                if i != max_inx: 
                    self.swap_row(j,max_inx)
                cont += 1
                n = n - 1
                if cont == self.size//2:
                    return

        self.direction = direction
        self.ordered_by = column
      
    @timeit
    def quick_sort(self, column="id", direction="asc"):
        """
        Ordena o DataGrid usando o algoritmo de ordenação quicksort.

        Args:
            column (str, optional): O nome da coluna pela qual o DataGrid será ordenado, "id" para ordenar na coluna ID.
            direction (str, optional): A direção da ordenação, "asc" para ascendente (padrão) ou "desc" para descendente.
        """
        if column == "owner_id" or column == "creation_date" or column == "name" or column  == "content":
            raise InvalidColumnError(column=column)

        # Tamanho da entrada
        def partition(low, high):
            """
            Particiona o DataGrid em duas partes, uma com valores menores que o pivô e outra com valores maiores que o pivô.
            
            Args:
                low (int): O índice inicial da partição.
                high (int): O índice final da partição.
            """
            # Pivô
            pivot = getattr(self.list[high], column)
            i = low - 1

            # Loop para percorrer a lista
            for j in range(low, high):
                # Se o elemento atual for menor que o pivô ou se a ordenação for decrescente e o elemento atual for maior que o pivô
                if direction == "asc" and getattr(self.list[j], column) <= pivot or \
                   direction == "desc" and getattr(self.list[j], column) >= pivot:
                    # Incrementa o índice do menor elemento
                    i = i + 1
                    # Troca os elementos
                    self.swap_row(i, j)
            # Troca o pivô com o elemento na posição correta    
            self.swap_row(i + 1, high)
            return i + 1
        
        # Função recursiva para ordenar o DataGrid
        def quick_sort_recursive(low, high):
            # Se o índice inicial for menor que o índice final
            if low < high:
                # pi é o índice de partição
                pi = partition(low, high)
                # Chamada recursiva para ordenar as partições                    
                quick_sort_recursive(low, pi - 1)
                quick_sort_recursive(pi + 1, high)

        n = self.size
        # Chamada inicial da função recursiva
        quick_sort_recursive(0, n - 1)

        self.direction = direction
        self.ordered_by = column
    
    @timeit
    def merge_sort(self, column, direction = "asc", start = 0, end = None):
        """Algoritmo merge_sort de complexidade O(n logn) para ordenar as linhas do DataGrid.

        Args:
            column (str): Nome da coluna que será usada para ordenação.
            direction (str, optional): Direção de ordenação, 'asc' para crescente, 'desc' para decrescente. Defaults to "asc".
            start (int, optional): Parâmetro para recursão. Índice de início da sublista a ser ordenada. Defaults to 0.
            end (_type_, optional): Parâmetro para recursão. Índice de fim da sublista a ser ordenada. Defaults to None.
        """
        if column == "owner_id" or column == "creation_date" or column == "name" or column  == "content":
            raise InvalidColumnError(column=column)
        # Define método de comparação segundo tipo da coluna e direção
        if direction == "asc": compare = lambda x, y: x < y
        else: compare = lambda x, y: x >= y
        
        # Define as divisões das sublistas
        if end == None: end = self.size - 1
        mid = int((end + start)/2)

        # Chamada recursiva para ordenar as sublistas
        if (mid - start) > 0: self.merge_sort(column, direction, start, mid)
        if (end - mid) > 0: self.merge_sort(column, direction, mid+1, end)
        
        temp_list = [] # Lista temporária auxiliar
        idx_left = start # Início da sublista esquerda
        idx_right = mid+1 # Início da sublista direita

        # Loop para merge das sublistas
        while idx_left <= mid and idx_right <= end:
            if compare(getattr(self.list[idx_left], column), getattr(self.list[idx_right], column)): 
                temp_list.append(self.list[idx_left])
                idx_left += 1
            else: 
                temp_list.append(self.list[idx_right])
                idx_right += 1
        
        # Se sobrou algo na esquerda
        while idx_left <= mid:
            temp_list.append(self.list[idx_left])
            idx_left += 1

        # Se sobrou algo na direita
        while idx_right <= end:
            temp_list.append(self.list[idx_right])
            idx_right += 1
        
        for i in range(start, end+1):
            self.list[i] = temp_list[i-start]

        self.direction = direction
        self.ordered_by = column
  
    @timeit    
    def heapfy_max(self, n, i, column):
        """
        Implementa a operação de heapify para um heap máximo.

        Args:
            n (int): O tamanho do heap.
            i (int): O índice do elemento a ser heapificado.
            column (str): O nome da coluna usada como critério para a ordenação.
        """
        if column == "owner_id" or column == "creation_date" or column == "name" or column  == "content":
            raise InvalidColumnError(column=column)
        inx = i
        left_inx = (i*2) + 1
        right_inx = (i*2) + 2
        # Descendo a árvore e comparando
        if (left_inx < n) and (getattr(self.list[left_inx], column) > getattr(self.list[inx], column)):
            inx = left_inx
        if (right_inx < n) and (getattr(self.list[right_inx], column) > getattr(self.list[inx], column)):
            inx = right_inx
        if inx != i:
            # Caso haja a necessidade de troca, troque o elemento com o nó filho
            self.swap_row(i, inx)
            # Faça a descidada novamente no nó filho
            self.heapfy_max(n, inx, column)
    
    @timeit
    def heapfy_min(self, n, i, column):
        """
        Implementa a operação de heapify para um heap mínimo.

        Args:
            n (int): O tamanho do heap.
            i (int): O índice do elemento a ser heapificado.
            column (str): O nome da coluna usada como critério para a ordenação.
        """
        inx = i
        left_inx = (i*2) + 1
        right_inx = (i*2) + 2
        # Descendo a árvore e comparando
        if (left_inx < n) and (getattr(self.list[left_inx], column) < getattr(self.list[inx], column)):
            inx = left_inx
        if (right_inx < n) and (getattr(self.list[right_inx], column) < getattr(self.list[inx], column)):
            inx = right_inx
        if inx != i:
            # Caso haja a necessidade de troca, troque o elemento com o nó filho
            self.swap_row(i, inx)
            # Faça a descidada novamente no nó filho
            self.heapfy_min(n, inx, column)
    
    @timeit
    def build_heap(self, n, column, type_heap="max"):
        """
        Constrói um heap a partir de um DataGrid.

        Args:
            n (int): O tamanho do heap.
            column (str): O nome da coluna usada como critério para a ordenação.
            type_heap (str, optional): O tipo de heap a ser construído, "max" para heap máximo (padrão) ou "min" para heap mínimo.

        Returns:
            None
        """
        # Faça a alocação correta até a penúltima altura da árvore
        for i in range((n//2)-1,-1,-1):
            if type_heap == "max":
                self.heapfy_max(n, i, column)
            elif type_heap == "min":
                self.heapfy_min(n, i, column)
    
    @timeit
    def heap_sort(self, column = "id", direction="asc"):
        """
        Ordena um DataGrid usando o algoritmo Heap Sort.

        Args:
            n (int): O tamanho da entrada.
            column (str, optional): O nome da coluna usada como critério para a ordenação, "id" para ordenar na coluna ID..
            direction (str, optional): A direção da ordenação, "asc" para ascendente (padrão) ou "desc" para descendente.
        """
        n = self.size
        if direction == "asc":
            # Construindo heap
            self.build_heap(n, column, "max")
        elif direction == "desc":
            self.build_heap(n, column, "min")
        for i in range(n-1,0,-1):
            # Ordene pela raiz da árvore
            self.swap_row(0,i)
            # Refaça o heap sem a raiz, ela foi jogada para o fim da lista e está ordenada
            if direction == "asc":
                self.heapfy_max(i, 0, column)
            elif direction == "desc":
                self.heapfy_min(i, 0, column)
        self.ordered_by = column
        self.direction = direction

    @timeit
    def radix_sort(self, lim = -1, column="owner_id", direction="asc", pos=0, type_code="ASCII", start=0, end=-1):
        """
        Ordena o DataGrid usando o algoritmo de ordenação Radix Sort.

        Args:
            pos (int): A posição do caractere a ser considerado durante a ordenação.
            lim (int, optinal): O número de caracteres a serem considerados durante a ordenação.
            column (str): O nome da coluna pela qual o DataGrid será ordenado.
            type_code (str, optional): O tipo de enumeração que será usada para cara char, padrão ASCII.
            start (int, optional): O índice inicial para a ordenação (padrão é 0).
            end (int, optional): O índice final para a ordenação (padrão é -1, indicando o final da lista).
            direction (str, optional): A direção da ordenação, "asc" para ascendente (padrão) ou "desc" para descendente.
            not_sort (bool): Boleano para lista na coluna ordenada ou não, (padrão) True, ou seja não está ordenada. 
        """
        if column == "id" or column == "count" or column == "timestamp":
            raise InvalidColumnError(column=column)
        # Padrão para enumeração de char
        if column == "owner_id":
            type_code = "alphanumeric"
  
        if column == "creation_date":
            type_code = "date_type"

        # Verificando se o lim foi está de acordo
        if  lim <= -1 or lim > 0:
            # Num de char
            if type_code == "ASCII":
                type_code_size = 128 
            elif type_code == "alphanumeric":
                type_code_size = 63
            elif type_code == "date_type":
                type_code_size = 13
            # Se não for dado o fim do datagrid, fazer o fim a última linha
            if end == -1:
                end = self.size
            # Número de caracteres no padrão type_code, fs inicialmente guarda a frequência de elementos
            # o elemento de valor n, é informado sua frequência na n+1-ésima entrada da lista fs
            fs = [0] * (type_code_size + 1)
            # Lista temporaria para inserir os valores ordenados
            temp = [0] * (self.size)
            n = end-start # Palavras no slice
            cont = 0 # Num de palavras que foram acrescentados " "
            for i in range(start, end):
                # Caso uma palavra não conter char na posição pos
                try:
                    getattr(self.list[i], column)[pos]
                except IndexError:
                    palavra_atual = getattr(self.list[i], column)
                    # Adiciona um espaço ao final da palavra se necessário
                    if len(palavra_atual) < pos + 1:
                        setattr(self.list[i], column, palavra_atual + " ")
                        # Aumenta 1 na palavra modificada
                        cont += 1
                if cont == n: #Parando de fazer comparações, caso acrescentarmos " " em todas palavras no slice
                    return
                # Guardando caractere com seu valor sendo index+1, o valor no vetor é a frequência em que ele aparece na pos atual
                if direction == "asc" and type_code == "ASCII": 
                    fs[ord(getattr(self.list[i], column)[pos]) + 1] += 1
                elif direction == "asc" and type_code == "alphanumeric": 
                    fs[enumerated_alpha_numeric(getattr(self.list[i], column)[pos]) + 1] += 1
                elif direction == "asc" and type_code == "date_type": 
                    fs[enumerated_date(getattr(self.list[i], column)[pos]) + 1] += 1
                # No caso de descrescente só invertemos os valores de cada char
                elif direction == "desc" and type_code == "ASCII":
                    fs[type_code_size - 1 - ord(getattr(self.list[i], column)[pos]) + 1] += 1
                elif direction == "desc" and type_code == "alphanumeric": 
                    fs[type_code_size - 1 - enumerated_alpha_numeric(getattr(self.list[i], column)[pos]) + 1] += 1
                elif direction == "desc" and type_code == "date_type": 
                    fs[type_code_size - 1 - enumerated_date(getattr(self.list[i], column)[pos]) + 1] += 1
            # Guardando o elemento que repetiu (o elemento é sua posição - 1 no vetor fs) e quantas vezes ele repetiu
            # (quantas vezes ele repetiu é fs[sua pos])
            aux = []
            # Entrada 1 do vetor fs e última entrada do vetor fs, guarda apenas aqueles que se repete mais de uma vez
            for j in range(1,type_code_size + 1):
              # Se o caractere se repete
                if fs[j]>1:
                    aux.append([j-1, fs[j]])
            # Calculando onde cada elemento da lista começa e o espaço para guardar cada caractere 
            for j in range(1,type_code_size + 1):
                fs[j]+=fs[j-1]
            # Agora nosso fs guarda onde cada elemento (char valor num = j) vai começar (começa ser posto fs[j])
            # Inicio da realocação de elementos, É AQUI QUE NÃO MUDAMOS OS ELEMENTOS JÁ MUDADOS ANTERIORMENTE!!!
            for i in range(start,end):#por causa do start e end!!!!
                if i == start:
                # Inicio da resursão, onde o elemento que contém mais de uma repetição começa
                    aux_start=[] # Guardando os starts das recursões, vamos aplicar a recursão só nos elementos repetidos, na pos+1 
                    for k in aux:
                        aux_start.append(fs[k[0]] + start) # k[0] é o valor do elemento, logo fs[k[0]] é onde ele começa
                # Realocando elemento j
                # Guardando caractere com seu valor numérico
                if direction == "asc" and type_code == "ASCII": 
                    j = ord(getattr(self.list[i], column)[pos])
                elif direction == "asc" and type_code == "alphanumeric": 
                    j = enumerated_alpha_numeric(getattr(self.list[i], column)[pos])
                elif direction == "asc" and type_code == "date_type": 
                    j = enumerated_date(getattr(self.list[i], column)[pos])
                elif direction == "desc" and type_code == "ASCII": 
                    j = type_code_size  -1 - ord(getattr(self.list[i], column)[pos])
                elif direction == "desc" and type_code == "alphanumeric": 
                    j = type_code_size -1 - enumerated_alpha_numeric(getattr(self.list[i], column)[pos])
                elif direction == "desc" and type_code == "date_type": 
                    j = type_code_size -1 - enumerated_date(getattr(self.list[i], column)[pos])
                # Guardando vetor na posição correta
                temp[fs[j] + start] = self.list[i]
                # Somando mais 1 para o vetor ser posto no lado direito
                fs[j] += 1 # Realocando onde o próximo valor j vai entrar na lista
            for i in range(start,end):
                if self.list[i] != temp[i]:
                    # Realocando na lista original
                    self.list[i] = temp[i]
            # Se tiver caracteres repetidos na posição
            if len(aux) != 0:
                for k in range(len(aux)):
                    # Fazemos um "Slice", para alterarmos vendo a pos+1 em apenas partes com caracteres repetidos
                    # Note que dessa forma, se os primeiros caracteres forem todos diferente, a excecusão é O(n)
                    self.radix_sort(lim -1, column, direction, pos+1, type_code, aux_start[k], aux_start[k] + aux[k][1])
        self.ordered_by = column
        self.direction = direction

    @timeit
    def __exact_binary_search(self, column, value):
        """Busca binária para valores de 'id' ou 'owner_id' de objetos Event.
        Método auxiliar a __exact_search().

        Args:
            column (str): Nome da coluna que está sendo buscada.
            value (int): Valor procurado.

        Returns:
            int | None: Índice do evento correspondente ao valor buscado no DataGrid, ou None se não existe.
        """
        if self.direction == "asc":
            if column == "id": compare = lambda x, y: x < y
            else: compare = lambda x, y: string_lesser(x, y, len(x), len(y))
        elif self.direction == "desc":
            if column == "id": compare = lambda x, y: x > y
            else: compare = lambda x, y: not string_lesser(x, y, len(x), len(y))

        start = 0
        end = self.size - 1
        mid = int(end/2)

        while start != end: 
            if getattr(self.list[mid], column) == value: return mid # Foi encontrado
        
            if compare(getattr(self.list[mid], column), value): start = mid
            else: end = mid

            mid = int(start + (end - start)/2)
            
        if getattr(self.list[mid], column) == value: return mid
        return None # Não foi encontrado
    
    @timeit
    def __exact_search(self, column, value, optimized):
        """Busca por valores exatos no DataGrid.
        Método auxiliar a search().

        Args:
            column (str): Nome da coluna que está sendo buscada.
            value (int | str): Valor procurado.
            optimized (bool): Define a estratégia adotada pelo algoritmo.

        Returns:
            int | None: Índice do evento correspondente ao valor buscado no DataGrid, ou None se não existe.
        """
        # Se estiver ordenado pela coluna que estamos buscando, implementa a binary search
        if self.ordered_by == column and optimized:
            return self.__exact_binary_search(column, value)

        # Se não, faça busca linear
        for idx in range(self.size):
            if getattr(self.list[idx], column) == value:
                return idx
        
        return None # Pior caso: não foi encontrado
    
    @timeit
    def __interval_binary_search(self, column, value):
        """Busca binária para valores pertencentes a um intervalo no DataGrid.
        Método auxiliar de __interval_search().

        Args:
            column (str): Nome da coluna que está sendo buscada.
            value (tuple): Tupla com valores de início e fim do intervalo desejado, ambos inclusive.

        Returns:
            list: Lista de índices dos elementos do DataGrid que pertencem ao intervalo desejado.
        """
        # Se procurar por data, usa timestamp ao invés da string
        if column == "creation_date": 
            column = "timestamp"
            value[0], value[1] = date_to_timestamp(value[0]), date_to_timestamp(value[1]) 
        
        start = 0
        end = self.size - 1
        mid = int(end/2)
        
        if self.direction == "asc":
            # Loop para encontrar o limite inferior
            while start != end: 
                cur_val = getattr(self.list[mid], column)

                # Se encontramos exatamente o limite inferior do intervalo, garantimos que abrangimos todas as suas duplicatas e quebramos o loop
                if cur_val == value[0]: 
                    while getattr(self.list[mid-1], column) == value[0]: mid -= 1
                    break
                
                if cur_val < value[0]: start = mid
                else: end = mid

                mid = int(start + (end - start)/2)

            if getattr(self.list[mid], column) < value[0]: mid += 1
            if getattr(self.list[mid], column) > value[1]: return [] # Caso em que o intervalo não existe

            # Nesse momento, mid é o índice do primeiro elemento do grid que pertence ao intervalo
            first = mid

            start = first # Não precisamos procurar o limite superior do intervalo antes do inferior
            end = self.size - 1
            mid = int((end+start)/2)

            # Loop para encontrar o limite superior
            while start != end:
                cur_val = getattr(self.list[mid], column)

                # Se encontramos exatamente o limite superior do intervalo, garantimos que abrangimos todas as suas duplicatas e quebramos o loop
                if cur_val == value[1]: 
                    while getattr(self.list[mid+1], column) == value[1]: mid += 1
                    break
                
                if cur_val < value[1]: start = mid
                else: end = mid

                mid = int(start + (end - start)/2)

            if getattr(self.list[mid], column) > value[1]: mid -= 1
            # Nesse momento, mid é o índice do último elemento do grid que pertence ao intervalo
            last = mid
            return range(first, last+1)

        elif self.direction == "desc":
            # Loop para encontrar o limite inferior
            while start != end: 
                cur_val = getattr(self.list[mid], column)

                # Se encontramos exatamente o limite inferior do intervalo, garantimos que abrangimos todas as suas duplicatas e quebramos o loop
                if cur_val == value[0]: 
                    while getattr(self.list[mid-1], column) == value[0]: mid += 1
                    break
                
                if cur_val < value[0]: end = mid
                else: start = mid

                mid = int(start + (end - start)/2)

            if getattr(self.list[mid], column) < value[0]: mid -= 1
            if getattr(self.list[mid], column) > value[1]: return [] # Caso em que o intervalo não existe

            # Nesse momento, mid é o índice do último elemento do grid que pertence ao intervalo
            first = mid

            start = 0 
            end = first # Não precisamos procurar o limite superior do intervalo depois do inferior
            mid = int((end+start)/2)

            # Loop para encontrar o limite superior
            while start != end:
                cur_val = getattr(self.list[mid], column)

                # Se encontramos exatamente o limite superior do intervalo, garantimos que abrangimos todas as suas duplicatas e quebramos o loop
                if cur_val == value[1]: 
                    while getattr(self.list[mid+1], column) == value[1]: mid -= 1
                    break
                
                if cur_val < value[1]: end = mid
                else: start = mid

                mid = int(start + (end - start)/2)

            if getattr(self.list[mid], column) > value[1]: mid += 1
            # Nesse momento, mid é o índice do último elemento do grid que pertence ao intervalo
            last = mid
            return range(last, first+1)
    
    @timeit
    def __interval_search(self, column, value, optimized):
        """Busca de valores pertencentes a um intervalo no DataGrid.
        Método auxiliar de search().

        Args:
            column (str): Nome da coluna que está sendo buscada.
            value (tuple): Tupla com valores de início e fim do intervalo desejado, ambos inclusive.
            optimized (bool): Define a estratégia adotada pelo algoritmo.

        Returns:
            list: Lista de índices dos elementos do DataGrid que pertencem ao intervalo desejado.
        """
        # Busca binária caso esteja ordenado
        if self.ordered_by == column and optimized:
            return self.__interval_binary_search(column, value)
        
        # Se procurar por data, usa timestamp ao invés da string
        if column == "creation_date": 
            column = "timestamp"
            value = (date_to_timestamp(value[0]), date_to_timestamp(value[1])) 
        
        start, end = value        
        result = []
        for idx in range(self.size):
            cur_val = getattr(self.list[idx], column)
            if cur_val >= start and cur_val <= end:
                result.append(idx)
        return result
    
    @timeit
    def __contain(self, str1, str2, str2_len):
        """Verifica se a string str1 contém str2.

        Args:
            str1 (str): String que deve conter a outra.
            str2 (str): String que deve estar contida na outra.
            str2_len (int): Tamanho da str2.

        Returns:
            bool: True se str1 conter str2, False caso contrário.
        """
        matches = 0
        for i in range(len(str1)):
            if str1[i] == str2[matches]:
                matches += 1
            else:
                matches = 0
            
            if matches == str2_len: 
                return True
        return False
    
    @timeit
    def __contain_search(self, column, value):
        """Busca por Events cujas entradas contenham o value passado.

        Args:
            column (str): Nome da coluna que está sendo buscada.
            value (str): Valor que deverá estar contido na entrada da coluna passada.
            optimized (bool): Define a estratégia adotada pelo algoritmo.

        Returns:
            list: Lista de índices dos Events cujas entradas contêm o valor passado na coluna passada.
        """
        lenght = len(value)     
        result = []

        for idx in range(self.size):
            if self.__contain(getattr(self.list[idx], column), value, lenght):
                result.append(idx)
        return result

    @timeit
    def search(self, column, value, optimized = True):
        """Busca pelo valor desejado na coluna desejada.

        Args:
            column (str): Nome da coluna onde será realizada a busca.
            value (int | str | tuple): Valor que será buscado na coluna passada. O tipo do parâmetro deve ser coerente com o tipo de busca da coluna passada.
            optimized (bool, optional): Define a estratégia adotada pelo algoritmo. Por padrão, verifica se o DataGrid está ordenado na coluna pedida e aplica 
            uma busca binária em caso afirmativo. Se for falso, esse parâmetro força a busca a ser sempre linear. Defaults to True. 

        Returns:
            DataGrid: Novo DataGrid contendo os Events que correspondem à busca. 
        """
        result = DataGrid() 

        # Busca exata
        if column == "id" or column == "owner_id":
            idx = self.__exact_search(column, value, optimized)
            
            if idx != None: 
                result.list.append(self.list[idx])
                result.size += 1
            
        # Busca por intervalo
        elif column == "creation_date" or column == "count":
            idx_list = self.__interval_search(column, value, optimized)
            
            for i in idx_list:
                result.list.append(self.list[i])
                result.size += 1
        
        # Busca por conteúdo
        elif column == "name" or column == "content":
            idx_list = self.__contain_search(column, value)
            
            for i in idx_list:
                result.list.append(self.list[i])
                result.size += 1

        return result

    @timeit
    def copy(self):
        """Produz uma deep copy do datagrid       
        """
        new_datagrid = DataGrid()

        # Copia a lista de eventos
        new_datagrid.list = self.list.copy()

        # Copia os atributos
        new_datagrid.ordered_by = self.ordered_by
        new_datagrid.direction = self.direction
        new_datagrid.size = self.size

        return new_datagrid
    
    # TODO: implementar o MOM de acordo com a função sort (a partir do momento q ela reconhecer o melhor algoritmo para cada ordenação)

    @timeit
    def __quick_select(self, datagrid, l, r, k):
        """Encontra o k-ésimo menor elemento do DataGrid através do algoritmo de Quick Select
        
        Args:
            datagrid (DataGrid): DataGrid a ser analisado
            l (int): índice inicial do intervalo
            r (int): índice final do intervalo
            k (int): índice do elemento procurado
        """
        
        # Caso base
        if l == r:
            return datagrid.list[l]
        
        # Particiona o vetor
        pivot = datagrid.list[l]
        i = l
        j = r
        while i < j:
            while datagrid.list[i].count <= pivot.count and i < r:
                i += 1
            while datagrid.list[j].count > pivot.count and j > l:
                j -= 1
            if i < j:
                datagrid.swap_row(i, j)
        datagrid.swap_row(l, j)

        # Verifica se o elemento procurado é o pivô
        if k == j:
            return datagrid.list[j]
        
        # Verifica se o elemento procurado está à esquerda do pivô
        elif k < j:
            return self.__quick_select(datagrid, l, j-1, k)
        
        # Verifica se o elemento procurado está à direita do pivô
        else:
            return self.__quick_select(datagrid, j+1, r, k)
        
    @timeit
    def select_count(self, i, j):
        """Seleciona um intervalo de entradas do DataGrid com base na coluna count ordenada de forma crescente.

        Args:
            i (int): índice inicial do intervalo
            j (int): índice final do intervalo
        """

        # Caso o datagrid esteja ordenado, basta retornar o intervalo entre a i-ésima e a j-ésima entrada
        if self.ordered_by == "Count":

            datagrid_selected = DataGrid()

            if self.direction == "asc":
                datagrid_selected.list = self.list[i:j+1]
            else:
                datagrid_selected.list = self.list[self.size-(i)-1 : self.size-(j+1)-1 : -1]

            return datagrid_selected
        
        # Caso contrário, usamos quickselect para encontrar o i-ésimo e o j-ésimo menor elemento
        else:
            # Cria uma cópia do datagrid (para preservar o estado interno da estrutura de dados)
            datagrid_copy = self.copy()

            # Encontra o i-ésimo e o j-ésimo menor elemento
            i_min = self.__quick_select(datagrid_copy, 0, len(datagrid_copy.list)-1, i)
            j_min = self.__quick_select(datagrid_copy, 0, len(datagrid_copy.list)-1, j)

            # Encontra o intervalo entre os dois elementos
            datagrid_copy.list = datagrid_copy.list[datagrid_copy.list.index(i_min):datagrid_copy.list.index(j_min)+1]

            # Retorna o datagrid apenas com o intervalo entre os dois elementos
            return datagrid_copy

class Event():
    """Objeto que armazena uma linha de um DataGrid
    """
    def __init__(self, dict = None, **kwargs):
        """Inicializa um evento a partir dos dados passados nominalmente, através de um dicionário ou diretamente com keyword arguments 
   
        Args:
            dict (dict, optional): dicionário contendo dados de uma linha do DataGrid, com o nome das colunas como chaves, e as entradas do DataGrid como valores. Defaults to None.
        """
        if dict == None: dict = kwargs
        
        self.id = dict["id"]
        self.owner_id = dict["owner_id"]
        self.creation_date = dict["creation_date"]
        self.count = dict["count"]
        self.name = dict["name"]
        self.content = dict["content"]

        # Coluna oculta para fins de ordenação
        self.timestamp = date_to_timestamp(self.creation_date)

if __name__ == "__main__":
     # Criar uma instância de DataGrid
    datagrid = DataGrid()

    # Inserir evento com base em dicionário de tuplas
    data_dict = {
        "id": 1,
        "owner_id": "ab123",
        "creation_date": "2023/09/26 14:00:00",
        "count": 43,
        "name": "Evento 1",
        "content": "Conteúdo do Evento 1"
    }
    datagrid.insert_row(data_dict)

    # Inserir outro evento com base em dicionário de tuplas
    data_dict2 = {
        "id": 2,
        "owner_id": "ac124",
        "creation_date": "2023/09/26 15:25:32",
        "count": 25,
        "name": "Evento 2",
        "content": "Conteúdo do Evento 2"
    }
    datagrid.insert_row(data_dict2)

    # Verificar o conteúdo do DataGrid
    datagrid.show()

    print("Após trocar linha 1 com linha 2")
    # Trocar linha 1 com linha 2
    datagrid.swap_row(0,1)

    datagrid.show()

    print("Ordenando DataGrid pela coluna ID com Insertion Sort")
    datagrid.insertion_sort("id")

    datagrid.show()

    print("Ordenando de forma decrescente DataGrid pela coluna ID com Selection Sort")
    datagrid.selection_sort("id", "desc")

    datagrid.show()
    
    print("Após deletar o evento 2 pela sua posição")

    # Deletar um evento
    datagrid.delete_row("position", 0)

    # Verificar o conteúdo do DataGrid
    datagrid.show()

    print("Reinserindo evento 2 e buscando pelo evento 1")
    
    # Buscar por elemento
    datagrid.insert_row(data_dict2)
    datagrid.search("id", 1).show()
    datagrid.search("owner_id", "ab123").show()

    print("Buscando por conteúdo")
    
    # Buscar por strings que contém outra    
    datagrid.search("content", "Conteúdo").show()
    datagrid.search("name", "2").show()

    print("Buscando por count entre 25 e 43")
    
    # Buscar por intervalo    
    datagrid.search("count", (25,43)).show()
    
    print("Buscando por data entre 2023/09/26 14:00:01 e 2023/09/26 17:00:00")
    
    # Buscar por intervalo
    datagrid.search("creation_date", ("2023/09/26 14:00:01", "2023/09/26 17:00:00")).show()

    # Carregando dados a partir de um CSV
    datagrid_csv = DataGrid()
    datagrid_csv.read_csv("data/dados_gerados.csv", ";")
    datagrid_csv.show()

    print("select_count(2, 5) para um vetor não ordenado")
    print(f"Ordenação: {datagrid_csv.ordered_by}")
    # datagrid_csv.select_count(2, 5).show()
    datagrid_csv.select_count(2, 5)
    
    get_execution_time("select_count", True)

    print("select_count(2, 5) para um vetor ordenado (asc)")
    datagrid_csv.insertion_sort("Count")
    print(f"Ordenação: {datagrid_csv.ordered_by} ({datagrid_csv.direction})")
    # datagrid_csv.select_count(2, 5).show()
    datagrid_csv.select_count(2, 5)
    
    get_execution_time("select_count", True)

    print("select_count(2, 5) para um vetor ordenado (desc)")
    datagrid_csv.insertion_sort("Count", "desc")
    print(f"Ordenação: {datagrid_csv.ordered_by} ({datagrid_csv.direction})")
    # datagrid_csv.select_count(2, 5).show()
    datagrid_csv.select_count(2, 5)
    
    get_execution_time("select_count", True)

    # TODO: implementar o decorador @timeit para as demais funções após discutir os métodos que receberão o decorador

    print("Teste merge_sort por ID")
    datagrid_csv.merge_sort("id")
    print("Ordenação:", datagrid_csv.ordered_by)
    datagrid_csv.show()

    print("Teste merge_sort por Owner ID")
    datagrid_csv.merge_sort("owner_id")
    print("Ordenação:", datagrid_csv.ordered_by)
    datagrid_csv.show()

    print("Teste merge_sort desc por creation_date")
    datagrid_csv.merge_sort("creation_date", "desc")
    print("Ordenação:", datagrid_csv.ordered_by)
    datagrid_csv.show()
