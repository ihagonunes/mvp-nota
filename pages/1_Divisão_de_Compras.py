import streamlit as st
from services.nfce_parser import processar_nfce
from services.gerarExcel import gerar_excel

st.set_page_config(
    page_title="Divisão de Compras | NFC-e Suite",
    page_icon="🛒",
    layout="centered",
)

st.markdown("""
<style>
  .block-container { padding-top: 2rem; }
  .page-header {
    background: linear-gradient(135deg, #1E3A5F, #1E6FD9);
    border-radius: 12px; padding: 1.8rem 2rem;
    margin-bottom: 2rem; color: white;
  }
  .page-header h2 { margin: 0; font-size: 1.8rem; }
  .page-header p  { margin: .4rem 0 0; opacity: .85; }
  .metric-box {
    background: #EBF0F8; border-radius: 10px;
    padding: 1rem 1.5rem; text-align: center;
    border-left: 4px solid #1E6FD9;
  }
  .metric-val { font-size: 1.6rem; font-weight: 800; color: #1E3A5F; }
  .metric-lbl { font-size: .85rem; color: #64748B; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <h2>🛒 Divisão de Compras</h2>
  <p>Cole o link da NFC-e, informe quem vai rachar — e receba a planilha pronta.</p>
</div>
""", unsafe_allow_html=True)

# ── Estado ────────────────────────────────────────────────────────────────────
if "dc_step" not in st.session_state:
    st.session_state.dc_step = "input"

# ── ETAPA 1: INPUT ────────────────────────────────────────────────────────────
if st.session_state.dc_step == "input":

    with st.expander("❓ Como obter o link da NFC-e?", expanded=False):
        st.markdown("""
        1. Peça o **cupom fiscal** (impresso ou digital)
        2. Escaneie o **QR Code** com o celular — o navegador abre a nota
        3. Copie o **link da barra de endereços** e cole abaixo
        """)

    url = st.text_input(
        "🔗 Link da NFC-e",
        placeholder="https://nfce.sefaz.xx.gov.br/...",
        key="dc_url",
    )

    pessoas_texto = st.text_area(
        "👥 Pessoas que vão rachar (uma por linha)",
        placeholder="Ana\nBruno\nCarlos",
        height=130,
        key="dc_pessoas",
    )

    if st.button("➡️ Processar Nota", type="primary", use_container_width=True):
        if not url.strip():
            st.error("Cole o link da NFC-e antes de continuar.")
        elif not pessoas_texto.strip():
            st.error("Informe pelo menos uma pessoa.")
        else:
            st.session_state.dc_url_val = url.strip()
            st.session_state.dc_pessoas_val = [
                p.strip() for p in pessoas_texto.split("\n") if p.strip()
            ]
            st.session_state.dc_step = "processing"
            st.rerun()

# ── ETAPA 2: PROCESSAMENTO ────────────────────────────────────────────────────
elif st.session_state.dc_step == "processing":
    st.info("⚙️ Processando nota fiscal...")
    bar = st.progress(0)
    status = st.empty()

    def cb(pct, msg):
        bar.progress(pct)
        status.text(msg)

    try:
        itens, total = processar_nfce(
            st.session_state.dc_url_val,
            st.session_state.dc_pessoas_val,
            progress_callback=cb,
        )
        caminho = gerar_excel(itens, st.session_state.dc_pessoas_val)
        st.session_state.dc_itens = itens
        st.session_state.dc_total = total
        st.session_state.dc_excel = caminho
        st.session_state.dc_step = "result"
        st.rerun()
    except Exception as e:
        st.error(f"❌ Erro ao processar a nota: {e}")
        if st.button("↩️ Tentar novamente"):
            st.session_state.dc_step = "input"
            st.rerun()

# ── ETAPA 3: RESULTADO ────────────────────────────────────────────────────────
elif st.session_state.dc_step == "result":
    pessoas = st.session_state.dc_pessoas_val
    total   = st.session_state.dc_total
    itens   = st.session_state.dc_itens
    n       = len(pessoas)

    st.success("✅ Nota processada com sucesso!")

    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-val">R$ {total:,.2f}</div>
          <div class="metric-lbl">Total da Nota</div>
        </div>""".replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-val">{n}</div>
          <div class="metric-lbl">Pessoas</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        vpp = total / n if n else 0
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-val">R$ {vpp:,.2f}</div>
          <div class="metric-lbl">Por Pessoa</div>
        </div>""".replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Preview da tabela
    with st.expander("📋 Ver itens da nota", expanded=True):
        import pandas as pd
        df_preview = pd.DataFrame(itens)[["Produto", "Quantidade", "Valor Unitário", "Subtotal"]]
        df_preview["Valor Unitário"] = df_preview["Valor Unitário"].map("R$ {:,.2f}".format)
        df_preview["Subtotal"] = df_preview["Subtotal"].map("R$ {:,.2f}".format)
        st.dataframe(df_preview, use_container_width=True, hide_index=True)

    # Download
    with open(st.session_state.dc_excel, "rb") as f:
        st.download_button(
            "⬇️ Baixar Planilha Excel",
            data=f,
            file_name="divisao_compras.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary",
        )

    if st.button("🔁 Nova Nota", use_container_width=True):
        for k in ["dc_step", "dc_url_val", "dc_pessoas_val", "dc_itens", "dc_total", "dc_excel"]:
            st.session_state.pop(k, None)
        st.rerun()
