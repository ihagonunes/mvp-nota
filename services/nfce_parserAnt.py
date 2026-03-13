import requests
from bs4 import BeautifulSoup
from utils.numbersFunc import limpar_numero
from services.gerarExcel import gerar_excel

def extrair_itens_nfce(url: str) -> list[dict]:
    if not url.startswith("http"):
        raise ValueError("URL inválida")

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all("tr", id=lambda x: x and x.startswith("Item"))
    if not rows:
        raise Exception("Estrutura da nota fiscal não reconhecida")

    itens = []

    for row in rows:
        nome = row.find("span", class_="txtTit")
        qtd = row.find("span", class_="Rqtd")
        unit = row.find("span", class_="RvlUnit")

        if not nome:
            continue

        itens.append({
            "Item": nome.get_text(strip=True),
            "Quantidade": limpar_numero(qtd.get_text() if qtd else "1"),
            "Valor Unitário": limpar_numero(unit.get_text() if unit else "0"),
            "Div": "",
            "SubTotal": "",
            "Subtotal Individual": "",
            "Pagantes": ""
        })

    caminho = gerar_excel(itens)
    return caminho