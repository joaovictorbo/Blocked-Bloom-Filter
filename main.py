# main.py
from bloom_filter import BlockedBloomFilter
from utils import print_filter_stats

def main():
    # Inicializa o filtro com 1000 elementos esperados e taxa de falso positivo de 1%
    filtro1 = BlockedBloomFilter(capacity=1000, error_rate=0.01, block_size=512)
    
    # Adiciona alguns itens
    filtro1.add("apple")
    filtro1.add("banana")
    
    # Verifica a presença de itens
    print("Testando filtro1:")
    print("apple" in filtro1)   # Espera True
    print("cherry" in filtro1)  # Provavelmente False (exceto caso ocorra falso positivo)
    
    print_filter_stats(filtro1)
    
    # Cria um segundo filtro e adiciona outros itens
    filtro2 = BlockedBloomFilter(capacity=1000, error_rate=0.01, block_size=512)
    filtro2.add("cherry")
    filtro2.add("date")
    
    # Realiza a união dos filtros
    filtro_uniao = filtro1.union(filtro2)
    print("\nTestando filtro_uniao (união de filtro1 e filtro2):")
    print("apple" in filtro_uniao)   # Espera True, já que estava em filtro1
    print("cherry" in filtro_uniao)  # Espera True, já que estava em filtro2
    
    # Realiza a interseção dos filtros
    filtro_interseccao = filtro1.intersection(filtro2)
    print("\nTestando filtro_interseccao (interseção de filtro1 e filtro2):")
    print("apple" in filtro_interseccao)   # Deve ser False (não consta em ambos)
    print("cherry" in filtro_interseccao)  # Deve ser False
    
    # Exemplo de serialização: salva filtro_uniao em um arquivo e carrega novamente
    arquivo = "filtro_uniao.pkl"
    filtro_uniao.save(arquivo)
    filtro_carregado = BlockedBloomFilter.load(arquivo)
    print("\nTestando filtro carregado:")
    print("date" in filtro_carregado)   # Espera True

if __name__ == "__main__":
    main()
