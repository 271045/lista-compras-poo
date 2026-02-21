# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime
import urllib.parse
try:
    import pytz
except ImportError:
    pass

class ListaComprasPro:
    def __init__(self):
        if 'categorias' not in st.session_state:
            st.session_state.categorias = {
                "Mercearia 🍞": ["Arroz", "Feijão", "Açúcar", "Café", "Macarrão", "Óleo", "Farinha de Trigo", "Milho Verde", "Extrato de Tomate", "Biscoitos", "Maionese", "Azeite"],
                "Limpeza 🧼": ["Sabão em Pó", "Sabão em Barra", "Desinfetante", "Água Sanitária", "Detergente", "Amaciante", "Álcool", "Saco de Lixo", "Bombril", "Veja", "Multiuso"],
                "Higiene 🪥": ["Pasta de Dente", "Sabonete", "Shampoo", "Condicionador", "Desodorante", "Papel Higiênico", "Fio Dental", "Algodão"],
                "Frios & Laticínios 🧀": ["Mussarela", "Presunto", "Leite", "Manteiga", "Iogurte", "Requeijão", "Ovos", "Salsicha", "Margarina"],
                "Frutas & Verduras 🍎": ["Banana", "Maçã", "Batata", "Cebola", "Alho", "Tomate", "Alface", "Limão", "Cenoura"],
                "Açougue 🥩": ["Carne Moída", "Bife", "Frango", "Linguiça", "Bacon", "Calabresa", "Costelinha"],
                "Outros 📦": []
            }

    def adicionar_item(self, nome):
        if nome and nome not in st.session_state.categorias["Outros 📦"]:
            st.session_state.categorias["Outros 📦"].append(nome)
            st.rerun()

    def limpar_selecoes(self):
        for chave in st.session_state.keys():
            if chave.startswith("check_"):
                st.session_state[chave] = False
        st.rerun()

    def gerar_whatsapp(self, lista_final):
        lista_final.sort()
        fuso_br = pytz.timezone('America/Sao_Paulo')
        data_br = datetime.now(fuso_br).strftime("%d/%m/%Y")
        
        cabecalho = f"--- LISTA DE COMPRAS ({data_br}) ---\n\n"
        corpo = ""
        for item in lista_final:
            corpo += f"[X] {item}\n"
        
        assinatura_wa = "\n\nby ®rvrs"
        texto_completo = cabecalho + corpo + assinatura_wa
        return f"https://wa.me/?text={urllib.parse.quote(texto_completo)}"

# --- Interface Streamlit ---
st.set_page_config(page_title="Super Lista Pro", page_icon="📝", layout="wide")

# Estilo para remover margens desnecessárias agora que não há colunas duplas por item
st.markdown("""
    <style>
    .stCheckbox { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

app = ListaComprasPro()

st.title("📝 Lista de Compras")

with st.sidebar:
    st.header("⚙️ Painel")
    if st.button("🗑️ LIMPAR MARCAÇÕES", use_container_width=True):
        app.limpar_selecoes()
    
    st.divider()
    
    st.subheader("➕ Novo Item (Outros)")
    novo_nome = st.text_input("Nome do produto:")
    if st.button("Adicionar em Outros", use_container_width=True):
        app.adicionar_item(novo_nome)

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
        st.info("Marque itens na lista.")

# --- Listagem Principal ---
col1, col2 = st.columns(2)
todas_cats = list(st.session_state.categorias.items())
ponto = (len(todas_cats) + 1) // 2

for i, (cat, produtos) in enumerate(todas_cats):
    coluna = col1 if i < ponto else col2
    with coluna:
        st.subheader(cat)
        if not produtos and cat == "Outros 📦":
            st.write("*Adicione itens na lateral.*")
        for p in produtos:
            # Removida a coluna da lixeira, agora é uma linha simples
            st.checkbox(p, key=f"check_{p}")

# --- Rodapé ---
st.write("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>2026 Lista de Compras | Desenvolvido por ®rvrs</p>", unsafe_allow_html=True)
