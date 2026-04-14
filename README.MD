# 🧮 HP 12C Digital - High Precision Edition

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.20+-FF4B4B.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Uma implementação fiel e moderna da lendária calculadora financeira HP 12C. Este projeto combina a experiência clássica da **Notação Polonesa Reversa (RPN)** com o poder do **Python** para garantir precisão absoluta em cálculos financeiros e análise de dados.

> **Status do Projeto:** 🚀 Em desenvolvimento ativo.

---

## 🛠️ Tecnologias Utilizadas

- **Python:** Linguagem core do projeto.
- **Streamlit:** Framework para a interface web.
- **Decimal Library:** Aritmética rigorosa de até 20 casas decimais.
- **CSS3 Customizado:** Layout fiel ao design industrial clássico.

---

## 🚀 Funcionalidades

- [x] **Lógica RPN:** Sistema de pilha (Stack) com registros X, Y, Z e T.
- [x] **Interface Retro:** Design baseado no layout original com modificadores `f` (laranja) e `g` (azul).
- [x] **Gestão de Estado:** Persistência de dados via `st.session_state`.
- [x] **Aritmética de Precisão:** Uso de `Decimal` para evitar erros de ponto flutuante.

---

## ⚙️ Como Executar

Se estiver no **Termux** ou PC:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/Josehenriqueprogramador/hp12c.git](https://github.com/Josehenriqueprogramador/hp12c.git)
   cd hp12c
