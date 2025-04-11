# hash_functions.py
import mmh3

def generate_hashes(item: str, k: int, block_size: int) -> list:
    """
    Gera uma lista de índices para um item usando a função mmh3.
    
    Parâmetros:
      item (str): O item a ser hashed.
      k (int): Número de funções de hash (ou sementes) a serem usadas.
      block_size (int): Tamanho do bloco (número de bits disponíveis no bloco).
    
    Retorna:
      Uma lista de índices inteiros no intervalo [0, block_size).
    """
    indices = []
    for seed in range(k):
        # Utiliza mmh3 com sementes diferentes para obter variabilidade
        hash_value = mmh3.hash(str(item), seed)
        indices.append(hash_value % block_size)
    return indices
