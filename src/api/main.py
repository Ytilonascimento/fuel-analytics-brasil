from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from src.processor import carregar_dados
from src.analysis import (
    calcular_preco_medio,
    melhor_combustivel,
    estatisticas_combustiveis,
    ranking_combustiveis,
    comparativo_etanol_gasolina,
    comparar_cidades
)

app = FastAPI(
    title="Fuel Analytics Brasil"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://fuel-analytics-brasil-tan.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(">>> MAIN.PY CARREGADO <<<")
print(app.user_middleware)


@app.get("/")
def inicio():
    return {
        "mensagem": "API Fuel Analytics Brasil funcionando!"
    }


@app.get("/combustivel")
def consultar_combustivel(cidade: str):

    arquivo = "data/anp.csv"

    df = carregar_dados(arquivo)

    precos = calcular_preco_medio(df, cidade)
    
    melhor = melhor_combustivel(precos)

    estatisticas = estatisticas_combustiveis(precos)

    ranking = ranking_combustiveis(precos)

    comparativo = comparativo_etanol_gasolina(precos)

    if precos is None:
        return {
            "erro": "Cidade não encontrada."
        }

    return {
    "cidade": cidade.upper(),

    "precos": {
        combustivel: round(preco, 2)
        for combustivel, preco in precos.items()
    },

    "melhor_opcao": melhor,

    "estatisticas": estatisticas,

    "ranking": ranking,

    "comparativo": comparativo
}

@app.get("/comparar")
def comparar(cidade1: str, cidade2: str):

    arquivo = "data/anp.csv"

    df = carregar_dados(arquivo)

    precos_cidade1 = calcular_preco_medio(df, cidade1)
    precos_cidade2 = calcular_preco_medio(df, cidade2)

    if precos_cidade1 is None:
        return {"erro": f"Cidade '{cidade1}' não encontrada"}

    if precos_cidade2 is None:
        return {"erro": f"Cidade '{cidade2}' não encontrada"}

    comparacao = comparar_cidades(
        precos_cidade1,
        precos_cidade2,
        cidade1,
        cidade2
    )

    return {
        "cidade1": cidade1.upper(),

        "cidade2": cidade2.upper(),

        "comparacao": comparacao
    }
