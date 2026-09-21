# NFC-e Suite

Transforme a sua NFC-e (Nota Fiscal de Consumidor Eletrônica) em planilhas Excel prontas para dividir contas, pedir reembolsos e comparar preços.

**Status:** Concluído

## Proposta

Toda NFC-e emitida no Brasil carrega um **QR Code** que abre a nota completa no navegador. A NFC-e Suite lê esse link, converte os dados da nota em planilhas prontas para uso — sem cadastro, sem upload de arquivos e sem digitação manual.

Não há cadastro nem envio de arquivos: a aplicação busca a página pública da nota na Sefaz (a partir do link informado), faz o parsing com BeautifulSoup e gera o Excel localmente no ambiente em que está rodando.

## Funcionalidades

### Divisão de Compras
Informe as pessoas que vão dividir a conta e receba uma planilha com o valor exato por participante. A aba **Resumo** consolida o total por pessoa.

### Reembolso Empresarial
Gera um arquivo de reembolso com:
- **Aba Solicitação:** cabeçalho com dados do solicitante, tabela de itens e total;
- **Aba Aprovação:** campos para assinatura de gestor, financeiro e diretoria.

### Comparação de Preços
Compare notas de até 5 mercados lado a lado, com o menor preço destacado em verde e o maior em vermelho.

## Como Usar

1. Peça o cupom fiscal — impresso ou digital (WhatsApp, e-mail).
2. Escaneie o QR Code: o navegador abre a nota na Sefaz.
3. Copie o link da barra de endereços.
4. Cole o link na ferramenta desejada e preencha as informações complementares.
5. Baixe o Excel gerado.

## Estrutura do Projeto

```text
mvp-nota/
  app.py                            # Landing page / Home
  pages/
    1_Divisão_de_Compras.py         # Divisão de compras
    2_Reembolso_Empresarial.py      # Reembolso empresarial
    3_Comparação_de_Preços.py       # Comparação de preços
  services/
    nfce_parser.py                  # Engine de leitura da NFC-e (compartilhada)
    gerarExcel.py                   # Geração do Excel de divisão
    gerarReembolso.py               # Geração do relatório de reembolso
    gerarComparacao.py              # Geração do comparativo de preços
  utils/
    numbersFunc.py                  # Conversão de números pt-BR -> float
  .streamlit/
    config.toml                     # Tema visual da aplicação
  requirements.txt
  README.md
```

## Executar Localmente

```bash
git clone https://github.com/ihagonunes/mvp-nota.git
cd mvp-nota

python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

A aplicação fica disponível em `http://localhost:8501`.

## Deploy no Streamlit Cloud 

Acesse [NFC-e Suite](https://nfc-esuite.streamlit.app/)

## Stack

| Tecnologia | Função |
|---|---|
| Python 3.10+ | Linguagem principal |
| Streamlit | Framework web / UI |
| BeautifulSoup4 | Parsing do HTML da NFC-e |
| Requests | Requisição HTTP ao link da nota |
| Pandas | Manipulação dos dados |
| openpyxl | Geração e estilização do Excel |

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).