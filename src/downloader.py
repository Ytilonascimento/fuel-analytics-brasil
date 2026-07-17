import os
import requests


URL = "https://raw.githubusercontent.com/ipeaGIT/ipeadata/master/ipeadata/data/ANP_PRECOS_COMBUSTIVEIS.csv"


def baixar_dados():
    """
    Baixa o arquivo CSV da internet
    caso ele ainda não exista.
    """

    caminho = "data/anp.csv"

    if os.path.exists(caminho):
        print("Arquivo já existe.")
        return caminho

    print("Baixando base da ANP...")

    resposta = requests.get(URL)

    resposta.raise_for_status()

    with open(caminho, "wb") as arquivo:
        arquivo.write(resposta.content)

    print("Download concluído!")

    return caminho