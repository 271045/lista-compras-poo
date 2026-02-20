# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime
import urllib.parse

class ListaComprasPro:
    def __init__(self):
        # Base de dados baseada no seu PDF
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
        
        # Estratégia: Usar um caractere que o WhatsApp entende como "visto"
        # Em vez de tentar enviar o desenho, enviamos a codificação segura
        cabecalho = f"*LISTA DE COMPRAS - {data}*\n\n"
        corpo = ""
        for item in lista_final:
            # O código %E2%9C%85 é interpretado diretamente pelo navegador como ✅
            corpo += "- " + item + "\n"
        
        texto_completo = cabecalho + corpo
        
        # Fazemos a substituição do traço pelo código do emoji na URL final
        link_safe = urllib.parse.quote(texto_completo)
        link_final = link_safe.replace("-", "%E2%9C%85")
        
        return f"https://wa.me/?text={link_final}"

# --- Interface ---
st.set_page_config(page_title="Super Lista Pro", page_icon="📝", layout="wide")
app = ListaComprasPro()

st.title("📝 Lista de Compras Categorizada")

with st.sidebar:
    st.header("⚙️ Opções")
    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        app.limpar_selecoes()
    st.divider()
    st.subheader("➕ Novo Item")
    cat_escolhida = st.selectbox("Categoria:", list(st.session_state.categorias.keys()))
    novo_nome = st.text_input("Produto:")
    if st.button("Adicionar"):
        app.adicionar_item(cat_escolhida, novo_nome)

col1, col2 = st.columns(2)
itens_selecionados = []
todas_categorias = list(st.session_state.categorias.items())
ponto_corte = len(todas_categorias) // 2

for i, (cat, produtos) in enumerate(todas_categorias):
    coluna_atual = col1 if i < ponto_corte else col2
    with coluna_atual:
        st.subheader(cat)
        for p in produtos:
            c_check, c_del = st.columns([5, 1])
            if c_check.checkbox(p, key=f"check_{p}"):
                itens_selecionados.append(p)
            if c_del.button("❌", key=f"del_{p}"):
                app.remover_item(cat, p)

st.divider()

if st.button("🟢 ENVIAR LISTA PARA O WHATSAPP", use_container_width=True):
    if itens_selecionados:
        link_final = app.gerar_whatsapp(itens_selecionados)
        # Usamos um botão HTML direto para evitar que o Streamlit mude o link
        st.markdown(f'<a href="{link_final}" target="_blank" style="text-decoration: none;"><div style="background-color: #25D366; color: white; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 22px;">CONFIRMAR ENVIO ✅</div></a>', unsafe_allow_html=True)
    else:
        st.warning("Selecione os itens antes de enviar.")
