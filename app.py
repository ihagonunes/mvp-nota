import streamlit as st

st.set_page_config(
    page_title="NFC-e Suite | Inteligência Fiscal",
    page_icon="🧾",
    layout="wide",
)

# ── CSS global ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Remove padding padrão do Streamlit */
  .block-container { padding-top: 2rem; padding-bottom: 3rem; }

  /* ── Hero ── */
  .hero {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A5F 60%, #1E6FD9 100%);
    border-radius: 16px;
    padding: 3.5rem 2.5rem;
    text-align: center;
    margin-bottom: 2.5rem;
  }
  .hero h1 { color: #FFFFFF; font-size: 2.8rem; font-weight: 800; margin: 0 0 .6rem; }
  .hero p  { color: #CBD5E1; font-size: 1.2rem; margin: 0 0 2rem; }
  .hero-badge {
    display: inline-block;
    background: rgba(255,255,255,.12);
    color: #93C5FD;
    border-radius: 999px;
    padding: .35rem 1rem;
    font-size: .85rem;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(147,197,253,.3);
  }

  /* ── Steps ── */
  .steps-wrap { display: flex; gap: 1rem; margin-bottom: 2.5rem; flex-wrap: wrap; }
  .step-box {
    flex: 1; min-width: 180px;
    background: #EBF0F8;
    border-radius: 12px;
    padding: 1.2rem 1rem;
    text-align: center;
    border-top: 4px solid #1E6FD9;
  }
  .step-num { font-size: 1.8rem; font-weight: 800; color: #1E6FD9; }
  .step-txt { font-size: .9rem; color: #334155; margin-top: .4rem; }

  /* ── Feature cards ── */
  .card-wrap { display: flex; gap: 1.2rem; flex-wrap: wrap; margin-bottom: 2.5rem; }
  .card {
    flex: 1; min-width: 240px;
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.8rem 1.5rem;
    border: 1px solid #DBEAFE;
    box-shadow: 0 2px 12px rgba(30,111,217,.08);
    transition: transform .2s, box-shadow .2s;
  }
  .card:hover { transform: translateY(-4px); box-shadow: 0 8px 28px rgba(30,111,217,.16); }
  .card-icon { font-size: 2.4rem; margin-bottom: .7rem; }
  .card-title { font-size: 1.1rem; font-weight: 700; color: #0F172A; margin-bottom: .4rem; }
  .card-desc  { font-size: .88rem; color: #475569; line-height: 1.5; }
  .card-tag {
    display: inline-block;
    background: #DBEAFE; color: #1E40AF;
    border-radius: 999px; font-size: .75rem;
    padding: .2rem .7rem; margin-top: .8rem;
  }

  /* ── Personas ── */
  .persona-wrap { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 2.5rem; }
  .persona {
    flex: 1; min-width: 160px;
    background: #F8FAFC;
    border-radius: 12px;
    padding: 1.2rem 1rem;
    text-align: center;
    border: 1px solid #E2E8F0;
  }
  .persona-icon { font-size: 2rem; }
  .persona-title { font-size: .95rem; font-weight: 700; color: #1E3A5F; margin: .5rem 0 .2rem; }
  .persona-desc  { font-size: .82rem; color: #64748B; }

  /* ── Section titles ── */
  .section-title {
    font-size: 1.5rem; font-weight: 700;
    color: #0F172A; margin-bottom: 1rem;
    padding-bottom: .5rem;
    border-bottom: 3px solid #1E6FD9;
    display: inline-block;
  }

  /* ── Footer ── */
  .footer {
    text-align: center; color: #94A3B8;
    font-size: .82rem; margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #E2E8F0;
  }
  .footer a { color: #1E6FD9; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🇧🇷 100% gratuito · Sem cadastro · Dados ficam no seu computador</div>
  <h1>🧾 NFC-e Suite</h1>
  <p>Transforme sua nota fiscal em inteligência financeira.<br>
  Em segundos, divida contas, gere reembolsos e compare preços — tudo a partir do QR Code do cupom.</p>
</div>
""", unsafe_allow_html=True)

# ── Como funciona ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">⚡ Como funciona</div>', unsafe_allow_html=True)
st.markdown("""
<div class="steps-wrap">
  <div class="step-box">
    <div class="step-num">1</div>
    <div class="step-txt"><strong>Escaneie o QR Code</strong> do cupom e copie o link da NFC-e</div>
  </div>
  <div class="step-box">
    <div class="step-num">2</div>
    <div class="step-txt"><strong>Cole o link</strong> na ferramenta desejada e preencha as informações</div>
  </div>
  <div class="step-box">
    <div class="step-num">3</div>
    <div class="step-txt"><strong>Baixe a planilha</strong> Excel pronta com tudo organizado e calculado</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Feature Cards ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🛠️ Ferramentas disponíveis</div>', unsafe_allow_html=True)
st.markdown("""
<div class="card-wrap">

  <div class="card">
    <div class="card-icon">🛒</div>
    <div class="card-title">Divisão de Compras</div>
    <div class="card-desc">
      Informe quem vai rachar a conta e receba uma planilha com o valor exato
      de cada pessoa. Perfeito para repúblicas, famílias e grupos de amigos.
    </div>
    <span class="card-tag">👥 Uso pessoal</span>
  </div>

  <div class="card">
    <div class="card-icon">📋</div>
    <div class="card-title">Reembolso Empresarial</div>
    <div class="card-desc">
      Gere um relatório profissional de reembolso com cabeçalho, tabela de
      itens, total e aba de aprovação. Chega de digitar nota por nota.
    </div>
    <span class="card-tag">🏢 Uso corporativo</span>
  </div>

  <div class="card">
    <div class="card-icon">💰</div>
    <div class="card-title">Comparação de Preços</div>
    <div class="card-desc">
      Cole notas de mercados diferentes e veja lado a lado qual tem o menor
      preço em cada produto. Os melhores preços ficam destacados em verde.
    </div>
    <span class="card-tag">📊 Análise de consumo</span>
  </div>

</div>
""", unsafe_allow_html=True)

# ── Navegação (botões reais do Streamlit) ─────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🛒 Ir para Divisão de Compras", use_container_width=True):
        st.switch_page("pages/1_Divisão_de_Compras.py")
with col2:
    if st.button("📋 Ir para Reembolso Empresarial", use_container_width=True):
        st.switch_page("pages/2_Reembolso_Empresarial.py")
with col3:
    if st.button("💰 Ir para Comparação de Preços", use_container_width=True):
        st.switch_page("pages/3_Comparação_de_Preços.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── Quem usa ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">👥 Quem usa?</div>', unsafe_allow_html=True)
st.markdown("""
<div class="persona-wrap">
  <div class="persona">
    <div class="persona-icon">🏠</div>
    <div class="persona-title">Repúblicas</div>
    <div class="persona-desc">Divida as compras do mês sem briga, com planilha pronta para todos.</div>
  </div>
  <div class="persona">
    <div class="persona-icon">👔</div>
    <div class="persona-title">Profissionais</div>
    <div class="persona-desc">Gere relatórios de reembolso em segundos, sem digitar item por item.</div>
  </div>
  <div class="persona">
    <div class="persona-icon">🎉</div>
    <div class="persona-title">Grupos & Eventos</div>
    <div class="persona-desc">Churrasco, viagem, festa — cada um sabe exatamente o que deve.</div>
  </div>
  <div class="persona">
    <div class="persona-icon">🔍</div>
    <div class="persona-title">Consumidores Atentos</div>
    <div class="persona-desc">Compare preços entre mercados e saiba onde seu dinheiro rende mais.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Onde obter o link ─────────────────────────────────────────────────────────
with st.expander("❓ Como obter o link da NFC-e?"):
    st.markdown("""
    1. **Peça o cupom fiscal** no caixa (impresso ou por WhatsApp/e-mail)
    2. **Escaneie o QR Code** com o celular — ele abre o site da Sefaz com a nota
    3. **Copie o link** do navegador e cole na ferramenta desejada
    
    > 💡 A NFC-e é um padrão nacional da Receita Federal, válido em todos os estados.
    """)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Construído com ❤️ usando <strong>Python · Streamlit · openpyxl · BeautifulSoup</strong><br>
  <a href="https://github.com" target="_blank">📁 GitHub</a> &nbsp;|&nbsp;
  Dados processados localmente — sua nota nunca sai do seu dispositivo.
</div>
""", unsafe_allow_html=True)