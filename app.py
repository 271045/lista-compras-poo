# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime
import urllib.parse

class ListaComprasPro:
    def __init__(self):
        # Base de dados organizada pelas categorias do seu PDF
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
        texto_completo = cabecalho + corpo
        return f"https://wa.me/?text={urllib.parse.quote(texto_completo)}"

# --- Interface Streamlit ---
st.set_page_config(page_title="Super Lista Pro", page_icon="📝", layout="wide")
app = ListaComprasPro()

st.title("📝 Lista de Compras Categorizada")

# Barra Lateral (Sidebar) - Agora com o botão de envio aqui!
with st.sidebar:
    st.header("⚙️ Ferramentas")
    if st.button("🗑️ LIMPAR MARCAÇÕES", use_container_width=True):
        app.limpar_selecoes()
    
    st.divider()
    
    st.subheader("➕ Novo Item")
    cat_escolhida = st.selectbox("Categoria:", list(st.session_state.categorias.keys()))
    novo_nome = st.text_input("Produto:")
    if st.button("Adicionar Item", use_container_width=True):
        app.adicionar_item(cat_escolhida, novo_nome)

    st.divider()

    # --- BOTÃO WHATSAPP MOVIDO PARA CÁ ---
    # Coletamos os itens marcados para saber se o botão deve funcionar
    itens_selecionados_para_envio = []
    for chave, valor in st.session_state.items():
        if chave.startswith("check_") and valor:
            item_nome = chave.replace("check_", "")
            itens_selecionados_para_envio.append(item_nome)

    if st.button("🟢 ENVIAR PARA WHATSAPP", use_container_width=True):
        if itens_selecionados_para_envio:
            link_final = app.gerar_whatsapp(itens_selecionados_para_envio)
            st.markdown(f'''
                <a href="{link_final}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 16px;">
                        CONFIRMAR E ABRIR WHATSAPP [X]
                    </div>
                </a>
            ''',
