<h1 align="center">🧾 NFC-e Suite</h1>

<p align="center">
  <strong>Transforme sua nota fiscal em inteligência financeira — em segundos.</strong><br/>
  Cole o link da NFC-e e receba planilhas Excel prontas para dividir contas, pedir reembolsos e comparar preços.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/openpyxl-3.1%2B-217346?logo=microsoftexcel&logoColor=white" />
  <img src="https://img.shields.io/badge/licença-MIT-green" />
</p>

---

## 💡 Proposta de Valor

A NFC-e (Nota Fiscal de Consumidor Eletrônica) é emitida em todo o Brasil e carrega um **QR Code** que abre a nota completa no browser. A NFC-e Suite lê esse link e converte os dados em planilhas prontas para uso — sem cadastro, sem upload de arquivos, sem digitar nada manualmente.

> Os dados são processados localmente. Sua nota nunca sai do seu computador.

---

## 🛠️ Funcionalidades

### 🛒 Divisão de Compras
Informe quem vai rachar a conta e receba uma planilha com o valor exato de cada pessoa. A aba **Resumo** consolida o total por participante.

**Ideal para:** repúblicas, grupos de amigos, casais, festas e churrascos.

### 📋 Reembolso Empresarial
Gere um relatório profissional de reembolso em segundos. O arquivo inclui:
- **Aba Solicitação:** cabeçalho com dados do solicitante, tabela de itens e total
- **Aba Aprovação:** campos para assinatura de gestor, financeiro e diretoria

**Ideal para:** analistas, consultores e qualquer profissional que precise prestar contas de despesas.

### 💰 Comparação de Preços
Cole notas de até 5 mercados diferentes e veja um comparativo lado a lado. O menor preço fica destacado em **verde** e o maior em **vermelho**.

**Ideal para:** consumidores atentos, donas de casa, gestores de estoque e quem quer saber onde o dinheiro rende mais.

---

## ⚡ Como usar

1. **Peça o cupom fiscal** — impresso ou digital (WhatsApp, e-mail)
2. **Escaneie o QR Code** com o celular — o browser abre a nota da Sefaz
3. **Copie o link** da barra de endereços
4. **Cole na ferramenta** desejada na aplicação e preencha as informações
5. **Baixe o Excel** gerado automaticamente

---

## 🗂️ Estrutura do Projeto

```
mvp-nota/
├── app.py                            # Landing page / Home
├── pages/
│   ├── 1_Divisão_de_Compras.py       # Página 1
│   ├── 2_Reembolso_Empresarial.py    # Página 2
│   └── 3_Comparação_de_Preços.py     # Página 3
├── services/
│   ├── nfce_parser.py                # Engine de leitura da NFC-e (compartilhada)
│   ├── gerarExcel.py                 # Geração do Excel de divisão
│   ├── gerarReembolso.py             # Geração do relatório de reembolso
│   └── gerarComparacao.py            # Geração do comparativo de preços
├── utils/
│   └── numbersFunc.py                # Conversão de números pt-BR → float
├── .streamlit/
│   └── config.toml                   # Tema visual da aplicação
└── requirements.txt
```

---

## 🚀 Executar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/mvp-nota.git
cd mvp-nota

# 2. Crie e ative um ambiente virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie a aplicação
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`.

---

## ☁️ Deploy no Streamlit Cloud (gratuito)

1. Faça fork deste repositório para sua conta do GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io) e conecte sua conta
3. Clique em **New app** → selecione o repositório e `app.py` como entry point
4. Clique em **Deploy** — em menos de 2 minutos a aplicação estará online

> O Streamlit Cloud oferece deploy gratuito para repositórios públicos.

---

## 🔧 Stack Técnica

| Tecnologia | Função |
|---|---|
| [Python 3.10+](https://python.org) | Linguagem principal |
| [Streamlit](https://streamlit.io) | Framework web / UI |
| [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) | Web scraping da NFC-e |
| [Requests](https://pypi.org/project/requests/) | Requisições HTTP |
| [Pandas](https://pandas.pydata.org) | Manipulação dos dados |
| [openpyxl](https://openpyxl.readthedocs.io) | Geração e estilização do Excel |

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.
