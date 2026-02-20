import streamlit as st
from datetime import datetime
import urllib.parse

class ListaComprasPro:
    def __init__(self):
        # Organização dos itens por categorias conforme o PDF enviado
        if 'categorias' not in st.session_state:
            st.session_state.categorias = {
                "Mercearia 🍞": ["Arroz", "Feijão", "Açúcar", "Café", "Macarrão", "Óleo", "Farinha de Trigo", "Milho Verde", "Extrato de Tomate", "Biscoitos"],
                "Limpeza 🧼": ["Sabão em Pó", "Sabão em Barra", "Desinfetante", "Água Sanitária", "Detergente", "Amaciante", "Álcool", "Saco de Lixo", "Bombril", "Veja"],
                "Higiene 🪥": ["Pasta de Dente", "Sabonete", "Shampoo", "Condicionador", "Desodorante", "Papel Higiênico", "Fio Dental", "Algodão"],
                "Frios & Laticínios 🧀": ["Mussarela", "Presunto", "Leite", "Manteiga", "Iogurte", "Requeijão", "Ovos", "Salsicha"],
                "Frutas & Verduras 🍎": ["Banana", "Maçã", "Batata", "Cebola", "Alho", "Tomate", "Alface", "Limão", "Cenoura"],
                "Açougue 🥩": ["Carne Moída", "Bife", "Frango", "Linguiça", "Bacon", "Calabresa", "Costelinha"]
            }
        
        # Estado dos itens selecionados
        if 'selecionados' not in st.session_state:
            st.session_state.selecionados = []

    def adicionar_item(self, categoria, nome):
        if nome and nome not in st.session_state.categorias[categoria]:
            st.session_state.categorias[categoria].append(nome)
            st.rerun()

    def remover_item(self, categoria, nome):
        st.session_state.categorias[categoria].remove(nome)
        st.rerun()

    def gerar_whatsapp(self, lista_final):
        # Ordenação Alfabética
        lista_final.sort()
        data = datetime.now().strftime("%d/%m/%Y")
        msg = f"*🛒 Minha Lista de Compras - {data}*\n\n"
        for item in lista_final:
            msg += f"✅ {item}\n"
        return f"https://wa.me/?text={urllib.parse.quote(msg)}"

# --- Interface Estilizada ---
st.set_page_config(page_title="Super Lista Pro", page_icon="📝", layout="wide")

app = ListaComprasPro()

st.title("📝 Lista de Compras Categorizada")
st.info("Baseada no seu modelo de PDF. Marque o que precisa comprar.")

# Sidebar para adicionar novos itens
with st.sidebar:
    st.header("⚙️ Gerenciar Itens")
    cat_escolhida = st.selectbox("Escolha a Categoria:", list(st.session_state.categorias.keys()))
    novo_nome = st.text_input("Nome do Produto:")
    if st.button("➕ Adicionar à Lista"):
        app.adicionar_item(cat_escolhida, novo_nome)

# Exibição das Categorias em Colunas (Layout igual ao PDF)
col1, col2 = st.columns(2)
itens_marcados = []

categorias_lista = list(st.session_state.categorias.items())
metade = len(categorias_lista) // 2

# Coluna 1
with col1:
    for cat, produtos in categorias_lista[:metade]:
        st.subheader(cat)
        for p in produtos:
            c1, c2 = st.columns([4, 1])
            if c1.checkbox(p, key=f"check_{p}"):
                itens_marcados.append(p)
            if c2.button("🗑️", key=f"del_{p}"):
                app.remover_item(cat, p)

# Coluna 2
with col2:
    for cat, produtos in categorias_lista[metade:]:
        st.subheader(cat)
        for p in produtos:
            c1, c2 = st.columns([4, 1])
            if c1.checkbox(p, key=f"check_{p}"):
                itens_marcados.append(p)
            if c2.button("🗑️", key=f"del_{p}"):
                app.remover_item(cat, p)

st.divider()

# Botão de Envio Flutuante/Destaque
if st.button("🟢 ENVIAR LISTA PARA WHATSAPP", use_container_width=True):
    if itens_marcados:
        link = app.gerar_whatsapp(itens_marcados)
        st.markdown(f"""
            <a href="{link}" target="_blank">
                <button style="background-color: #25D366; color: white; border: none; padding: 20px; border-radius: 10px; width: 100%; font-weight: bold; font-size: 20px; cursor: pointer;">
                    CONFIRMAR E ABRIR WHATSAPP 📱
                </button>
            </a>
        """, unsafe_allow_html=True)
    else:
        st.warning("Selecione pelo menos um item para enviar.")
