import time
import sys
sys.setrecursionlimit(10**6) 

# Dicionário global para armazenar os tempos de execução das funções decoradas
_execution_times = {}

def timeit(func):
    """Decorador para medir o tempo de execução de uma função.

    Args:
        func (function): A função a ser decorada.

    Returns:
        function: A função decorada.    
    """
    
    def wrapper(*args, **kwargs):
        """Wrapper da função decorada.

        Args:
            *args: Argumentos posicionais da função.
            **kwargs: Argumentos nomeados da função.

        Returns:
            object: O resultado da função decorada.        
        """
        
        
        start_time = time.time_ns()     # Início da contagem de tempo
        result = func(*args, **kwargs)  # Execução da função decorada
        end_time = time.time_ns()       # Fim da contagem de tempo

        # Calcula o tempo de execução da função decorada e armazena em um dicionário global
        duration = (end_time - start_time)
        # duration = (end_time - start_time)

        # Checa se a função decorada já foi executada antes
        if func.__name__ not in _execution_times:
            # Se não, cria uma lista, onde o primeiro elemento é o tempo de execução mensurado
            _execution_times[func.__name__] = [duration]
        else:
            # Se sim, adiciona o tempo de execução mensurado à lista
            _execution_times[func.__name__].append(duration)

        return result

    return wrapper

def get_execution_time(func_name, print_result=False):
    """Retorna o tempo de execução de uma função decorada a partir do nome da função.

    Args:
        func_name (str): O nome da função decorada.

    Returns:
        float: O tempo de execução da função decorada.
    """

    time_list = _execution_times.get(func_name, 0)

    # Como o tempo de execução é uma lista, retorna a média dos tempos
    result = sum(time_list) / len(time_list)

    if print_result:
        print(f'Tempo de execução da função {func_name}: {result} ns')

    return result

def reset_execution_times():
    """Reseta o dicionário global de tempos de execução.
    """
    _execution_times.clear()
