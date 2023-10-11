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