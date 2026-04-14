import streamlit as st
from decimal import Decimal, getcontext
import math

getcontext().prec = 20
st.set_page_config(page_title="HP 12C Profissional", layout="centered")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("style.css")
except:
    pass

# --- ESTADO DA CALCULADORA ---
if 'stack' not in st.session_state:
    st.session_state.stack = [Decimal('0')] * 4  # X, Y, Z, T
    st.session_state.tvm = {'n': None, 'i': None, 'pv': None, 'pmt': None, 'fv': None}
    st.session_state.buffer = ""
    st.session_state.modifier = None

# --- MOTORES DE CÁLCULO ---

def solve_tvm(target):
    """Resolve a equação fundamental: PV(1+i)^n + PMT[(1+i)^n - 1]/i + FV = 0"""
    t = st.session_state.tvm
    # Converte para float para cálculos de potência/log
    n = float(t['n']) if t['n'] else 0
    i = float(t['i']) / 100 if t['i'] else 0
    pv = float(t['pv']) if t['pv'] else 0
    pmt = float(t['pmt']) if t['pmt'] else 0
    fv = float(t['fv']) if t['fv'] else 0

    try:
        if target == 'fv':
            res = -(pv * (1+i)**n + pmt * (((1+i)**n - 1)/i)) if i != 0 else -(pv + pmt * n)
        elif target == 'pv':
            res = -(fv / (1+i)**n + pmt * (((1+i)**n - 1)/(i * (1+i)**n))) if i != 0 else -(fv + pmt * n)
        elif target == 'n':
            # Simplificado para PV e FV apenas
            res = math.log(-fv/pv) / math.log(1+i)
        
        st.session_state.stack[0] = Decimal(str(round(res, 4)))
    except:
        st.session_state.stack[0] = "Error"

def handle_click(key, top=None, bot=None):
    mod = st.session_state.modifier
    actual_key = key
    if mod == 'f': actual_key = top if top else key
    if mod == 'g': actual_key = bot if bot else key

    if actual_key in ['f', 'g']:
        st.session_state.modifier = actual_key
        return

    process_logic(actual_key)
    st.session_state.modifier = None

def process_logic(key):
    s = st.session_state
    
    # 1. Entrada Numérica
    if key.isdigit() or key == ".":
        s.buffer += key
        s.stack[0] = Decimal(s.buffer)
    
    # 2. Operações RPN
    elif key == "ENTER":
        s.stack[3], s.stack[2], s.stack[1] = s.stack[2], s.stack[1], s.stack[0]
        s.buffer = ""
    
    elif key in ["+", "-", "*", "/"]:
        x, y = s.stack[0], s.stack[1]
        if key == "+": res = y + x
        if key == "-": res = y - x
        if key == "*": res = y * x
        if key == "/": res = y / x if x != 0 else Decimal('0')
        
        s.stack[0] = res
        s.stack[1], s.stack[2], s.stack[3] = s.stack[2], s.stack[3], Decimal('0')
        s.buffer = ""

    # 3. Teclas Financeiras (TVM)
    elif key in ['n', 'i', 'PV', 'PMT', 'FV']:
        if s.buffer != "": # Se digitou algo, armazena
            s.tvm[key.lower()] = s.stack[0]
            s.buffer = ""
        else: # Se não digitou, calcula o valor faltante
            solve_tvm(key.lower())

# --- INTERFACE ---
st.markdown('<div class="calc-container">', unsafe_allow_html=True)

# Display
mod_display = st.session_state.modifier.upper() if st.session_state.modifier else ""
st.markdown(f'<div class="mod-indicator">{mod_display}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="display">{st.session_state.stack[0]:,.2f}</div>', unsafe_allow_html=True)

# Grid (Exemplo de 2 linhas completas)
rows = [
    [("n", "AMORT", "12*"), ("i", "INT", "12/"), ("PV", "NPV", "CFo"), ("FV", "IRR", "CFj")],
    [("7", "", ""), ("8", "", ""), ("9", "", ""), ("/", "", "")]
]

for row in rows:
    cols = st.columns(4)
    for i, (main, t, b) in enumerate(row):
        with cols[i]:
            st.markdown(f'<span class="top-lab">{t}</span>', unsafe_allow_html=True)
            st.button(main, key=f"btn_{main}", on_click=handle_click, args=(main, t, b))
            st.markdown(f'<span class="bot-lab">{b}</span>', unsafe_allow_html=True)

# Linha do ENTER e 0
c1, c2, c3 = st.columns([2, 1, 1])
with c1: 
    st.markdown('<div class="enter-btn">', unsafe_allow_html=True)
    st.button("ENTER", on_click=handle_click, args=("ENTER",))
    st.markdown('</div>', unsafe_allow_html=True)
with c2: st.button("0", on_click=handle_click, args=("0",))
with c3: st.button(".", on_click=handle_click, args=(".",))

st.markdown('</div>', unsafe_allow_html=True)
