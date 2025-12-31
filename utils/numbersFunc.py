def limpar_numero(texto: str) -> float:
    """
    Converte número pt-BR para float de forma robusta.
    """
    if not texto:
        return 0.0
    
    # Remove R$, espaços normais e espaços especiais (\xa0)
    texto = texto.replace("R$", "").replace("\xa0", "").strip()
    
    # Se o número usa ponto como milhar (ex: 1.200,50), removemos o ponto
    # e trocamos a vírgula decimal por ponto.
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    
    try:
        return float(texto)
    except ValueError:
        # Caso ainda reste algum caractere não numérico por erro do site
        import re
        # Mantém apenas números e o ponto decimal
        apenas_numeros = re.sub(r"[^0-9.]", "", texto)
        return float(apenas_numeros) if apenas_numeros else 0.0