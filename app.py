# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime
import urllib.parse
import unicodedata
import io
from PIL import Image, ImageDraw, ImageFont

try:
    import pytz
except ImportError:
    pass

# Função para evitar erros de acentuação na imagem (AÃ‡ÃšCAR -> ACUCAR)
def limpar_texto_img(texto):
    if not texto: return ""
    return ''.join(c for c in unicodedata.normalize('NFD', str(texto))
                  if unicodedata.category(c) != 'Mn').upper()

def remover_acentos_ordem(texto):
    if not texto: return ""
    return ''.join(c for c in unicodedata.normalize('NFD', str(texto))
                  if unicodedata.category(c) != 'Mn')

class ListaComprasPro:
    def __init__(self):
        if 'categorias' not in st.session_state:
            raw_data = {
                "MERCEARIA": ["AÇÚCAR", "AMENDOIM", "ARROZ", "AZEITE", "AZEITONA", "BATATA FRITA", "BISCOITOS", "BOLACHAS", "CAFÉ", "CALDO GALINHA", "CHÁ", "COCO RALADO", "CREME DE LEITE", "ERVILHA", "ESSÊNCIA", "EXTRATO TOMATE", "FARINHA DE MILHO", "FARINHA DE TRIGO", "FARINHA MANDIOCA", "FARINHA ROSCA", "FARINHA TEMPERADA", "FEIJÃO", "FERMENTO", "FILTRO CAFÉ", "FLOCÃO DE MILHO", "FÓSFORO", "FUBÁ", "GELATINA", "KETCHUP", "LASANHA", "LEITE", "LEITE CONDENSADO", "LEITE DE COCO", "LENTILHA", "MACARRÃO", "MAIONESE", "MAISENA", "MASSA PIZZA", "MILHO VERDE", "MISTURA P/ BOLO", "MOLHO INGLÊS", "MOLHO TOMATE", "MOSTARDA", "ÓLEO", "OVOS", "PALMITO", "PÓ ROYAL", "TAPIOCA", "TEMPERO", "TODDY"],
                "LIMPEZA": ["ÁGUA SANITÁRIA", "ÁLCOOL", "AMACIANTE", "BICARBONATO", "BOMBRIL", "BUCHA BANHO", "BUCHA COZINHA", "CÊRA", "DESINFETANTE", "DETERGENTE", "LÂMPADA", "LISOFORME", "LUSTRA MÓVEIS", "PAPEL ALUMÍNIO", "PASTA PINHO", "PEDRA SANITÁRIA", "PEROBA", "RODO", "SABÃO BARRA", "SABÃO EM PÓ", "SACO DE LIXO", "VASSOURA", "VEJA", "VELA"],
                "HIGIENE": ["ACETONA", "ALGODÃO", "CONDICIONADOR", "DESODORANTE", "ESCOVA DE DENTE", "FIO DENTAL", "GUARDANAPO", "PAPEL HIGIÊNICO", "PASTA DE DENTE", "PRESTO-BARBA", "SABONETE", "SABONETE LÍQUIDO", "SHAMPOO"],
                "FRIOS": ["CHEDDAR", "EMPANADO", "GORGONZOLA", "HAMBURGUER", "IOGURTE", "MANTEIGA", "MARGARINA", "MORTADELA", "MUSSARELA", "PASTEL (MASSA)", "PRESUNTO", "QUEIJO", "REQUEIJÃO", "SALSICHA"],
                "FRUTAS / VERDURAS": ["ABÓBORA", "ALFACE", "ALHO", "BANANA", "BATATA", "BETERRABA", "CEBOLA", "CENOURA", "CHUCHU", "LARANJA", "LIMÃO", "MAÇÃ", "MAMÃO", "MELANCIA", "MELÃO", "PÊRA", "TOMATE"],
                "AÇOUGUE": ["ALCATRA", "ASINHA", "BACON", "BIFE", "CALABRESA", "CARNE MOÍDA", "COSTELÃO", "COSTELINHA", "COXINHA", "CUPIM", "FÍGADO", "FILÉ", "FILÉ DE PEITO", "FRALDINHA", "FRANGO", "LINGUA", "LINGUIÇA", "LOMBO", "MÚSCULO", "PICANHA"],
                "TEMPEROS": ["AÇÚCAR MASCAVO", "ALHO EM PÓ", "CEBOLA EM PÓ", "OREGANO", "PÁPRICA DEFUMADA", "PÁPRICA PICANTE", "PIMENTA DO REINO"],
                "BEBIDAS": ["ÁGUA MINERAL", "CERVEJA", "ENERGÉTICO", "REFRIGERANTE", "SUCO", "VINHO"],
                "OUTROS": []
            }
            st.session_state.categorias = {k: sorted(v, key=remover_acentos_ordem) for k, v in raw_data.items()}
        
        if 'reset_count' not in st.session_state:
            st.session_state.reset_count = 0

    def limpar_tudo(self):
        for chave in list(st.session_state.keys()):
            if chave.startswith("check_"):
                st.session_state[chave] = False
        st.session_state.reset_count += 1
        st.rerun()

    def gerar_imagem(self, itens, motivo_val):
        largura = 500
        # O pulo do gato: calculamos onde os itens começam
        y_cabecalho_fim = 120 if motivo_val else 85
        altura_total = y_cabecalho_fim + (len(itens) * 32) + 60
        
        img = Image.new('RGB', (largura, altura_total), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        fuso_br = pytz.timezone('America/Sao_Paulo')
        data_br = datetime.now(fuso_br).strftime("%d/%m/%Y")
        
        # Desenho do Cabeçalho
        draw.text((20, 20), "LISTA DE COMPRAS", fill=(0, 0, 0))
        draw.text((20, 45), f"DATA: {data_br}", fill=(100, 100, 100))
        
        if motivo_val:
            txt_motivo = f"MOTIVO: {limpar_texto_img(motivo_val)}"
            draw.text((20, 75), txt_motivo, fill=(0, 51, 153))
        
        # Linha divisória dinâmica
        draw.line((20, y_cabecalho_fim - 5, 480, y_cabecalho_fim - 5), fill=(0, 0, 0), width=2)
        
        # Desenho dos Itens
        y = y_cabecalho_fim + 15
        for item in itens:
            draw.text((40, y), f"[X] {limpar_texto_img(item)}", fill=(0, 0, 0))
            y += 32
            
        draw.text((20, y + 10), "BY RVRS", fill=(180, 180, 180))
        
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()

# --- Interface ---
st.set_page_config(page_title="Lista rvrs", layout="wide", initial_sidebar_state="collapsed")
app = ListaComprasPro()

st.markdown("<h2 style='text-align:center;'>LISTA DE COMPRAS</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ MENU")
    # Captura o motivo
    motivo_input = st.text_input("📍 Motivo / Local:", placeholder="Ex: Mercado Central", key=f"mot_v_{st.session_state.reset_count}")
    
    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        app.limpar_tudo()
    
    st.divider()
    with st.form("add_item", clear_on_submit=True):
        novo = st.text_input("➕ Novo Item:")
        if st.form_submit_button("ADICIONAR"):
            if novo:
                st.session_state.categorias["OUTROS"].append(novo.upper())
                st.session_state.categorias["OUTROS"].sort(key=remover_acentos_ordem)
                st.rerun()
    
    st.divider()
    selecionados = [k.split("_")[1] for k, v in st.session_state.items() if k.startswith("check_") and v]

    if selecionados:
        # Texto WhatsApp
        fuso_br = pytz.timezone('America/Sao_Paulo')
        data_br = datetime.now(fuso_br).strftime("%d/%m/%Y")
        msg = f"*--- LISTA DE COMPRAS ({data_br}) ---*\n"
        if motivo_input: msg += f"\n*MOTIVO:* {motivo_input.upper()}\n"
        msg += "\n" + "\n".join([f"[X] {i}" for i in sorted(selecionados, key=remover_acentos_ordem)]) + "\n\nby ®rvrs"
        url_wa = f"https://wa.me/?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'<a href="{url_wa}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-align:center;font-weight:bold;">📲 ENVIAR TEXTO</div></a>', unsafe_allow_html=True)
        
        # Imagem consertada
        img_data = app.gerar_imagem(sorted(selecionados, key=remover_acentos_ordem), motivo_input)
        st.download_button("🖼️ BAIXAR IMAGEM", data=img_data, file_name="lista.png", mime="image/png", use_container_width=True)

# Grid de Categorias
col1, col2, col3 = st.columns(3)
for i, (cat, produtos) in enumerate(st.session_state.categorias.items()):
    with [col1, col2, col3][i % 3]:
        st.subheader(cat)
        for p in produtos:
            st.checkbox(p, key=f"check_{p}_{cat}")

st.markdown("<br><hr><center>2026 | ®rvrs</center>", unsafe_allow_html=True)
