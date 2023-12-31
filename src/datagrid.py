import sys

from exceptions import InvalidColumnError
from timer import timeit, get_execution_time
from utils import enumerated_alpha_numeric, enumerated_date, date_to_timestamp, string_lesser

sys.setrecursionlimit(10**6) 

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
            self.insertion_sort(column, direction, optimized)
        elif strategy == "selection_sort":
            self.selection_sort(column, direction, optimized)
        elif strategy == "merge_sort":
             self.merge_sort(column, direction, start = 0, end = None)
        elif strategy == "quick_sort":
            self.quick_sort(column, direction)
        elif strategy == "heap_sort":
            self.heap_sort(column, direction)
        elif strategy == "radix_sort":
            self.radix_sort(-1, column, direction)
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
            ordenada = True
            for i in range(self.size-1):
                if getattr(self.list[i],column) > getattr(self.list[i+1],column) and direction == "asc":
                    ordenada = False 
                elif getattr(self.list[i],column) < getattr(self.list[i+1],column) and direction == "desc":
                    ordenada = False                
            if ordenada:
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
        
            if compare(getattr(self.list[mid], column), value): start = mid+1
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
            value = date_to_timestamp(value[0]), date_to_timestamp(value[1]) 
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
                
                if cur_val < value[0]: start = mid+1
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
                
                if cur_val < value[1]: start = mid+1
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
                else: start = mid+1

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
                else: start = mid+1

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
            value = date_to_timestamp(value[0]), date_to_timestamp(value[1])
        
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
    
    def __median_of_medians(self, event_list):
        """Encontra o índice do elemento mediano de uma lista de eventos através do algoritmo de Median of Medians
        
        Args:
            event_list (list): lista de eventos a ser analisada

        Returns:
            Event: o elemento mediano
        """

        def __insertion_sort(event_list):
            """Ordena uma lista de eventos através do algoritmo de Insertion Sort
            
            Args:
                event_list (list): lista de eventos a ser ordenada
            """
            for i in range(1, len(event_list)):
                key = event_list[i]
                j = i-1
                while j >= 0 and key.count < event_list[j].count:
                    event_list[j+1] = event_list[j]
                    j -= 1
                event_list[j+1] = key

        # Caso o datagrid tenha tamanho <= 5, basta ordená-lo e retornar o índice do elemento mediano
        if len(event_list) <= 5:
            
            # Ordena a lista de eventos
            __insertion_sort(event_list)

            # Retorna o pivô como sendo o elemento mediano
            return event_list[len(event_list)//2]
        
        # Caso contrário, particiona o datagrid em grupos de 5 elementos e encontra o elemento mediano de cada grupo
        medians = []
        for i in range(0, len(event_list), 5):
            group = []
            for j in range(0,5):
                if i+j < len(event_list):
                    group.append(event_list[i+j])
            __insertion_sort(group)
            medians.append(group[len(group)//2])
        return self.__median_of_medians(medians)

    @timeit
    def __partition(self, low, high, pivot=None, strategy=None):
        """Particiona a lista de eventos, agrupando os eventos menores que o pivô, o pivô, e os eventos maiores que o pivô.
        
        Args:
            low (int): índice inicial do intervalo
            high (int): índice final do intervalo
            pivot (Event, optional): pivô da partição. Defaults to None.
            strategy (str, optional): estratégia de escolha do pivô. Defaults to None.

        Returns:
            int: índice do pivô
        """

        if not pivot:
            # Escolhe o pivô como o elemento mediano da lista de eventos
            if strategy == "quickselect_median_of_medians":

                # Caso a lista que seria passada tem pelo menos um elemento
                list_mom = self.list[low:high+1]
                if len(list_mom) > 0:
                    pivot = self.__median_of_medians(self.list[low:high+1])
                else:
                    # Por padrão, escolhe o último elemento do intervalo como pivô
                    pivot = self.list[high]

                # pivot = self.list[high]

            else:
                # Por padrão, escolhe o último elemento do intervalo como pivô
                pivot = self.list[high]

        # Computa as parcelas da lista menores, iguais ou maiores que o pivô
        lower_than_pivot = [x for x in self.list[low:high+1] if x.count < pivot.count]
        equal_to_pivot = [x for x in self.list[low:high+1] if x.count == pivot.count]
        greater_than_pivot = [x for x in self.list[low:high+1] if x.count > pivot.count]

        # Atualiza a lista de eventos, concatenando as parcelas na ordem correta
        self.list[low:high+1] = lower_than_pivot + equal_to_pivot + greater_than_pivot

        # Retorna o índice do pivô
        return low + len(lower_than_pivot)

    @timeit
    def __quickselect(self, low, high, k, strategy=None):
        """Encontra o k-ésimo menor elemento do DataGrid através do algoritmo de Quick Select
        
        Args:
            low (int): índice inicial do intervalo
            high (int): índice final do intervalo
            k (int): índice do elemento procurado
            strategy (str, optional): estratégia de escolha do pivô. Defaults to None.

        Returns:
            Event: k-ésimo menor elemento do DataGrid
        """

        # Particiona o intervalo
        pivot_index = self.__partition(low, high, strategy=strategy)

        # Se o índice do pivô for igual ao índice do elemento procurado, retorna o pivô
        if pivot_index == k:
            return self.list[pivot_index]

        # Se o índice do pivô for maior que o índice do elemento procurado, chama a função recursivamente para o intervalo à esquerda do pivô
        elif pivot_index > k:
            return self.__quickselect(low, pivot_index-1, k, strategy=strategy)

        # Se o índice do pivô for menor que o índice do elemento procurado, chama a função recursivamente para o intervalo à direita do pivô
        else:
            return self.__quickselect(pivot_index+1, high, k, strategy=strategy)

    @timeit
    def select_count(self, i, j, strategy="order_and_select"):
        """Seleciona um intervalo de entradas do DataGrid com base na coluna count ordenada de forma crescente.

        Args:
            i (int): índice inicial do intervalo
            j (int): índice final do intervalo
            strategy (str, optional): Estratégia de seleção. Defaults to "order_and_select".

        Returns:
            DataGrid: Novo DataGrid contendo os Events que correspondem ao intervalo.
        """

        # Cria uma cópia do datagrid (para não alterar o original)
        datagrid_copy = self.copy()

        # Caso o datagrid já esteja ordenado pela coluna count, basta selecionar o intervalo desejado
        if self.ordered_by == "count":

            # Caso esteja ordenado de forma ascendente, basta selecionar o intervalo
            if self.direction == "asc":
                datagrid_copy.list = datagrid_copy.list[i:j+1]

            # Caso esteja ordenado de forma descendente, é necessário inverter a ordem do intervalo
            else:
                # Inverte a ordem do datagrid
                datagrid_copy.list = datagrid_copy.list[::-1]
                # Seleciona o intervalo
                datagrid_copy.list = datagrid_copy.list[i:j+1]
                

            # Atualiza o tamanho do datagrid
            datagrid_copy.size = j - i + 1

            return datagrid_copy
    
        # Caso contrário, é necessário aplicar alguma das estratégias
        else:

            # Ordena o datagrid e seleciona o intervalo 
            if strategy == "order_and_select":

                # Ordena o datagrid
                datagrid_copy.sort("count", "asc")

                # Seleciona o intervalo chamando a função recursivamente
                return datagrid_copy.select_count(i, j)
            
            # Aplica o algoritmo de quickselect para selecionar o intervalo
            elif strategy == "quickselect" or strategy == "quickselect_median_of_medians":
    
                # Encontra o i-esimo menor elemento do datagrid usando QuickSelect
                ith_event = datagrid_copy.__quickselect(0, datagrid_copy.size-1, i, strategy=strategy)
                # Particiona o vetor novamente
                ith_event_index = datagrid_copy.__partition(0, datagrid_copy.size-1, pivot=ith_event)
                # Remove da lista todos os elementos menores que o i-ésimo e atualiza o tamanho do datagrid
                datagrid_copy.list = datagrid_copy.list[ith_event_index:]
                datagrid_copy.size = len(datagrid_copy.list)

                # Encontra o j-esimo menor elemento do datagrid usando QuickSelect
                jth_event = datagrid_copy.__quickselect(0, datagrid_copy.size-1, j-i, strategy=strategy)
                # Particiona o vetor novamente
                jth_event_index = datagrid_copy.__partition(0, datagrid_copy.size-1, pivot=jth_event)
                # Remove da lista todos os elementos maiores que o j-ésimo e atualiza o tamanho do datagrid
                datagrid_copy.list = datagrid_copy.list[:jth_event_index+1]
                datagrid_copy.size = len(datagrid_copy.list)

                # Ordena o datagrid de forma ascendente de acordo com a coluna count
                datagrid_copy.sort("count", "asc")

                # Caso o datagrid final tenha mais do que o número esperado de elementos (j-i+1), remove os últimos elementos
                if datagrid_copy.size > j-i+1:
                    datagrid_copy.list = datagrid_copy.list[:j-i+1]
                    datagrid_copy.size = len(datagrid_copy.list)
                
                return datagrid_copy

            # Se nenhuma estratégia for escolhida, utiliza o quickselect
            else:
                return self.select_count(i, j, "quickselect")

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

