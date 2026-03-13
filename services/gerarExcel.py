import pandas as pd
import os

def gerar_excel(itens: list[dict], pessoasStr: str) -> str:
    """
    Gera um Excel com os itens da nota.
    Retorna o caminho do arquivo.
    """
    caminho = "divisao_compras.xlsx"

    os.write(1,b'Pessoas executou (gerarExcel.py).\n')
    df = pd.DataFrame(itens)

    with pd.ExcelWriter(caminho, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Compras")
        ws = writer.book["Compras"]

        for i in range(2, len(df) + 2):
            ws[f"D{i}"] = f'=IF(G{i}="","",LEN(G{i})-LEN(SUBSTITUTE(G{i},",",""))+1)'
            ws[f"E{i}"] = f"=B{i}*C{i}"
            ws[f"F{i}"] = f'=IF(D{i}="","",E{i}/D{i})'
    return caminho
