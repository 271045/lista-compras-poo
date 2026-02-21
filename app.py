# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime
import urllib.parse

class ListaComprasPro:
    def __init__(self):
        if 'categorias' not in st.session_state:
            st.session_state.categorias = {
                "Mercearia 🍞": ["Arroz", "Feijão", "Açúcar", "Café", "Macarrão", "Óleo", "Farinha de Trigo", "Milho Verde", "Extrato de Tomate", "Biscoitos", "Maionese", "Azeite"],
                "Limpeza 🧼": ["Sabão em Pó", "Sabão em Barra", "Desinfetante", "Água Sanitária", "Detergente", "Amaciante", "Álcool", "Saco de Lixo", "Bombril", "Veja", "Multiuso"],
                "Higiene 🪥": ["Pasta de Dente", "Sabonete", "Shampoo", "Condicionador", "Desodorante", "Papel Higiênico", "Fio Dental", "Algodão"],
                "Frios & Laticínios 🧀": ["Mussarela", "Presunto", "Leite", "Manteiga", "Iogurte", "Requeijão", "Ovos", "Salsicha", "Margarina"],
                "Frutas & Verduras 🍎": ["Banana", "Maçã", "Batata", "Cebola", "Alho", "Tomate", "Alface", "Limão", "Cenoura"],
                "Açougue 🥩": ["Carne Moída", "Bife", "Frango", "Linguiça", "Bacon", "Calabresa", "Costelinha"]
            }

    def adicionar_item(self, categoria, nome):
        if nome and nome not in st.session_state.categorias[categoria]:
            st.session_state.categorias[categoria].append(nome)
            st.rerun()

    def remover_item(self, categoria, nome):
        st.session_state.categorias[categoria].remove(nome)
        st.rerun()

    def limpar_selecoes(self):
        for chave in st.session_state.keys():
            if chave.startswith("check_"):
                st.session_state[chave] = False
        st.rerun()

    def gerar_whatsapp(self, lista_final):
        lista_final.sort()
        data = datetime.now().strftime("%d/%m/%Y")
        cabecalho = f"--- LISTA DE COMPRAS ({data}) ---\n\n"
        corpo = ""
        for item in lista_final:
            corpo += f"[X] {item}\n"
        
        assinatura_wa = "\n\nby ®rvrs"
        texto_completo = cabecalho + corpo + assinatura_wa
        return f"https://wa.me/?text={urllib.parse.quote(texto_completo)}"

# --- Configuração da Página ---
st.set_page_config(page_title="Super Lista Pro", page_icon="📝", layout="wide")

# CSS Simplificado: Apenas para ajustar a altura dos botões de lixeira
st.markdown("""
    <style>
    .stButton > button {
        padding: 0px 5px !important;
        height: 1.8rem !important;
        border: none !important;
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

app = ListaComprasPro()

st.title("📝 Lista de Compras")

# Barra Lateral (Sidebar)
with st.sidebar:
    st.header("⚙️ Painel")
    if st.button("🗑️ LIMPAR MARCAÇÕES", use_container_width=True):
        app.limpar_selecoes()
    
    st.divider()
    
    st.subheader("➕ Novo Item")
    cat_escolhida = st.selectbox("Categoria:", list(st.session_state.categorias.keys()))
    novo_nome = st.text_input("Produto:")
    if st.button("Adicionar Item", use_container_width=True):
        app.adicionar_item(cat_escolhida, novo_nome)

    st.divider()

    selecionados = [k.replace("check_", "") for k, v in st.session_state.items() if k.startswith("check_") and v]

    if selecionados:
        link = app.gerar_whatsapp(selecionados)
        st.markdown(f"""
            <a href="{link}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 18px;">
                    ENVIAR LISTA [X]
                </div>
            </a>
        """, unsafe_allow_html=True)
    else:
        st.info("Marque os itens abaixo.")

# --- Listagem Principal ---
col1, col2 = st.columns(2)
todas_cats = list(st.session_state.categorias.items())
ponto = (len(todas_cats) + 1) // 2

for i, (cat, produtos) in enumerate(todas_cats):
    coluna = col1 if i < ponto else col2
    with coluna:
        st.subheader(cat)
        for p in produtos:
            # Layout de linha: Checkbox ocupa 80%, Lixeira ocupa 20%
            c_check, c_del = st.columns([0.8, 0.2])
            c_check.checkbox(p, key=f"check_{p}")
            if c_del.button("🗑️", key=f"del_{p}"):
                app.remover_item(cat, p)

# --- Rodapé ---
st.write("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>2026 Lista de Compras | Desenvolvido por ®rvrs</p>", unsafe_allow_html=True)
