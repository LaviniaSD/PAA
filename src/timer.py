import time

# Dicionário global para armazenar os tempos de execução das funções decoradas
_execution_times = {}

def timeit(func, dict_list=False):
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

        _execution_times[func.__name__] = duration
        return result

    return wrapper

def get_execution_time(func_name, print_result=False):
    """Retorna o tempo de execução de uma função decorada a partir do nome da função.

    Args:
        func_name (str): O nome da função decorada.

    Returns:
        float: O tempo de execução da função decorada.
    """

    result = _execution_times.get(func_name, 0)

    if print_result:
        print(f'Tempo de execução da função {func_name}: {result} ns')

    return result
