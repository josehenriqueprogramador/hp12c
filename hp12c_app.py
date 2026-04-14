import streamlit as st
from decimal import Decimal, getcontext

# Configurações iniciais
getcontext().prec = 20
st.set_page_config(page_title="HP 12C Pro", layout="centered")

# Função para carregar o CSS externo
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Inicialização do Estado
if 'stack' not in st.session_state:
    st.session_state.stack = [Decimal('0')] * 4
    st.session_state.input_buffer = ""
    st.session_state.modifier = None
    st.session_state.tvm = {'n': 0, 'i': 0, 'pv': 0, 'pmt': 0, 'fv': 0}

# Lógica de Cliques
def handle_click(main_key, top_key=None, bot_key=None):
    if main_key in ['f', 'g']:
        st.session_state.modifier = main_key
        return

    mod = st.session_state.modifier
    target = main_key
    if mod == 'f' and top_key: target = top_key
    elif mod == 'g' and bot_key: target = bot_key

    # Aqui entraria a chamada para as funções financeiras reais
    execute_action(target)
    st.session_state.modifier = None

def execute_action(key):
    # Lógica simplificada de input numérico
    if key.isdigit() or key == ".":
        st.session_state.input_buffer += key
        st.session_state.stack[0] = Decimal(st.session_state.input_buffer)
    elif key == "ENTER":
        st.session_state.stack[1] = st.session_state.stack[0]
        st.session_state.input_buffer = ""

# --- INTERFACE ---
st.markdown('<div class="calc-container">', unsafe_allow_html=True)

# Visor
mod_text = st.session_state.modifier.upper() if st.session_state.modifier else ""
st.markdown(f'<div class="mod-indicator">{mod_text}</div>', unsafe_allow_html=True)
display_val = f"{st.session_state.stack[0]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
st.markdown(f'<div class="display">{display_val}</div>', unsafe_allow_html=True)

# Teclado (Exemplo de linha)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="f-btn">', unsafe_allow_html=True)
    st.button("f", on_click=handle_click, args=("f",))
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="g-btn">', unsafe_allow_html=True)
    st.button("g", on_click=handle_click, args=("g",))
    st.markdown('</div>', unsafe_allow_html=True)

# Linha Numérica
c1, c2, c3, c4 = st.columns(4)
with c1: st.button("7", on_click=handle_click, args=("7",))
with c2: st.button("8", on_click=handle_click, args=("8",))
with c3: st.button("9", on_click=handle_click, args=("9",))
with c4: st.button("/", on_click=handle_click, args=("/",))

st.markdown('</div>', unsafe_allow_html=True)
