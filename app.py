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
            # Lista exata extraída do seu arquivo PDF
            st.session_state.categorias = {
                "MERCEARIA": [
                    "AÇÚCAR", "AMENDOIM", "ARROZ", "AZEITE", "AZEITONA", "BISCOITOS", "BOLACHAS", "CAFÉ", 
                    "CALDO GALINHA", "CHÁ", "COCO RALADO", "CREME DE LEITE", "ERVILHA", "EXTRATO TOMATE", 
                    "FARINHA DE TRIGO", "FARINHA MANDIOCA", "FARINHA ROSCA", "FARINHA TEMPERADA", "FEIJÃO", 
                    "FERMENTO", "FILTRO CAFÉ", "FÓSFORO", "FUBÁ", "GELATINA", "KETCHUP", "LASANHA", "LEITE", 
                    "LEITE CONDENSADO", "LEITE DE COCO", "LENTILHA", "MACARRÃO", "MAIONESE", "MAISENA", 
                    "MASSA PIZZA", "MILHO VERDE", "MISTURA P/ BOLO", "MOLHO INGLÊS", "MOLHO TOMATE", 
                    "MOSTARDA", "ÓLEO", "OVOS", "PALMITO", "PÓ ROYAL", "TAPIOCA", "TEMPERO", "TODDY"
                ],
                "LIMPEZA": [
                    "DETERGENTE", "ÁGUA SANITÁRIA", "ÁLCOOL", "LISOFORME", "AMACIANTE", "SABÃO EM PÓ", 
                    "SABÃO BARRA", "SACO DE LIXO", "DESINFETANTE", "VEJA", "BICARBONATO", "PEDRA SANITÁRIA", 
                    "RODO", "VASSOURA", "LUSTRA MÓVEIS", "BOMBRIL", "BUCHA COZINHA", "PEROBA", "PASTA PINHO", 
                    "CÊRA", "BUCHA BANHO", "LÂMPADA", "PAPEL ALUMÍNIO", "VELA"
                ],
                "HIGIENE": [
                    "ACETONA", "ALGODÃO", "FIO DENTAL", "GUARDANAPO", "PAPEL HIGIÊNICO", "CONDICIONADOR", 
                    "PASTA DE DENTE", "DESODORANTE", "ESCOVA DE DENTE", "PRESTO-BARBA", "SHAMPOO", 
                    "SABONETE LÍQUIDO", "SABONETE"
                ],
                "FRIOS": [
                    "CHEDDAR", "MANTEIGA", "MARGARINA", "MORTADELA", "MUSSARELA", "NUGGETS", 
                    "PASTEL (MASSA)", "PRESUNTO", "QUEIJO MINAS", "QUEIJO RALADO", "REQUEIJÃO", 
                    "RICOTA", "SALSICHA", "YOGURTE"
                ],
                "AÇOUGUE": [
                    "BACON", "BIFE (BOI)", "CALABRESA", "CARNE MOÍDA", "COSTELINHA", "CUPIM", 
                    "FRANGO", "LINGUIÇA", "LOMBO", "PEIXE"
                ],
                "TEMPEROS": [
                    "ALHO E SAL", "CALDO DE CARNE", "CANELA", "FUMAÇA", "PÁPRICA", "AÇÚCAR MASCAVO ", 
                    "CRAVO", "LOURO", "NOZ-MOSCADA", "ORÉGANO", "CEBOLA EM PÓ", "ALHO EM PÓ", "PIMENTA DO REINO"
                ],
                "BEBIDAS": [
                    "ÁGUA MINERAL", "CERVEJA", "REFRIGERANTE", "SUCO", "VINHO"
                ],
                "HORTIFRUTI": [
                    "ALFACE", "ALHO", "BANANA", "BATATA", "CEBOLA", "CENOURA", "LARANJA", 
                    "LIMÃO", "MAÇÃ", "MAMÃO", "OVOS", "TOMATE"
                ],
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

# --- Interface Estilizada ---
st.set_page_config(page_title="Lista de Compras", layout="wide")

st.markdown("""
    <style>
    .main-title {
        font-family: 'Arial Black', sans-serif;
        color: #000;
        text-align: center;
        border-bottom: 3px solid #000;
        padding-bottom: 5px;
        text-transform: uppercase;
        font-size: 32px;
    }
    .stMarkdown h3 {
        background-color: #000;
        color: #fff !important;
        padding: 4px 12px;
        font-size: 16px !important;
        text-transform: uppercase;
        margin-top: 15px !important;
    }
    .stCheckbox { margin-bottom: -12px; }
    </style>
    """, unsafe_allow_html=True)

app = ListaComprasPro()

st.markdown('<h1 class="main-title">Lista de Compras</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.header("CONTROLE")
    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        app.limpar_selecoes()
    st.divider()
    st.subheader("➕ NOVO ITEM")
    novo_nome = st.text_input("Item:")
    if st.button("ADICIONAR", use_container_width=True):
        app.adicionar_item(novo_nome)
    st.divider()
    
    selecionados = []
    for k, v in st.session_state.items():
        if k.startswith("check_") and v:
            partes = k.split("_")
            if len(partes) >= 2:
                selecionados.append(partes[1])

    if selecionados:
        link = app.gerar_whatsapp(selecionados)
        st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white;padding:15px;border-radius:8px;text-align:center;font-weight:bold;">ENVIAR PARA WHATSAPP</div></a>', unsafe_allow_html=True)

# --- Layout de Colunas ---
col1, col2, col3 = st.columns(3)
todas_cats = list(st.session_state.categorias.items())

for i, (cat, produtos) in enumerate(todas_cats):
    if i % 3 == 0: target_col = col1
    elif i % 3 == 1: target_col = col2
    else: target_col = col3
    
    with target_col:
        st.subheader(cat)
        for p in produtos:
            st.checkbox(p, key=f"check_{p}_{cat}")

# --- Rodapé ---
st.write("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align:center; color:grey;'>2026 Lista de Compras | Desenvolvido por ®rvrs</p>", unsafe_allow_html=True)
