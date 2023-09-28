from datetime import datetime

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
        self.size = 0

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

    def insert_row(self, row):
        """Insere uma linha no DataGrid

        Args:
            row (dict): dicionário contendo dados de uma linha do DataGrid, com o nome das colunas como chaves, e as entradas do DataGrid como valores.
        """
        event = Event(**row)
        self.list.append(event)
        self.size += 1
        self.ordered_by = None
    
    def delete_row(self, column, value,method=None):
        """Deleta uma linha do DataGrid

        Args:
            column (str): nome da coluna que será usada para encontrar o valor a ser deletado
            value (any): valor que será usado para encontrar a linha a ser deletada
        """
        new_list = []
        self.size = 0

        if method == "position":
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
        
        if self.ordered_by: self.ordered_by = None 

    def insertion_sort(self, column="ID", direction="asc"):
        """
        Ordena um datagrid usando o algoritmo de ordenação por inserção.

        Args:
            column (str): O nome da coluna pela qual o datagrid será ordenado.
            direction (str, optional): A direção da ordenação, "asc" para ascendente (padrão) ou "desc" para descendente.
        """
        # Tamanho da entrada
        n = self.size
        # Ordenanado em ordem crescente
        if direction == "asc":
            # Iniciando loop externo
            for i in range(1,n):
                current_value = self.list[i]
                j = i-1
                # Iniciando loop interno
                if column == "ID":    
                    while (self.list[j].id > current_value.id) and (j >= 0) :
                        self.list[j+1] = self.list[j]
                        # Atualizando j
                        j -= 1
                elif column == "Count":
                    while (self.list[j].count > current_value.count) and (j >= 0) :
                        self.list[j+1] = self.list[j]
                        # Atualizando j
                        j -= 1
                self.list[j+1] = current_value
        # Ordenanado em ordem decrescente
        elif direction == "desc":
            # Iniciando loop externo
            for i in range(1,n):
                current_value = self.list[i]
                j = i-1
                # Iniciando loop interno
                if column == "ID":    
                    while (self.list[j].id < current_value.id) and (j >= 0) :
                        self.list[j+1] = self.list[j]
                        # Atualizando j
                        j -= 1
                elif column == "Count":
                    while (self.list[j].count < current_value.count) and (j >= 0) :
                        self.list[j+1] = self.list[j]
                        # Atualizando j
                        j -= 1
                self.list[j+1] = current_value
        self.ordered_by = column
    
    def selection_sort(self, column="ID", direction="asc"):
        """
        Ordena o DataGrid usando o algoritmo de ordenação por seleção.

        Args:
            column (str): O nome da coluna pela qual o DataGrid será ordenado.
            direction (str, optional): A direção da ordenação, "asc" para ascendente (padrão) ou "desc" para descendente.
        """
        # Tamanho da entrada
        n = self.size
        # Ordenando em ordem crescente
        if direction == "asc":
            # Iniciando loop externo
            for i in range(n-1):
                min_inx = i
                # Iniciando loop interno
                for j in range(i+1,n):
                    if column == "ID":
                        if self.list[j].id < self.list[min_inx].id:
                            min_inx = j
                    elif column == "Count":
                        if self.list[j].count < self.list[min_inx].count:
                            min_inx = j
                self.swap_row(i, min_inx)
        # Ordenando em ordem decrescente
        if direction == "desc":
            # Iniciando loop externo
            for i in range(n-1):
                max_inx = i
                # Iniciando loop interno
                for j in range(i+1,n):
                    if column == "ID":
                        if self.list[j].id > self.list[max_inx].id:
                            max_inx = j
                    elif column == "Count":
                        if self.list[j].count > self.list[max_inx].count:
                            max_inx = j
                self.swap_row(i, max_inx)     
        self.ordered_by = column

    # def __quick_sort(self, column, direction="asc")
            #int

    # def __merge_sort(self, column, direction="asc")
            #

    # def __radix_sort(self, column, direction="asc") 
            #owner

    # def __radix_sort_2(self, column, direction="asc")
            #name, content

    # def __radix_sort_3(self, column, direction="asc")
            #date
    def heapfy_max(self, n, i, column="ID"):
        inx = i
        left_inx = (i*2) + 1
        right_inx = (i*2) + 2
        if column == "ID":
            if (left_inx < n) and (self.list[left_inx].id > self.list[inx].id):
                inx = left_inx
            if (right_inx < n) and (self.list[right_inx].id > self.list[inx].id):
                inx = right_inx
        elif column == "Count":
            if (left_inx < n) and (self.list[left_inx].count > self.list[inx].count):
                inx = left_inx
            if (right_inx < n) and (self.list[right_inx].count > self.list[inx].count):
                inx = right_inx
        if inx != i:
            self.swap_row(i, inx)
            self.heapfy_max(n, inx, column)

    def heapfy_min(self, n, i, column="ID"):
        inx = i
        left_inx = (i*2) + 1
        right_inx = (i*2) + 2
        if column == "ID":
            if (left_inx < n) and (self.list[left_inx].id < self.list[inx].id):
                inx = left_inx
            if (right_inx < n) and (self.list[right_inx].id < self.list[inx].id):
                inx = right_inx
        elif column == "Count":
            if (left_inx < n) and (self.list[left_inx].count < self.list[inx].count):
                inx = left_inx
            if (right_inx < n) and (self.list[right_inx].count < self.list[inx].count):
                inx = right_inx
        if inx != i:
            self.swap_row(i, inx)
            self.heapfy_min(n, inx, column)
    
    def build_heap(self, n, column="ID", type_heap="max"):
        for i in range((n//2)-1,-1,-1):
            if type_heap == "max":
                self.heapfy_max(n, i, column)
            elif type_heap == "min":
                self.heapfy_min(n, i, column)

    def heap_sort(self, n, column="ID", direction="asc"):
        if direction == "asc":
            self.build_heap(n, column, "max")
        elif direction == "min":
            self.build_heap(n, column, "min")
        for i in range(n-1,0,-1):
            self.swap_row(0,i)
            if direction == "asc":
                self.heapfy_max(i, 0, column)
            elif direction == "desc":
                self.heapfy_min(i, 0, column)
        self.ordered_by = column


            

    #def sort(self, column, direction="asc"):
    #   if column == "ID" or column == "Count":
    #        return self.__quick_sort(column, direction)

    def __id_binary_search(self, column, value):
        """Busca binária para valores de 'id' de objetos Event.
        Método auxiliar a __exact_search().

        Args:
            column (str): Nome da coluna que está sendo buscada.
            value (int): Valor procurado.

        Returns:
            int | None: Índice do evento correspondente ao valor buscado no DataGrid, ou None se não existe.
        """
        start = 0
        end = self.size - 1
        mid = int(end/2)

        while start != end: 
            if getattr(self.list[mid], column) == value: return mid # Foi encontrado
        
            if getattr(self.list[mid], column) < value: start = mid
            else: end = mid

            mid = int(start + (end - start)/2)
            
        if getattr(self.list[mid], column) == value: return mid
        return None # Não foi encontrado
    
    def __owner_binary_search(self, column, value):
        """Busca binária para valores de 'owner_id' de objetos Event.
        Método auxiliar a __exact_search().

        Args:
            column (str): Nome da coluna que está sendo buscada.
            value (int): Valor procurado.

        Returns:
            int | None: Índice do evento correspondente ao valor buscado no DataGrid, ou None se não existe.
        """
        start = 0
        end = self.size - 1
        mid = int(end/2)

        while start != end: 
            if getattr(self.list[mid], column) == value: return mid # Foi encontrado
        
            if string_lesser(getattr(self.list[mid], column), value, 5, 5): start = mid
            else: end = mid

            mid = int(start + (end - start)/2)
        
        if getattr(self.list[mid], column) == value: return mid
        return None # Não foi encontrado

    def __exact_search(self, column, value):
        """Busca por valores numéricos no DataGrid.
        Método auxiliar a search().

        Args:
            column (str): Nome da coluna que está sendo buscada.
            value (int | str): Valor procurado.

        Returns:
            int | None: Índice do evento correspondente ao valor buscado no DataGrid, ou None se não existe.
        """
        # Se estiver ordenado pela coluna que estamos buscando, implementa a binary search
        if self.ordered_by == column:
            if column == "id":
                return self.__id_binary_search(column, value)
            elif column == "owner_id":
                return self.__owner_binary_search(column, value)

        # Se não, faça busca linear
        for idx in range(self.size):
            if getattr(self.list[idx], column) == value:
                return idx
        
        return None # Pior caso: não foi encontrado

    def __interval_binary_search(self, column, value):
        """Busca binária para valores pertencentes a um intervalo no DataGrid.
        Método auxiliar de __interval_search().

        Args:
            column (str): Nome da coluna que está sendo buscada.
            value (tuple): Tupla com valores de início e fim do intervalo desejado, ambos inclusive.

        Returns:
            list: Lista de índices dos elementos do DataGrid que pertencem ao intervalo desejado.
        """
        # Casos em que é impossível o intervalo existir no datagrid
        if getattr(self.list[self.size-1], column) < value[0] or getattr(self.list[0], column) > value[1]: return []

        # Se procurar por data, usa timestamp ao invés da string
        if column == "creation_date": 
            column = "timestamp"
            value[0], value[1] = date_to_timestamp(value[0]), date_to_timestamp(value[1]) 
        
        start = 0
        end = self.size - 1
        mid = int(end/2)

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
        mid = int(end/2)

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

    def __interval_search(self, column, value):
        """Busca de valores pertencentes a um intervalo no DataGrid.
        Método auxiliar de search().

        Args:
            column (str): Nome da coluna que está sendo buscada.
            value (tuple): Tupla com valores de início e fim do intervalo desejado, ambos inclusive.

        Returns:
            list: Lista de índices dos elementos do DataGrid que pertencem ao intervalo desejado.
        """
        # Busca binária caso esteja ordenado
        if self.ordered_by == column:
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

    def __contain_search(self, column, value):
        """Busca por Events cujas entradas contenham o value passado.

        Args:
            column (str): Nome da coluna que está sendo buscada.
            value (str): Valor que deverá estar contido na entrada da coluna passada.

        Returns:
            list: Lista de índices dos Events cujas entradas contêm o valor passado na coluna passada.
        """
        lenght = len(value)     
        result = []

        for idx in range(self.size):
            if self.__contain(getattr(self.list[idx], column), value, lenght):
                result.append(idx)
        return result

    def search(self, column, value):
        """Busca pelo valor desejado na coluna desejada.

        Args:
            column (str): Nome da coluna onde será realizada a busca.
            value (int | str | tuple): Valor que será buscado na coluna passada. O tipo do parâmetro deve ser coerente com o tipo de busca da coluna passada.

        Returns:
            _type_: _description_
        """
        # Busca exata
        if column == "id" or column == "owner_id":
            idx = self.__exact_search(column, value)
            
            if idx == None: return None

            result = DataGrid()
            result.list.append(self.list[idx])
            result.size += 1
            return result

        # Busca por intervalo
        elif column == "creation_date" or column == "count":
            idx_list = self.__interval_search(column, value)
            if len(idx_list) > 0:
                result = DataGrid()
                for i in idx_list:
                    result.list.append(self.list[i])
                    result.size += 1
                return result
        
        # Busca por conteúdo
        elif column == "name" or column == "content":
            idx_list = self.__contain_search(column, value)
            
            if len(idx_list) > 0:
                result = DataGrid()
                for i in idx_list:
                    result.list.append(self.list[i])
                    result.size += 1
                return result

        return None # Pior caso: busca não encontrou nada
    
    def copy(self):
        """Produz uma deep copy do datagrid       
        """
        new_datagrid = DataGrid()

        # Copia a lista de eventos
        new_datagrid.list = self.list.copy()

        # Copia os atributos
        new_datagrid.ordered_by = self.ordered_by
        new_datagrid.size = self.size

        return new_datagrid
    
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
        
    def select_count(self, i, j):
        """Seleciona um intervalo de entradas do DataGrid com base na coluna count ordenada de forma crescente.

        Args:
            i (int): índice inicial do intervalo
            j (int): índice final do intervalo
        """

        # Caso o datagrid esteja ordenado, basta retornar o intervalo entre a i-ésima e a j-ésima entrada
        if self.ordered_by == "Count":

            datagrid_selected = DataGrid()

            datagrid_selected.list = self.list[i:j+1]
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
    datagrid.insertion_sort("ID")

    datagrid.show()

    print("Ordenando de forma decrescente DataGrid pela coluna ID com Selection Sort")
    datagrid.selection_sort("ID", "desc")

    datagrid.show()
    
    print("Após deletar o evento 2 pela sua posição")

    # Deletar um evento
    datagrid.delete_row("id", 0, "position")

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
    datagrid_csv.read_csv("data/sample.csv")
    datagrid_csv.show()

    print("select_count(2, 5) para um vetor não ordenado")
    print("Ordenação:", datagrid_csv.ordered_by)
    datagrid_csv.select_count(2, 5).show()

    print("select_count(2, 5) para um vetor ordenado")
    datagrid_csv.insertion_sort("Count")
    print("Ordenação:", datagrid_csv.ordered_by)
    datagrid_csv.select_count(2, 5).show()