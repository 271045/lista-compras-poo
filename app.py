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
            # Itens ajustados conforme o conteúdo do seu PDF
            st.session_state.categorias = {
                "MERCEARIA": ["AÇÚCAR", "ARROZ", "AZEITE", "AZEITONA", "BISCOITOS", "CAFÉ", "EXTRATO TOMATE", "FARINHA DE TRIGO", "FEIJÃO", "MACARRÃO", "MAIONESE", "MILHO VERDE", "MOLHO INGLÊS", "ÓLEO"],
                "LIMPEZA": ["ÁGUA SANITÁRIA", "ÁLCOOL", "AMACIANTE", "BOMBRIL", "DETERGENTE", "DESINFETANTE", "SABÃO EM PÓ", "SABÃO EM BARRA", "SACO DE LIXO", "VEJA"],
                "HIGIENE": ["ALGODÃO", "CONDICIONADOR", "DESODORANTE", "ESCOVA DE DENTE", "FIO DENTAL", "PAPEL HIGIÊNICO", "PASTA DE DENTE", "SABONETE", "SHAMPOO"],
                "FRIOS & LATICÍNIOS": ["CREME DE LEITE", "LEITE", "LEITE CONDENSADO", "MANTEIGA", "MUSSARELA", "OVOS", "PRESUNTO", "SALSICHA", "YOGURTE"],
                "FRUTAS & VERDURAS": ["ALHO", "BANANA", "BATATA", "CEBOLA", "CENOURA", "LARANJA", "LIMÃO", "MAÇÃ", "TOMATE"],
                "AÇOUGUE": ["BACON", "BIFE", "CALABRESA", "CARNE MOÍDA", "COSTELINHA", "FRANGO", "LINGUIÇA"],
                "OUTROS": []
            }

    def adicionar_item(self, nome):
        nome_upper = nome.upper()
        if nome_upper and nome_upper not in st.session_state.categorias["OUTROS"]:
            st.session_state.categorias["OUTROS"].append(nome_upper)
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

# --- Configurações de Design (Igual ao PDF) ---
st.set_page_config(page_title="Lista de Compras", layout="wide")

st.markdown("""
    <style>
    /* Estilo do Título igual ao cabeçalho do PDF */
    .main-title {
        font-family: 'Arial', sans-serif;
        color: #1a1a1a;
        text-align: center;
        border-bottom: 2px solid #000;
        padding-bottom: 10px;
        margin-bottom: 25px;
        text-transform: uppercase;
    }
    /* Estilo das Subcategorias */
    .stMarkdown h3 {
        background-color: #f0f2f6;
        padding: 5px 10px;
        border-left: 5px solid #333;
        font-size: 18px !important;
        margin-top: 20px !important;
    }
    /* Deixar os checkboxes mais limpos */
    .stCheckbox {
        padding: 2px 0px;
    }
    </style>
    """, unsafe_allow_html=True)

app = ListaComprasPro()

st.markdown('<h1 class="main-title">Lista de Compras</h1>', unsafe_allow_html=True)

# --- Barra Lateral ---
with st.sidebar:
    st.header("PAINEL DE CONTROLO")
    if st.button("🗑️ LIMPAR MARCAÇÕES", use_container_width=True):
        app.limpar_selecoes()
    
    st.divider()
    st.subheader("➕ NOVO ITEM")
    novo_nome = st.text_input("Nome do produto:")
    if st.button("ADICIONAR", use_container_width=True):
        app.adicionar_item(novo_nome)

    st.divider()
    selecionados = [k.replace("check_", "") for k, v in st.session_state.items() if k.startswith("check_") and v]

    if selecionados:
        link = app.gerar_whatsapp(selecionados)
        st.markdown(f"""
            <a href="{link}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 18px;">
                    ENVIAR PARA WHATSAPP
                </div>
            </a>
        """, unsafe_allow_html=True)
    else:
        st.info("Selecione os itens na lista.")

# --- Corpo da Lista (Colunas Iguais ao PDF) ---
col1, col2 = st.columns(2)
categorias_itens = list(st.session_state.categorias.items())
meio = (len(categorias_itens) + 1) // 2

for i, (cat, produtos) in enumerate(categorias_itens):
    target_col = col1 if i < meio else col2
    with target_col:
        st.subheader(cat)
        # Se for a categoria Outros e estiver vazia, mostra aviso discreto
        if cat == "OUTROS" and not produtos:
            st.caption("Use a lateral para adicionar itens extras.")
        
        # Organização dos itens
        for p in produtos:
            st.checkbox(p, key=f"check_{p}")

# --- Rodapé ---
st.write("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey; font-family: sans-serif;'>2026 Lista de Compras | Desenvolvido por ®rvrs</p>", unsafe_allow_html=True)
