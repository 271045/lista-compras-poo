import streamlit as st
from datetime import datetime
import urllib.parse

class ListaComprasPro:
    def __init__(self):
        # Dados baseados no seu PDF
        if 'categorias' not in st.session_state:
            st.session_state.categorias = {
                "Mercearia 🍞": ["Arroz", "Feijão", "Açúcar", "Café", "Macarrão", "Óleo", "Farinha de Trigo", "Milho Verde", "Extrato de Tomate", "Biscoitos", "Maionese", "Azeite"],
                "Limpeza 🧼": ["Sabão em Pó", "Sabão em Barra", "Desinfetante", "Água Sanitária", "Detergente", "Amaciante", "Álcool", "Saco de Lixo", "Bombril", "Veja", "Multiuso"],
                "Higiene 🪥": ["Pasta de Dente", "Sabonete", "Shampoo", "Condicionador", "Desodorante", "Papel Higiênico", "Fio Dental", "Algodão"],
                "Frios & Laticínios 🧀": ["Mussarela", "Presunto", "Leite", "Manteiga", "Iogurte", "Requeijão", "Ovos", "Salsicha"],
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
        # Ordenação Alfabética
        lista_final.sort()
        data = datetime.now().strftime("%d/%m/%Y")
        
        # Montando o texto com o Check que funciona em todos os sistemas
        corpo_lista = ""
        for item in lista_final:
            corpo_lista += f"✅ {item}\n"
            
        mensagem = f"*🛒 LISTA DE COMPRAS - {data}*\n\n{corpo_lista}"
        
        # O segredo está aqui: o quote do urllib garante que o emoji viaje bem na internet
        return f"https://wa.me/?text={urllib.parse.quote(mensagem)}"

# --- Interface ---
st.set_page_config(page_title="Super Lista Pro", page_icon="📝", layout="wide")
app = ListaComprasPro()

st.title("📝 Lista de Compras Categorizada")

with st.sidebar:
    st.header("⚙️ Opções")
    if st.button("🗑️ Limpar Marcações", use_container_width=True):
        app.limpar_selecoes()
    st.divider()
    st.subheader("➕ Adicionar Item")
    cat_escolhida = st.selectbox("Categoria:", list(st.session_state.categorias.keys()))
    novo_nome = st.text_input("Produto:")
    if st.button("Adicionar"):
        app.adicionar_item(cat_escolhida, novo_nome)

col1, col2 = st.columns(2)
itens_marcados = []
categorias_lista = list(st.session_state.categorias.items())
metade = len(categorias_lista) // 2

for i, (cat, produtos) in enumerate(categorias_lista):
    target_col = col1 if i < metade else col2
    with target_col:
        st.subheader(cat)
        for p in produtos:
            c_check, c_del = st.columns([4, 1])
            if c_check.checkbox(p, key=f"check_{p}"):
                itens_marcados.append(p)
            if c_del.button("❌", key=f"del_{p}"):
                app.remover_item(cat, p)

st.divider()

if st.button("🟢 ENVIAR PARA WHATSAPP", use_container_width=True):
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
        st.warning("Selecione os itens antes de enviar.")
