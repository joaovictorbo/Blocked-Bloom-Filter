# bloom_filter.py
import math
import mmh3
import threading
import pickle
from hash_functions import generate_hashes

class BlockedBloomFilter:
    def __init__(self, capacity: int, error_rate: float, block_size: int = 512):
        self.capacity = capacity
        self.error_rate = error_rate
        self.block_size = block_size
        
        # Calcula o número total de bits necessários (m)
        self.m = math.ceil(-capacity * math.log(error_rate) / (math.log(2) ** 2))
        
        # Calcula o número de blocos necessários
        self.num_blocks = math.ceil(self.m / block_size)
        
        # Número ótimo de funções de hash (k)
        self.k = int(math.ceil((self.m / capacity) * math.log(2)))
        
        # Inicializa os blocos; cada bloco é representado por um inteiro (vetor de bits)
        self.blocks = [0] * self.num_blocks
        
        # Lock para garantir thread-safe nas operações
        self.lock = threading.Lock()
    
    def __getstate__(self):
        # Cria o estado do objeto sem o lock, pois locks não podem ser pickleados
        state = self.__dict__.copy()
        if "lock" in state:
            del state["lock"]
        return state
    
    def __setstate__(self, state):
        # Restaura o estado e recria o lock
        self.__dict__.update(state)
        self.lock = threading.Lock()
    
    def _get_block_index(self, item) -> int:
        h = mmh3.hash(str(item), 42)  # semente fixa para seleção de bloco
        return h % self.num_blocks
    
    def add(self, item):
        block_index = self._get_block_index(item)
        indices = generate_hashes(str(item), self.k, self.block_size)
        with self.lock:
            for bit_index in indices:
                self.blocks[block_index] |= (1 << bit_index)
    
    def __contains__(self, item) -> bool:
        block_index = self._get_block_index(item)
        indices = generate_hashes(str(item), self.k, self.block_size)
        with self.lock:
            for bit_index in indices:
                if not (self.blocks[block_index] & (1 << bit_index)):
                    return False
        return True
    
    def union(self, other):
        if not isinstance(other, BlockedBloomFilter):
            raise TypeError("O outro objeto deve ser um BlockedBloomFilter.")
        if self.block_size != other.block_size or self.num_blocks != other.num_blocks or self.k != other.k:
            raise ValueError("Os filtros devem ter parâmetros compatíveis para realizar a união.")
        
        new_filter = BlockedBloomFilter(self.capacity, self.error_rate, self.block_size)
        new_filter.m = self.m
        new_filter.num_blocks = self.num_blocks
        new_filter.k = self.k
        
        new_filter.blocks = [a | b for a, b in zip(self.blocks, other.blocks)]
        return new_filter

    def intersection(self, other):
        if not isinstance(other, BlockedBloomFilter):
            raise TypeError("O outro objeto deve ser um BlockedBloomFilter.")
        if self.block_size != other.block_size or self.num_blocks != other.num_blocks or self.k != other.k:
            raise ValueError("Os filtros devem ter parâmetros compatíveis para realizar a interseção.")
        
        new_filter = BlockedBloomFilter(self.capacity, self.error_rate, self.block_size)
        new_filter.m = self.m
        new_filter.num_blocks = self.num_blocks
        new_filter.k = self.k
        
        new_filter.blocks = [a & b for a, b in zip(self.blocks, other.blocks)]
        return new_filter

    def save(self, filename: str):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename: str):
        with open(filename, "rb") as f:
            return pickle.load(f)
