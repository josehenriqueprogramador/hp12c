import streamlit as st
from decimal import Decimal, getcontext

# 1. Configuração de Precisão (Essencial para finanças)
getcontext().prec = 20

# Configuração da página
st.set_page_config(page_title="HP 12C Digital", layout="centered")

# 2. Inicialização do Estado (Pilha RPN e Variáveis)
if 'stack' not in st.session_state:
    st.session_state.stack = [Decimal('0')] * 4  # X, Y, Z, T
    st.session_state.input_buffer = ""           # Para digitar números
    st.session_state.has_comma = False

# --- Lógica de Operações ---
def push_to_stack(value):
    st.session_state.stack[3] = st.session_state.stack[2]
    st.session_state.stack[2] = st.session_state.stack[1]
    st.session_state.stack[1] = st.session_state.stack[0]
    st.session_state.stack[0] = Decimal(str(value))

def handle_click(key):
    # Se for número
    if key.isdigit() or key == ".":
        if key == "." and st.session_state.has_comma:
            return
        if key == ".":
            st.session_state.has_comma = True
        
        st.session_state.input_buffer += key
        st.session_state.stack[0] = Decimal(st.session_state.input_buffer)
    
    # Se for ENTER
    elif key == "ENTER":
        push_to_stack(st.session_state.stack[0])
        st.session_state.input_buffer = ""
        st.session_state.has_comma = False

    # Se for Operação
    elif key in ["+", "-", "*", "/"]:
        x = st.session_state.stack[0]
        y = st.session_state.stack[1]
        
        if key == "+": res = y + x
        elif key == "-": res = y - x
        elif key == "*": res = y * x
        elif key == "/": res = y / x if x != 0 else Decimal('0')
        
        st.session_state.stack[0] = res
        st.session_state.stack[1] = st.session_state.stack[2]
        st.session_state.stack[2] = st.session_state.stack[3]
        st.session_state.input_buffer = ""
        st.session_state.has_comma = False

# 3. CSS Customizado (O seu estilo aprimorado para Streamlit)
st.markdown(f"""
<style>
    /* Esconde elementos nativos do Streamlit para focar na calculadora */
    #MainMenu, footer, header {{visibility: hidden;}}
    .stApp {{ background: #1a1a1a; }}

    .calc-container {{
        background: #2b2b2b;
        padding: 20px;
        border-radius: 15px;
        width: 320px;
        margin: auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }}

    .display {{
        background: #9fbfa0;
        color: #1a1a1a;
        font-family: 'Courier New', monospace;
        font-size: 32px;
        text-align: right;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
        box-shadow: inset 2px 2px 8px #6d8f6e;
        min-height: 50px;
    }}

    /* Estilização dos botões nativos do Streamlit para parecerem HP */
    div.stButton > button {{
        background: #3a3a3a !important;
        color: white !important;
        border-radius: 6px !important;
        height: 60px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: inset 1px 1px 0px #555, 2px 2px 5px #000 !important;
        transition: all 0.1s;
    }}

    div.stButton > button:active {{
        transform: translateY(2px);
        box-shadow: none !important;
    }}

    /* Cores específicas */
    .stButton.enter-btn button {{ background: #4a6fa5 !important; }}
    .stButton.num-btn button {{ background: #2f2f2f !important; }}
    
    .label-box {{ text-align: center; }}
    .top-lab {{ color: orange; font-size: 10px; font-weight: bold; display: block; }}
    .bot-lab {{ color: #6ec1ff; font-size: 10px; font-weight: bold; display: block; }}
</style>
""", unsafe_allow_html=True)

# 4. Interface e Layout
with st.container():
    st.markdown('<div class="calc-container">', unsafe_allow_html=True)
    
    # Display formatado
    val_display = f"{st.session_state.stack[0]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.markdown(f'<div class="display">{val_display}</div>', unsafe_allow_html=True)

    # Grid de botões
    # Linha Financeira
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<span class="top-lab">NPV</span>', unsafe_allow_html=True)
        if st.button("PV", key="btn_pv"): handle_click("PV")
        st.markdown('<span class="bot-lab">CFo</span>', unsafe_allow_html=True)
    with c2:
        st.markdown('<span class="top-lab">IRR</span>', unsafe_allow_html=True)
        if st.button("PMT", key="btn_pmt"): handle_click("PMT")
        st.markdown('<span class="bot-lab">CFj</span>', unsafe_allow_html=True)
    with c3:
        st.markdown('<span class="top-lab">AMORT</span>', unsafe_allow_html=True)
        if st.button("FV", key="btn_fv"): handle_click("FV")
        st.markdown('<span class="bot-lab">Nj</span>', unsafe_allow_html=True)
    with c4:
        st.markdown('<span class="top-lab">INT</span>', unsafe_allow_html=True)
        if st.button("/", key="btn_div"): handle_click("/")
        st.markdown('<span class="bot-lab">12/</span>', unsafe_allow_html=True)

    # Teclado Numérico e ENTER
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("7", key="7", on_click=handle_click, args=("7",))
    with c2: st.button("8", key="8", on_click=handle_click, args=("8",))
    with c3: st.button("9", key="9", on_click=handle_click, args=("9",))
    with c4: st.button("*", key="*", on_click=handle_click, args=("*",))

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("4", key="4", on_click=handle_click, args=("4",))
    with c2: st.button("5", key="5", on_click=handle_click, args=("5",))
    with c3: st.button("6", key="6", on_click=handle_click, args=("6",))
    with c4: st.button("-", key="-", on_click=handle_click, args=("-",))

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("1", key="1", on_click=handle_click, args=("1",))
    with c2: st.button("2", key="2", on_click=handle_click, args=("2",))
    with c3: st.button("3", key="3", on_click=handle_click, args=("3",))
    with c4: st.button("+", key="+", on_click=handle_click, args=("+",))

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: 
        if st.button("ENTER", key="ent", use_container_width=True): handle_click("ENTER")
    with c2: st.button("0", key="0", on_click=handle_click, args=("0",))
    with c3: st.button(".", key="dot", on_click=handle_click, args=(".",))

    st.markdown('</div>', unsafe_allow_html=True)

# Debug da Pilha (Opcional - Útil para Ciência de Dados)
with st.expander("Visualizar Pilha RPN (Stack)"):
    st.write(f"**X:** {st.session_state.stack[0]}")
    st.write(f"**Y:** {st.session_state.stack[1]}")
    st.write(f"**Z:** {st.session_state.stack[2]}")
    st.write(f"**T:** {st.session_state.stack[3]}")
