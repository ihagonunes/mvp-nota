import streamlit as st
from services.nfce_parser import processar_nfce
from services.gerarReembolso import gerar_excel_reembolso
from datetime import date

st.set_page_config(
    page_title="Reembolso Empresarial | NFC-e Suite",
    page_icon="📋",
    layout="centered",
)

st.markdown("""
<style>
  .block-container { padding-top: 2rem; }
  .page-header {
    background: linear-gradient(135deg, #1A3A2F, #1A7A4A);
    border-radius: 12px; padding: 1.8rem 2rem;
    margin-bottom: 2rem; color: white;
  }
  .page-header h2 { margin: 0; font-size: 1.8rem; }
  .page-header p  { margin: .4rem 0 0; opacity: .85; }
  .metric-box {
    background: #ECFDF5; border-radius: 10px;
    padding: 1rem 1.5rem; text-align: center;
    border-left: 4px solid #1A7A4A;
  }
  .metric-val { font-size: 1.6rem; font-weight: 800; color: #1A3A2F; }
  .metric-lbl { font-size: .85rem; color: #64748B; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <h2>📋 Reembolso Empresarial</h2>
  <p>Gere um relatório profissional de reembolso a partir da NFC-e — sem digitar nada manualmente.</p>
</div>
""", unsafe_allow_html=True)

# ── Estado ────────────────────────────────────────────────────────────────────
if "re_step" not in st.session_state:
    st.session_state.re_step = "input"

# ── ETAPA 1: INPUT ────────────────────────────────────────────────────────────
if st.session_state.re_step == "input":

    url = st.text_input(
        "🔗 Link da NFC-e",
        placeholder="https://nfce.sefaz.xx.gov.br/...",
        key="re_url",
    )

    st.markdown("#### 👤 Dados do Solicitante")
    col1, col2 = st.columns(2)
    with col1:
        solicitante = st.text_input("Nome completo", key="re_solicitante", placeholder="João da Silva")
        centro_custo = st.text_input("Centro de custo / Departamento", key="re_cc", placeholder="TI — Infraestrutura")
    with col2:
        cargo = st.text_input("Cargo / Função", key="re_cargo", placeholder="Analista de Sistemas")
        data_compra = st.date_input("Data da compra", value=date.today(), key="re_data")

    justificativa = st.text_area(
        "📝 Justificativa da despesa",
        placeholder="Ex: Material de escritório para o projeto X — reunião com cliente em 30/04/2025.",
        height=100,
        key="re_just",
    )

    if st.button("➡️ Gerar Relatório", type="primary", use_container_width=True):
        if not url.strip():
            st.error("Cole o link da NFC-e antes de continuar.")
        elif not solicitante.strip():
            st.error("Informe o nome do solicitante.")
        else:
            st.session_state.re_url_val        = url.strip()
            st.session_state.re_solicitante_val = solicitante.strip()
            st.session_state.re_cargo_val       = cargo.strip()
            st.session_state.re_cc_val          = centro_custo.strip()
            st.session_state.re_data_val        = data_compra.strftime("%d/%m/%Y")
            st.session_state.re_just_val        = justificativa.strip()
            st.session_state.re_step            = "processing"
            st.rerun()

# ── ETAPA 2: PROCESSAMENTO ────────────────────────────────────────────────────
elif st.session_state.re_step == "processing":
    st.info("⚙️ Processando nota fiscal...")
    bar = st.progress(0)
    status = st.empty()

    def cb(pct, msg):
        bar.progress(pct)
        status.text(msg)

    try:
        itens, total = processar_nfce(
            st.session_state.re_url_val,
            [],
            progress_callback=cb,
        )
        caminho = gerar_excel_reembolso(
            itens,
            solicitante  = st.session_state.re_solicitante_val,
            cargo        = st.session_state.re_cargo_val,
            centro_custo = st.session_state.re_cc_val,
            justificativa= st.session_state.re_just_val,
            data_compra  = st.session_state.re_data_val,
        )
        st.session_state.re_itens  = itens
        st.session_state.re_total  = total
        st.session_state.re_excel  = caminho
        st.session_state.re_step   = "result"
        st.rerun()
    except Exception as e:
        st.error(f"❌ Erro ao processar a nota: {e}")
        if st.button("↩️ Tentar novamente"):
            st.session_state.re_step = "input"
            st.rerun()

# ── ETAPA 3: RESULTADO ────────────────────────────────────────────────────────
elif st.session_state.re_step == "result":
    itens = st.session_state.re_itens
    total = st.session_state.re_total

    st.success("✅ Relatório de reembolso gerado!")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-val">R$ {total:,.2f}</div>
          <div class="metric-lbl">Valor Total da Nota</div>
        </div>""".replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-val">{len(itens)}</div>
          <div class="metric-lbl">Itens na Nota</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("📋 Ver itens da nota", expanded=True):
        import pandas as pd
        df_preview = pd.DataFrame(itens)[["Produto", "Quantidade", "Valor Unitário", "Subtotal"]]
        df_preview["Valor Unitário"] = df_preview["Valor Unitário"].map("R$ {:,.2f}".format)
        df_preview["Subtotal"]       = df_preview["Subtotal"].map("R$ {:,.2f}".format)
        st.dataframe(df_preview, use_container_width=True, hide_index=True)

    with open(st.session_state.re_excel, "rb") as f:
        st.download_button(
            "⬇️ Baixar Relatório de Reembolso",
            data=f,
            file_name="reembolso_empresarial.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary",
        )

    st.info("💡 O arquivo inclui a aba **Solicitação** (itens e total) e a aba **Aprovação** (campos para assinatura).")

    if st.button("🔁 Novo Reembolso", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k.startswith("re_"):
                del st.session_state[k]
        st.rerun()
