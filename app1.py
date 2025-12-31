import streamlit as st
import time

# Configuração inicial da página
st.set_page_config(page_title="App Sequencial", layout="centered")

# Inicialização do estado da navegação
if 'step' not in st.session_state:
    st.session_state.step = 1

# --- Funções de Navegação ---
def next_step():
    st.session_state.step += 1

def reset_app():
    st.session_state.step = 1

# --- Renderização das Páginas ---

# ETAPA 1: INPUT
if st.session_state.step == 1:
    st.title("Step 1: Entrada de Dados")
    
    url_input = st.text_input("Insira o link URL:", placeholder="https://exemplo.com")
    text_input = st.text_input("Insira o texto descritivo:", placeholder="Digite algo aqui...")
    
    if st.button("Próxima Etapa"):
        next_step()

# ETAPA 2: PROCESSAMENTO
elif st.session_state.step == 2:
    st.title("Step 2: Processamento")
    
    st.write("Estamos preparando tudo para você...")
    
    # Exemplo visual da barra de progresso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("Iniciando processo...")
    progress_bar.progress(50) # Apenas visual, parado em 50%
    
    if st.button("Finalizar Processamento"):
        next_step()

# ETAPA 3: RESULTADO
elif st.session_state.step == 3:
    st.title("Step 3: Resultado")
    
    st.success("Processamento concluído com sucesso!")
    
    # Botão de download (simulado com um arquivo vazio)
    st.download_button(
        label="Baixar arquivo de resultado",
        data="Conteúdo do arquivo de exemplo",
        file_name="resultado_final.txt",
        mime="text/plain"
    )
    
    if st.button("Retornar ao Início"):
        reset_app()