import streamlit as st
from decimal import Decimal, getcontext

getcontext().prec = 20
st.set_page_config(page_title="HP 12C", layout="centered")

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except: pass

local_css("style.css")

if 'stack' not in st.session_state:
    st.session_state.stack = [Decimal('0')] * 4
    st.session_state.buffer = ""
    st.session_state.modifier = None

def handle_click(key, top=None, bot=None):
    mod = st.session_state.modifier
    actual_key = key
    if mod == 'f' and top: actual_key = top
    elif mod == 'g' and bot: actual_key = bot

    if actual_key in ['f', 'g']:
        st.session_state.modifier = actual_key
    else:
        execute_logic(actual_key)
        st.session_state.modifier = None

def execute_logic(key):
    s = st.session_state
    if key.isdigit() or key == ".":
        s.buffer += key
        s.stack[0] = Decimal(s.buffer)
    elif key == "ENTER":
        s.stack[3], s.stack[2], s.stack[1] = s.stack[2], s.stack[1], s.stack[0]
        s.buffer = ""
    elif key in ["+", "-", "*", "/"]:
        x, y = s.stack[0], s.stack[1]
        if key == "+": res = y + x
        elif key == "-": res = y - x
        elif key == "*": res = y * x
        elif key == "/": res = y / x if x != 0 else Decimal('0')
        s.stack[0] = res
        s.stack[1], s.stack[2], s.stack[3] = s.stack[2], s.stack[3], Decimal('0')
        s.buffer = ""
    elif key == "CLX":
        s.stack[0] = Decimal('0')
        s.buffer = ""

# --- INTERFACE ---
st.markdown('<div class="calc-container">', unsafe_allow_html=True)

# Visor
mod_indicator = st.session_state.modifier.upper() if st.session_state.modifier else ""
st.markdown(f'<div class="mod-indicator">{mod_indicator}</div>', unsafe_allow_html=True)
display_val = f"{st.session_state.stack[0]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
st.markdown(f'<div class="display">{display_val}</div>', unsafe_allow_html=True)

# Layout de Botões (Mapeamento Profissional)
def draw_button(main, t="", b="", css_class=""):
    st.markdown(f'<span class="top-lab">{t}</span>', unsafe_allow_html=True)
    if st.button(main, key=f"btn_{main}_{t}", on_click=handle_click, args=(main, t, b)): pass
    st.markdown(f'<span class="bot-lab">{b}</span>', unsafe_allow_html=True)

# Linha 1: Financeira
c1, c2, c3, c4, c5 = st.columns(5)
with c1: draw_button("n", "AMORT", "12*")
with c2: draw_button("i", "INT", "12/")
with c3: draw_button("PV", "NPV", "CFo")
with c4: draw_button("PMT", "RND", "CFj")
with c5: draw_button("FV", "IRR", "Nj")

# Linha 2: f, g e números
c1, c2, c3, c4, c5 = st.columns(5)
with c1: 
    st.markdown('<div class="f-btn">', unsafe_allow_html=True)
    draw_button("f")
    st.markdown('</div>', unsafe_allow_html=True)
with c2: 
    st.markdown('<div class="g-btn">', unsafe_allow_html=True)
    draw_button("g")
    st.markdown('</div>', unsafe_allow_html=True)
with c3: draw_button("7")
with c4: draw_button("8")
with c5: draw_button("9")

# Linha 3: Números e /
c1, c2, c3, c4, c5 = st.columns(5)
with c1: draw_button("STO")
with c2: draw_button("RCL")
with c3: draw_button("4")
with c4: draw_button("5")
with c5: draw_button("6")

# Linha 4: ENTER e Números
c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
with c1: draw_button("1")
with c2: draw_button("2")
with c3: draw_button("3")
with c4: 
    st.markdown('<div class="enter-btn">', unsafe_allow_html=True)
    st.button("ENTER", on_click=handle_click, args=("ENTER",))
    st.markdown('</div>', unsafe_allow_html=True)

# Linha 5: 0, ponto e operações
c1, c2, c3, c4, c5 = st.columns(5)
with c1: draw_button("0")
with c2: draw_button(".")
with c3: draw_button("+")
with c4: draw_button("-")
with c5: draw_button("*")

st.markdown('</div>', unsafe_allow_html=True)
