import streamlit as st


def upload_html_nota(key: str) -> str | None:
    """
    Mostra a alternativa de envio da página da nota salva (.html).
    Retorna o conteúdo do arquivo enviado, ou None.
    """
    st.info(
        "💡 **Alternativa:** abra o link da nota no navegador, salve a página "
        "(`Ctrl+S` → *Página da Web, somente HTML*) e envie o arquivo aqui."
    )
    arquivo = st.file_uploader("📄 Página da nota (.html)", type=["html", "htm"], key=key)
    if arquivo is None:
        return None

    conteudo = arquivo.getvalue()
    try:
        return conteudo.decode("utf-8")
    except UnicodeDecodeError:
        return conteudo.decode("latin-1")
