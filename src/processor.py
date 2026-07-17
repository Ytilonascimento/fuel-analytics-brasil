import pandas as pd


def carregar_dados(caminho):
    """
    Carrega o arquivo CSV da ANP.
    """

    print("Abrindo arquivo...")

    df = pd.read_csv(
        caminho,
        sep=";",
        encoding="latin1"
    )

    # Remove o caractere estranho da primeira coluna (BOM)
    df.columns = df.columns.str.replace("ï»¿", "", regex=False)

    # Converte a coluna Valor de Venda para número
    df["Valor de Venda"] = (
        df["Valor de Venda"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    df["Valor de Venda"] = pd.to_numeric(
        df["Valor de Venda"],
        errors="coerce"
    )

    print("Arquivo carregado com sucesso!")

    return df