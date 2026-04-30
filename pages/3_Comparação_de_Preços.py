import streamlit as st
from services.nfce_parser import processar_nfce
from services.gerarComparacao import gerar_excel_comparacao
import pandas as pd

st.set_page_config(
    page_title="Comparação de Preços | NFC-e Suite",
    page_icon="💰",
    layout="wide",
)

st.markdown("""
<style>
  .block-container { padding-top: 2rem; }
  .page-header {
    background: linear-gradient(135deg, #3B1F5E, #7C3AED);
    border-radius: 12px; padding: 1.8rem 2rem;
    margin-bottom: 2rem; color: white;
  }
  .page-header h2 { margin: 0; font-size: 1.8rem; }
  .page-header p  { margin: .4rem 0 0; opacity: .85; }
  .nota-input-card {
    background: #F5F3FF; border: 1px solid #DDD6FE;
    border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: .8rem;
  }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <h2>💰 Comparação de Preços</h2>
  <p>Cole notas de mercados diferentes e descubra onde cada produto é mais barato.</p>
</div>
""", unsafe_allow_html=True)

# ── Estado ────────────────────────────────────────────────────────────────────
if "cp_step" not in st.session_state:
    st.session_state.cp_step = "input"

if "cp_num_notas" not in st.session_state:
    st.session_state.cp_num_notas = 2

# ── ETAPA 1: INPUT ────────────────────────────────────────────────────────────
if st.session_state.cp_step == "input":

    col_ctrl1, col_ctrl2, _ = st.columns([2, 2, 4])
    with col_ctrl1:
        n = st.number_input(
            "Quantas notas comparar?",
            min_value=2, max_value=5,
            value=st.session_state.cp_num_notas,
            step=1,
        )
        st.session_state.cp_num_notas = int(n)

    st.markdown("<br>", unsafe_allow_html=True)

    notas_input = []
    for i in range(st.session_state.cp_num_notas):
        st.markdown(f'<div class="nota-input-card">', unsafe_allow_html=True)
        st.markdown(f"**🏪 Mercado / Local {i + 1}**")
        col1, col2 = st.columns([2, 3])
        with col1:
            rotulo = st.text_input(
                "Nome do local",
                key=f"cp_rotulo_{i}",
                placeholder=f"Ex: Mercado {chr(65 + i)}",
            )
        with col2:
            url = st.text_input(
                "Link da NFC-e",
                key=f"cp_url_{i}",
                placeholder="https://nfce.sefaz.xx.gov.br/...",
            )
        notas_input.append({"rotulo": rotulo, "url": url})
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("📊 Comparar Preços", type="primary", use_container_width=True):
        erros = []
        for i, nota in enumerate(notas_input):
            if not nota["url"].strip():
                erros.append(f"Link da nota {i + 1} não preenchido.")
            if not nota["rotulo"].strip():
                erros.append(f"Nome do mercado {i + 1} não preenchido.")
        if erros:
            for e in erros:
                st.error(e)
        else:
            st.session_state.cp_notas_input = notas_input
            st.session_state.cp_step = "processing"
            st.rerun()

# ── ETAPA 2: PROCESSAMENTO ────────────────────────────────────────────────────
elif st.session_state.cp_step == "processing":
    st.info("⚙️ Processando notas fiscais...")
    notas_processadas = []

    for i, nota in enumerate(st.session_state.cp_notas_input):
        with st.spinner(f"Lendo nota de **{nota['rotulo']}**..."):
            try:
                itens, total = processar_nfce(nota["url"], [])
                notas_processadas.append({
                    "rotulo": nota["rotulo"],
                    "itens":  itens,
                    "total":  total,
                })
                st.success(f"✅ {nota['rotulo']} — {len(itens)} itens | Total: R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            except Exception as e:
                st.error(f"❌ Erro ao processar nota de {nota['rotulo']}: {e}")
                if st.button("↩️ Voltar e corrigir"):
                    st.session_state.cp_step = "input"
                    st.rerun()
                st.stop()

    caminho = gerar_excel_comparacao(notas_processadas)
    st.session_state.cp_notas = notas_processadas
    st.session_state.cp_excel = caminho
    st.session_state.cp_step  = "result"
    st.rerun()

# ── ETAPA 3: RESULTADO ────────────────────────────────────────────────────────
elif st.session_state.cp_step == "result":
    notas = st.session_state.cp_notas

    st.success(f"✅ Comparativo de {len(notas)} notas gerado!")

    # Métricas por mercado
    cols = st.columns(len(notas))
    for col, nota in zip(cols, notas):
        with col:
            st.metric(
                label=f"🏪 {nota['rotulo']}",
                value=f"R$ {nota['total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                delta=f"{len(nota['itens'])} itens",
            )

    st.markdown("---")

    # Tabela comparativa interativa
    st.markdown("### 📊 Comparativo de Preços")

    rotulos = [n["rotulo"] for n in notas]
    mapa: dict[str, dict] = {}
    for nota in notas:
        for item in nota["itens"]:
            nome = item["Produto"].upper().strip()
            if nome not in mapa:
                mapa[nome] = {}
            mapa[nome][nota["rotulo"]] = item["Valor Unitário"]

    linhas = []
    for produto, precos in sorted(mapa.items()):
        linha = {"Produto": produto.title()}
        vals = [precos.get(r) for r in rotulos]
        numericos = [v for v in vals if v is not None]
        menor = min(numericos) if numericos else None

        for rotulo in rotulos:
            val = precos.get(rotulo)
            linha[rotulo] = val  # numérico para highlight

        linha["✅ Menor Preço"] = (
            f"{[r for r in rotulos if precos.get(r) == menor][0]}"
            if menor and len(numericos) > 1 else "—"
        )
        linhas.append(linha)

    df_comp = pd.DataFrame(linhas)

    # Highlight: verde = menor, vermelho = maior
    def highlight_row(row):
        styles = [""] * len(row)
        vals = {r: row[r] for r in rotulos if pd.notna(row.get(r))}
        if len(vals) < 2:
            return styles
        menor = min(vals.values())
        maior = max(vals.values())
        for i, col in enumerate(row.index):
            if col in vals:
                if vals[col] == menor:
                    styles[i] = "background-color:#C6EFCE; color:#276221; font-weight:bold"
                elif vals[col] == maior:
                    styles[i] = "background-color:#FFC7CE; color:#9C0006"
        return styles

    # Formatar colunas numéricas como moeda para exibição
    df_display = df_comp.copy()
    for r in rotulos:
        df_display[r] = df_display[r].apply(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if pd.notna(x) and x != "" else "—"
        )

    st.dataframe(df_comp.style.apply(highlight_row, axis=1), use_container_width=True, hide_index=True)

    st.info("🟢 Verde = menor preço | 🔴 Vermelho = maior preço — para produtos presentes em mais de uma nota")

    st.markdown("<br>", unsafe_allow_html=True)

    with open(st.session_state.cp_excel, "rb") as f:
        st.download_button(
            "⬇️ Baixar Comparativo em Excel",
            data=f,
            file_name="comparacao_precos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary",
        )

    if st.button("🔁 Nova Comparação", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k.startswith("cp_"):
                del st.session_state[k]
        st.rerun()
