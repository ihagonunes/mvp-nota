import requests
from bs4 import BeautifulSoup
from services.gerarExcel import gerar_excel

print("✅ services.nfce_parser carregado")

from utils.numbersFunc import limpar_numero

def processar_nfce(
    url: str,
    pessoas: str,
    progress_callback=None
) -> str:
    """
    Processa NFC-e e gera Excel.
    progress_callback: função que recebe (percentual, mensagem)
    """

    def progress(p, msg):
        if progress_callback:
            progress_callback(p, msg)

    progress(5, "Conectando à nota fiscal...")

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    progress(25, "Lendo itens da nota...")

    itens_html = soup.select("tr[id^='Item']")
    itens = []

    total_itens = len(itens_html)

    for idx, item in enumerate(itens_html):
        nome = item.select_one(".txtTit").get_text(strip=True)

        # Pegar o texto bruto
        qtd_raw = item.select_one(".Rqtd").get_text(strip=True)
        # Remover "Qtde:" ou "Qtde.:" e limpar espaços
        qtd_limpa = qtd_raw.replace("Qtde:", "").replace("Qtde.:", "").strip()
        qtd = limpar_numero(qtd_limpa)

        valor_raw = item.select_one(".RvlUnit").get_text(strip=True)
        # Remover o prefixo do valor unitário e limpar espaços
        valor_limpo = valor_raw.replace("Vl. Unit.:", "").replace("Vl.Unit.:", "").strip()
        valor = limpar_numero(valor_limpo)

        subtotal = round(qtd * valor, 2)

        itens.append({
            "Produto": nome,
            "Quantidade": qtd,
            "Valor Unitário": valor,
            "Subtotal": subtotal
        })

        progresso = 25 + int((idx + 1) / total_itens * 50)
        progress(progresso, f"Processando item {idx + 1}/{total_itens}")

    progress(80, "Gerando planilha Excel...")

    caminho = gerar_excel(itens, pessoas)

    progress(100, "Processamento finalizado!")

    return caminho
