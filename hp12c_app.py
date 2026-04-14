import streamlit as st
from decimal import Decimal, getcontext

getcontext().prec = 20
st.set_page_config(page_title="HP 12C Engineering", layout="centered")

# --- INICIALIZAÇÃO DO HARDWARE VIRTUAL ---
if 'stack' not in st.session_state:
    st.session_state.stack = [Decimal('0')] * 4  # X, Y, Z, T
    st.session_state.last_x = Decimal('0')
    st.session_state.registers = [Decimal('0')] * 10 # R0-R9
    st.session_state.tvm = {'n': Decimal('0'), 'i': Decimal('0'), 'pv': Decimal('0'), 'pmt': Decimal('0'), 'fv': Decimal('0')}
    st.session_state.buffer = ""
    st.session_state.modifier = None
    st.session_state.error = None

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except: pass

local_css("style.css")

# --- LÓGICA DE MOVIMENTAÇÃO DE PILHA (STRICT RPN) ---
def push_stack(val):
    # Elevação real: T recebe Z, Z recebe Y, Y recebe X
    s = st.session_state
    s.stack[3] = s.stack[2]
    s.stack[2] = s.stack[1]
    s.stack[1] = s.stack[0]
    s.stack[0] = Decimal(str(val))

def drop_stack():
    # Queda após operação: Y recebe Z, Z recebe T, T mantém T
    s = st.session_state
    s.stack[1] = s.stack[2]
    s.stack[2] = s.stack[3]

# --- ENGINE DE EXECUÇÃO ---
def execute_logic(key):
    s = st.session_state
    s.error = None # Limpa erro a cada nova tecla

    try:
        # 1. Entrada Numérica
        if key.isdigit() or key == ".":
            s.buffer += key
            s.stack[0] = Decimal(s.buffer)

        # 2. Operações Aritméticas
        elif key in ["+", "-", "*", "/"]:
            s.last_x = s.stack[0]
            x, y = s.stack[0], s.stack[1]
            if key == "+": res = y + x
            elif key == "-": res = y - x
            elif key == "*": res = y * x
            elif key == "/":
                if x == 0: raise ZeroDivisionError
                res = y / x
            
            s.stack[0] = res
            drop_stack()
            s.buffer = ""

        # 3. ENTER Real
        elif key == "ENTER":
            s.stack[3] = s.stack[2]
            s.stack[2] = s.stack[1]
            s.stack[1] = s.stack[0]
            s.buffer = ""

        # 4. Storage & Recall (Simples: R0-R9 baseado no próximo buffer ou fixo em R0)
        elif key == "STO":
            s.registers[0] = s.stack[0] # Simplificado para R0 nesta versão
        elif key == "RCL":
            push_stack(s.registers[0])

        # 5. Financeiro (TVM Registers)
        elif key in ["n", "i", "PV", "PMT", "FV"]:
            s.tvm[key.lower()] = s.stack[0]
            s.buffer = ""

        # 6. Clears
        elif key == "CLX":
            s.stack[0] = Decimal('0')
            s.buffer = ""
        elif key == "fCLEAR REG":
            s.stack = [Decimal('0')] * 4
            s.tvm = {k: Decimal('0') for k in s.tvm}
            s.registers = [Decimal('0')] * 10
            s.buffer = ""

    except ZeroDivisionError:
        s.error = "Error 0"
    except Exception:
        s.error = "Error"

# --- INTERFACE ---
st.markdown('<div class="calc-container">', unsafe_allow_html=True)

# Visor com tratamento de erro
mod_text = st.session_state.modifier.upper() if st.session_state.modifier else ""
st.markdown(f'<div class="mod-indicator">{mod_text}</div>', unsafe_allow_html=True)

if st.session_state.error:
    st.markdown(f'<div class="display" style="color:#cc0000">{st.session_state.error}</div>', unsafe_allow_html=True)
else:
    val = f"{st.session_state.stack[0]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.markdown(f'<div class="display">{val}</div>', unsafe_allow_html=True)

# Grid de botões (Exemplo de linha financeira e comandos)
c1, c2, c3, c4, c5 = st.columns(5)
with c1: 
    if st.button("n", key="n"): execute_logic("n")
with c2: 
    if st.button("i", key="i"): execute_logic("i")
with c3: 
    if st.button("PV", key="pv"): execute_logic("PV")
with c4: 
    if st.button("PMT", key="pmt"): execute_logic("PMT")
with c5: 
    if st.button("FV", key="fv"): execute_logic("FV")

# Teclado Numérico (omitido aqui para brevidade, mas segue o padrão anterior)
# ...

st.markdown('</div>', unsafe_allow_html=True)
