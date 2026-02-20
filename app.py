import streamlit as st
from datetime import datetime
import urllib.parse

class ListaCompras:
    """Classe que gerencia a lógica e os dados da lista de compras."""
    
    def __init__(self):
        # Inicializa a lista de produtos no estado da sessão se não existir
        if 'produtos' not in st.session_state:
            st.session_state.produtos = ["Arroz", "Feijão", "Sabão em pó", "Sabão em barra", "Desinfetante"]

    def adicionar_item(self, nome):
        """Adiciona um novo item à lista, evitando duplicados."""
        if nome and nome not in st.session_state.produtos:
            st.session_state.produtos.append(nome)
            return True
        return False

    def remover_item(self, nome):
        """Remove um item da lista e recarrega a interface."""
        if nome in st.session_state.produtos:
            st.session_state.produtos.remove(nome)
            st.rerun()

    def gerar_link_whatsapp(self, itens_selecionados):
        """Ordena os itens alfabeticamente e gera o link formatado."""
        if not itens_selecionados:
            return None
        
        # Ordenação Alfabética (conforme solicitado)
        itens_selecionados.sort()
        
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        mensagem = f"*Lista de Compras - {data_hoje}*\n\n"
        
        for item in itens_selecionados:
            mensagem += f"✅ {item}\n"
            
        # Codifica a mensagem para o formato de URL do WhatsApp
        texto_url = urllib.parse.quote(mensagem)
        return f"https://wa.me/?text={texto_url}"

# --- Instanciação e Interface ---

# Configuração da Página
st.set_page_config(page_title="Minha Lista POO", page_icon="🛒")

# Criação do objeto principal
minha_lista = ListaCompras()

st.title("🛒 Lista de Compras Inteligente")

# 1. Seção para adicionar itens
with st.expander("➕ Adicionar Novo Produto"):
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        novo = st.text_input("Nome do item:", key="input_item", placeholder="Ex: Macarrão")
    with col_btn:
        if st.button("Incluir"):
            if minha_lista.adicionar_item(novo):
                st.rerun()

st.write("---")

# 2. Seção de exibição e seleção
selecionados = []
st.subheader("Selecione o que precisa comprar:")

for item in st.session_state.produtos:
    col_check, col_del = st.columns([5, 1])
    
    with col_check:
        # Se marcado, o item entra na lista de 'selecionados'
        if st.checkbox(item, key=f"cb_{item}"):
            selecionados.append(item)
            
    with col_del:
        # Botão para excluir o item da base
        if st.button("🗑️", key=f"btn_{item}"):
            minha_lista.remover_item(item)

st.write("---")

# 3. Botão Final de Envio
if st.button("🚀 Enviar via WhatsApp (Ordem A-Z)"):
    link = minha_lista.gerar_link_whatsapp(selecionados)
    if link:
        # Estilização do botão de link para ficar verde como o WhatsApp
        st.markdown(f"""
            <a href="{link}" target="_blank">
                <button style="
                    background-color: #25D366;
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 10px;
                    width: 100%;
                    font-size: 18px;
                    font-weight: bold;
                    cursor: pointer;">
                    Confirmar Envio ✅
                </button>
            </a>
            """, unsafe_allow_html=True)
    else:
        st.warning("Por favor, marque pelo menos um item da lista.")