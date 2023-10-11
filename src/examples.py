from datagrid import DataGrid
from timer import timeit, get_execution_time


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
datagrid_csv.read_csv("data_base2/data_2e4.csv", ",")

# Use select_count() num vetor não ordenado (usando 'order_and_select')
print("select_count para um vetor não ordenado usando 'order_and_select'")
print(f"Ordenação: {datagrid_csv.ordered_by}")
selected_datagrid = datagrid_csv.select_count(12, 15, "order_and_select")
print(selected_datagrid.size)
selected_datagrid.show()
get_execution_time("select_count", True)

# Use select_count() num vetor não ordenado (usando 'quickselect')
print("select_count para um vetor não ordenado usando 'quickselect'")
print(f"Ordenação: {datagrid_csv.ordered_by}")
selected_datagrid = datagrid_csv.select_count(12, 15, "quickselect")
print(selected_datagrid.size)
selected_datagrid.show()
get_execution_time("select_count", True)

# Use select_count() num vetor não ordenado (usando 'quickselect_median_of_medians')
print("select_count para um vetor não ordenado usando 'quickselect_median_of_medians'")
print(f"Ordenação: {datagrid_csv.ordered_by}")
selected_datagrid = datagrid_csv.select_count(12, 15, "quickselect_median_of_medians")
print(selected_datagrid.size)
selected_datagrid.show()
get_execution_time("select_count", True)

# Use select_count() num vetor não ordenado (asc)
print("select_count() para um vetor ordenado (asc)")
datagrid_csv.insertion_sort("count", "asc")
print(f"Ordenação: {datagrid_csv.ordered_by} ({datagrid_csv.direction})")
selected_datagrid = datagrid_csv.select_count(12, 15)
selected_datagrid.show()
get_execution_time("select_count", True)

# Use select_count() num vetor não ordenado (desc)
print("select_count() para um vetor ordenado (desc)")
datagrid_csv.insertion_sort("count", "desc")
print(f"Ordenação: {datagrid_csv.ordered_by} ({datagrid_csv.direction})")
selected_datagrid = datagrid_csv.select_count(12, 15)
selected_datagrid.show()
get_execution_time("select_count", True)

# Teste de ordenação (merge sort / id)
print("Teste merge_sort por ID")
datagrid_csv.merge_sort("id")
print("Ordenação:", datagrid_csv.ordered_by)
datagrid_csv.show()
