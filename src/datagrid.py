
class DataGrid():
    """Objeto que armazena um datagrid de negócios
    """
    def __init__(self):
        """Inicializa um DataGrid vazio
        """
        self.list = []

    def insert_row(self, row):
        """Insere uma linha no DataGrid

        Args:
            row (dict): dicionário contendo dados de uma linha do DataGrid, com o nome das colunas como chaves, e as entradas do DataGrid como valores.
        """
        event = Event(**row)
        self.list.append(event)
    
    def delete_row(self, column, value):
        """Deleta uma linha do DataGrid

        Args:
            column (str): nome da coluna que será usada para encontrar o valor a ser deletado
            value (any): valor que será usado para encontrar a linha a ser deletada
        """
        new_list = []
        for event in self.list:
            if getattr(event, column) != value:
                new_list.append(event)
        self.list = new_list
        
    def show(self, start=0, end=100):
        """Imprime o conteúdo do DataGrid (segundo o início e fim especificados)

        Args:
            start (int): índice inicial da impressão. 0, por padrão.
            end (int): índice final da impressão. 100, por padrão.
        """

        # Caso o índice inicial seja maior que o tamanho da lista, ou caso o índice inicial seja igual ao índice final, não há eventos para serem impressos
        if (start > len(self.list) or start == end):
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

    def __insertion_sort(self, column, direction="asc"):
        """
        Ordena um datagrid usando o algoritmo de ordenação por inserção.

        Args:
            column (str): O nome da coluna pela qual o datagrid será ordenado.
            direction (str, optional): A direção da ordenação, "asc" para ascendente (padrão) ou "desc" para descendente.

        """
        # tamanho da entrada
        n = len(self.list)
        # Ordenanado em ordem crescente
        if direction == "asc":
            # Iniciando loop externo
            for i in range(1,n):
              current_value = self.list[i][column]
              j = i-1
              # Iniciando loop interno
              while (self.list[j] > current_value) and (j >= 0) :
                self.list[j+1][column] = self.list[j][column]
                # Atualizando j
                j -= 1
              self.list[j+1][column] = current_value
        # Ordenanado em ordem decrescente
        elif direction == "desc":
            # Iniciando loop externo
            for i in range(1,n):
              current_value= self.list[i][column]
              j = i-1
              # Iniciando loop interno
              while (self.list[j] <= current_value) and (j >= 0) :
                self.list[j+1][column] = self.list[j][column]
                # Atualizando j
                j -= 1
              self.list[j+1][column] = current_value

    # def __selection_sort(self, column, direction="asc")
            #int

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
    # def __heap_sort(self, column, direction="asc")
            #


    #def sort(self, column, direction="asc"):
    #   if column == "ID" or column == "Count":
    #        return self.__quick_sort(column, direction)
        
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

        
    print("Após deletar o evento 2")

    # Deletar um evento
    datagrid.delete_row("id", 2)

    # Verificar o conteúdo do DataGrid
    datagrid.show()


