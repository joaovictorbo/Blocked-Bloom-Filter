# utils.py

def print_filter_stats(bloom_filter):
    """
    Exibe informações básicas sobre o filtro.
    
    Parâmetros:
      bloom_filter (BlockedBloomFilter): Instância do filtro.
    """
    print("=== Estatísticas do Blocked Bloom Filter ===")
    print(f"Capacidade esperada: {bloom_filter.capacity}")
    print(f"Taxa de erro desejada: {bloom_filter.error_rate}")
    print(f"Total de bits (m): {bloom_filter.m}")
    print(f"Número de funções de hash (k): {bloom_filter.k}")
    print(f"Número de blocos: {bloom_filter.num_blocks}")
    print(f"Tamanho do bloco: {bloom_filter.block_size} bits")
