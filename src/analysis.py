def calcular_preco_medio(df, cidade):
    """
    Calcula o preço médio dos combustíveis
    de uma cidade.
    """

    # Remove espaços antes e depois do nome
    cidade = cidade.strip()

    # Procura a cidade no DataFrame
    df_cidade = df[
        df["Municipio"].str.upper() == cidade.upper()
    ]

    # Se não encontrar
    if df_cidade.empty:
        return None

    # Calcula a média do preço por combustível
    preco_medio = (
        df_cidade
        .groupby("Produto")["Valor de Venda"]
        .mean()
    )

    return preco_medio

def melhor_combustivel(precos):

    if "ETANOL" not in precos.index:
        return "Etanol não encontrado"

    if "GASOLINA" not in precos.index:
        return "Gasolina não encontrada"

    etanol = precos["ETANOL"]
    gasolina = precos["GASOLINA"]

    percentual = etanol / gasolina

    if percentual <= 0.70:
        return "Etanol compensa"

    return "Gasolina compensa"

def estatisticas_combustiveis(precos):

    combustivel_mais_barato = precos.idxmin()
    menor_preco = precos.min()

    combustivel_mais_caro = precos.idxmax()
    maior_preco = precos.max()

    return {
        "combustivel_mais_barato": combustivel_mais_barato,
        "menor_preco": round(menor_preco, 2),

        "combustivel_mais_caro": combustivel_mais_caro,
        "maior_preco": round(maior_preco, 2)
    }

def ranking_combustiveis(precos):

    ranking = precos.sort_values()

    resultado = []

    for combustivel, preco in ranking.items():

        resultado.append({
            "combustivel": combustivel,
            "preco": round(preco, 2)
        })

    return resultado

def comparativo_etanol_gasolina(precos):

    if "ETANOL" not in precos.index:
        return None

    if "GASOLINA" not in precos.index:
        return None

    etanol = precos["ETANOL"]
    gasolina = precos["GASOLINA"]

    percentual = (etanol / gasolina) * 100

    if percentual <= 70:
        recomendacao = "Etanol compensa"
    else:
        recomendacao = "Gasolina compensa"

    return {
        "etanol": round(etanol, 2),
        "gasolina": round(gasolina, 2),
        "percentual": round(percentual, 2),
        "recomendacao": recomendacao
    }

def comparar_cidades(precos1, precos2, cidade1, cidade2):

    comparacao = []

    combustiveis = sorted(
        set(precos1.index).intersection(precos2.index)
    )

    for combustivel in combustiveis:

        preco1 = round(float(precos1[combustivel]), 2)
        preco2 = round(float(precos2[combustivel]), 2)

        if preco1 < preco2:
            mais_barata = cidade1.upper()

        elif preco2 < preco1:
            mais_barata = cidade2.upper()

        else:
            mais_barata = "EMPATE"

        comparacao.append({

            "combustivel": combustivel,

            "cidade1": preco1,

            "cidade2": preco2,

            "mais_barata": mais_barata

        })

    return comparacao