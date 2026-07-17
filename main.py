from src.processor import carregar_dados
from src.analysis import calcular_preco_medio

arquivo = "data/anp.csv"

df = carregar_dados(arquivo)

print("=" * 40)
print("ANÁLISE DE COMBUSTÍVEIS DA ANP")
print("=" * 40)

cidade = input("Digite o nome da cidade: ")

resultado = calcular_preco_medio(df, cidade)

if resultado is None:
    print("\nCidade não encontrada.")
else:
    print()
    print("=" * 40)
    print(f"PREÇO MÉDIO DOS COMBUSTÍVEIS - {cidade.upper()}")
    print("=" * 40)

    for produto, preco in resultado.items():
        print(f"{produto:<20} R$ {preco:.2f}")

    print("=" * 40)