print("🚀 app.py iniciado")

import streamlit as st
from utils.qr_reader import ler_qr_code
from services.nfce_parser import processar_nfce


st.set_page_config(page_title="Divisão de Compras", page_icon="🧾")

# =============================
# Estado global
# =============================
if "step" not in st.session_state:
    st.session_state.step = "input"

if "excel_path" not in st.session_state:
    st.session_state.excel_path = None

# =============================
# ETAPA 1 — INPUT
# =============================
if st.session_state.step == "input":
    st.title("📸 Leitura da Nota Fiscal")

    # Upload do QR Code
    st.subheader("1️⃣ Envie a imagem do QR Code")
    imagem = st.file_uploader(
        "Foto do QR Code da nota",
        type=["png", "jpg", "jpeg"]
    )

    url_extraida = ""

    if imagem:
        with st.spinner("Lendo QR Code..."):
            resultado = ler_qr_code(imagem)

        if resultado:
            st.success("QR Code lido com sucesso!")
            url_extraida = resultado
        else:
            st.warning("Não foi possível ler o QR Code. Você pode colar o link manualmente.")

    # Campo de URL (editável)
    st.subheader("2️⃣ Confirme o link da nota")
    url = st.text_input(
        "Link da NFC-e",
        value=url_extraida
    )

    # Pessoas
    st.subheader("3️⃣ Pessoas pagantes")
    pessoas_texto = st.text_area(
        "Digite um nome por linha",
        placeholder="Ana\nBruno\nCarlos"
    )

    if st.button("➡️ Processar nota"):
        if not url or not pessoas_texto.strip():
            st.error("Preencha o link da nota e as pessoas.")
        else:
            st.session_state.url = url
            st.session_state.pessoas = [
                p.strip() for p in pessoas_texto.split("\n") if p.strip()
            ]
            st.session_state.step = "processing"
            st.rerun()

# =============================
# ETAPA 2 — PROCESSAMENTO
# =============================
elif st.session_state.step == "processing":
    st.title("⚙️ Processando nota")

    progress_bar = st.progress(0)
    status = st.empty()

    def atualizar_progresso(percentual, mensagem):
        progress_bar.progress(percentual)
        status.text(mensagem)

    try:
        caminho = processar_nfce(
            st.session_state.url,
            st.session_state.pessoas,
            progress_callback=atualizar_progresso
        )

        st.session_state.excel_path = caminho
        st.session_state.step = "result"
        st.rerun()

    except Exception as e:
        st.error(f"Erro ao processar NFC-e: {e}")
        st.session_state.step = "input"

# =============================
# ETAPA 3 — RESULTADO
# =============================
elif st.session_state.step == "result":
    st.title("📥 Planilha pronta")

    with open(st.session_state.excel_path, "rb") as f:
        st.download_button(
            "⬇️ Baixar Excel",
            data=f,
            file_name="divisao_compras.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    if st.button("🔁 Nova nota"):
        st.session_state.clear()
        st.rerun()
