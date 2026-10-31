import requests
from bs4 import BeautifulSoup
from utils.numbersFunc import limpar_numero


def processar_nfce(
    url: str,
    pessoas: list,
    progress_callback=None,
    html: str | None = None,
) -> tuple[list[dict], float]:
    """
    Processa NFC-e e retorna (itens, total_geral).
    itens: lista de dicts com Produto, Quantidade, Valor Unitário, Subtotal.
    total_geral: soma de todos os Subtotais.
    progress_callback: função (percentual: int, mensagem: str) -> None
    html: conteúdo da página da nota salva pelo usuário; se informado, a URL não é consultada.
    """

    def progress(p, msg):
        if progress_callback:
            progress_callback(p, msg)

    if html is None:
        progress(5, "Conectando à nota fiscal...")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        html = response.text
    else:
        progress(5, "Lendo arquivo da nota...")

    soup = BeautifulSoup(html, "html.parser")

    progress(25, "Lendo itens da nota...")

    itens_html = soup.select("tr[id^='Item']")
    if not itens_html:
        if "Request Rejected" in html:
            raise ValueError(
                "O portal da SEFAZ bloqueou a consulta automática desta nota."
            )
        raise ValueError(
            "Nenhum item encontrado na nota. Verifique se o link está completo e se a nota "
            "já está disponível para consulta no portal da SEFAZ."
        )

    itens: list[dict] = []
    total_itens = len(itens_html)

    for idx, item in enumerate(itens_html):
        nome = item.select_one(".txtTit").get_text(strip=True)

        qtd_raw   = item.select_one(".Rqtd").get_text(strip=True)
        qtd_limpa = qtd_raw.replace("Qtde:", "").replace("Qtde.:", "").strip()
        qtd       = limpar_numero(qtd_limpa)

        valor_raw   = item.select_one(".RvlUnit").get_text(strip=True)
        valor_limpo = valor_raw.replace("Vl. Unit.:", "").replace("Vl.Unit.:", "").strip()
        valor       = limpar_numero(valor_limpo)

        subtotal = round(qtd * valor, 2)

        itens.append({
            "Produto":        nome,
            "Quantidade":     qtd,
            "Valor Unitário": valor,
            "Subtotal":       subtotal,
        })

        progresso = 25 + int((idx + 1) / total_itens * 65)
        progress(progresso, f"Processando item {idx + 1}/{total_itens}...")

    total_geral = round(sum(i["Subtotal"] for i in itens), 2)

    progress(100, "Processamento finalizado!")

    return itens, total_geral
