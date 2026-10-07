"""Consulta de cotações de moedas via AwesomeAPI.

Uso:
    python menu_informativo.py
"""

import re

import requests

API_URL = "https://economia.awesomeapi.com.br/json/last/{par}"
TIMEOUT_SEGUNDOS = 10
PADRAO_PAR = re.compile(r"^[A-Z]{3,5}-[A-Z]{3}$")

MENU_MOEDAS = """
=== Opções de Moedas para Consulta ===

Tradicionais:

- USD-BRL (Dólar Americano)
- EUR-BRL (Euro)
- GBP-BRL (Libra Esterlina)
- ARS-BRL (Peso Argentino)

Criptomoedas:

- BTC-BRL (Bitcoin)
- ETH-BRL (Ethereum)

Digite 'sair' para encerrar.
=====================================
"""


class ErroConsulta(Exception):
    """Erro ao consultar a API, com mensagem pronta para o usuário."""


def normalizar_par(entrada):
    """Padroniza a entrada (maiúsculas, sem espaços) e valida o formato."""
    par = entrada.strip().upper()
    if not PADRAO_PAR.match(par):
        raise ErroConsulta(
            f"Formato inválido: '{entrada.strip()}'. Use o padrão MOEDA-MOEDA, ex: USD-BRL."
        )
    return par


def consultar_moeda(par):
    """Retorna o dicionário de cotação do par (ex: 'USD-BRL') ou levanta ErroConsulta."""
    url = API_URL.format(par=par)

    try:
        resposta = requests.get(url, timeout=TIMEOUT_SEGUNDOS)
    except requests.Timeout:
        raise ErroConsulta("A API demorou demais para responder. Tente novamente.")
    except requests.ConnectionError:
        raise ErroConsulta("Não foi possível conectar. Verifique sua internet.")
    except requests.RequestException as erro:
        raise ErroConsulta(f"Erro inesperado na requisição: {erro}")

    if resposta.status_code == 404:
        raise ErroConsulta(f"O par '{par}' não é suportado pela API.")
    if resposta.status_code != 200:
        raise ErroConsulta(f"A API retornou o status {resposta.status_code}.")

    try:
        dados = resposta.json()
        return dados[par.replace("-", "")]
    except (ValueError, KeyError):
        raise ErroConsulta("Resposta inesperada da API.")


def formatar_brl(valor):
    """Formata em reais no padrão brasileiro.

    Valores abaixo de R$ 1 usam mais casas decimais, senão moedas de baixo
    valor (como o peso argentino) apareceriam como R$ 0,00.
    """
    numero = float(valor)
    casas = 2 if numero >= 1 else 6
    texto = f"{numero:,.{casas}f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def exibir_cotacao(par, dados):
    """Imprime os principais campos da cotação."""
    variacao = float(dados["pctChange"])
    print("\nRequisição bem-sucedida!")
    print(f"Cotação de {par} ({dados['name']})")
    print(f"  Compra (bid):  {formatar_brl(dados['bid'])}")
    print(f"  Venda (ask):   {formatar_brl(dados['ask'])}")
    print(f"  Máxima do dia: {formatar_brl(dados['high'])}")
    print(f"  Mínima do dia: {formatar_brl(dados['low'])}")
    print(f"  Variação:      {variacao:+.2f}%")
    print(f"  Atualizado em: {dados['create_date']}")


def main():
    print(MENU_MOEDAS)

    while True:
        entrada = input("Digite a moeda que deseja consultar (ex: USD-BRL): ")

        if entrada.strip().lower() in {"sair", "s", "q"}:
            print("Encerrando. Até a próxima!")
            break

        try:
            par = normalizar_par(entrada)
            dados = consultar_moeda(par)
        except ErroConsulta as erro:
            print(f"\nErro: {erro}\n")
            continue

        exibir_cotacao(par, dados)
        print()


if __name__ == "__main__":
    main()
