# Consumo de API REST com Python

Programa de terminal que consulta cotações de moedas e criptomoedas em tempo real
usando a [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas), sem necessidade de chave de acesso.

## Funcionalidades

- Menu com moedas tradicionais (USD, EUR, GBP, ARS) e criptomoedas (BTC, ETH)
- Aceita qualquer par suportado pela API (ex: `USD-BRL`, `eur-brl`)
- Exibe compra, venda, máxima, mínima, variação percentual e horário da cotação
- Múltiplas consultas na mesma execução (digite `sair` para encerrar)
- Tratamento de erros: formato inválido, par não suportado, timeout e falta de conexão
- Valores abaixo de R$ 1 mostrados com mais casas decimais (ex: peso argentino)

## Como executar

```bash
# 1. Crie e ative um ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute
python menu_informativo.py
```

## Exemplo de saída

```
Digite a moeda que deseja consultar (ex: USD-BRL): usd-brl

Requisição bem-sucedida!
Cotação de USD-BRL (Dólar Americano/Real Brasileiro)
  Compra (bid):  R$ 5,45
  Venda (ask):   R$ 5,45
  Máxima do dia: R$ 5,48
  Mínima do dia: R$ 5,41
  Variação:      +0.35%
  Atualizado em: 2026-10-06 19:50:00
```

*(valores ilustrativos)*

## Tecnologias

- Python 3
- [requests](https://requests.readthedocs.io/)
