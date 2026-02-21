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

def remover_acentos(texto):
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
                "AÇOUGUE": ["ALCATRA", "ASINHA", "BACON", "BIFE", "CALABRESA", "CARNE MOÍDA", "COSTELÃO", "COSTELINHA", "COXINHA", "CUPIM", "FÍGADO", "FILÉ", "FILÉ DE PEITO", "FRALDINHA", "FRANGO", "LÍNGUA", "LINGUIÇA", "LOMBO", "MÚSCULO", "PICANHA"],
                "TEMPEROS": ["AÇÚCAR MASCAVO", "ALHO EM PÓ", "CEBOLA EM PÓ", "ORÉGANO", "PÁPRICA DEFUMADA", "PÁPRICA PICANTE", "PIMENTA DO REINO"],
                "BEBIDAS": ["ÁGUA MINERAL", "CERVEJA", "ENERGÉTICO", "REFRIGERANTE", "SUCO", "VINHO"],
                "OUTROS": []
            }
            st.session_state.categorias = {k: sorted(v, key=remover_acentos) for k, v in raw_data.items()}
        
        if 'reset_trigger' not in st.session_state:
            st.session_state.reset_trigger = 0

    def adicionar_item(self, nome):
        nome_upper = str(nome).upper()
        if nome_upper and nome_upper not in st.session_state.categorias["OUTROS"]:
            st.session_state.categorias["OUTROS"].append(nome_upper)
            st.session_state.categorias["OUTROS"].sort(key=remover_acentos)
            st.rerun()

    def limpar_tudo(self):
        for chave in list(st.session_state.keys()):
            if chave.startswith("check_"):
                st.session_state[chave] = False
        st.session_state.reset_trigger += 1
        st.rerun()

    def gerar_imagem(self, itens, motivo):
        largura = 550
        espaco_item = 45
        # Altura dinâmica baseada na existência ou não do motivo
        base_altura = 220 if motivo else 150
        altura_total = base_altura + (len(itens) * espaco_item) + 100
        
        img = Image.new('RGB', (largura, altura_total), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        try:
            font_titulo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
            font_motivo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
            font_texto = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except:
            font_titulo = font_motivo = font_texto = ImageFont.load_default()

        fuso_br = pytz.timezone('America/Sao_Paulo')
        data_br = datetime.now(fuso_br).strftime("%d/%m/%Y")
        
        # Cabeçalho
        draw.text((30, 30), "LISTA DE COMPRAS", fill=(0, 0, 0), font=font_titulo)
        draw.text((30, 65), f"DATA: {data_br}", fill=(100, 100, 100), font=font_texto)
        
        y_linha = 110
        if motivo:
            motivo_limpo = f"MOTIVO: {motivo.upper()}"
            draw.text((30, 100), motivo_limpo, fill=(0, 50, 150), font=font_motivo)
            y_linha = 150
        
        draw.line((30, y_linha, 520, y_linha), fill=(0, 0, 0), width=3)
        
        y = y_linha + 30
        for item in itens:
            draw.text((40, y), f"[X] {item}", fill=(0, 0, 0), font=font_texto)
            y += espaco_item
            
        draw.text((30, y + 30), "by ®rvrs", fill=(150, 150, 150), font=font_texto)
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    def gerar_whatsapp_texto(self, lista_final, motivo):
        lista_final.sort(key=remover_acentos)
        fuso_br = pytz.timezone('America/Sao_Paulo')
        data_br = datetime.now(fuso_br).strftime("%d/%m/%Y")
        cabecalho = f"*--- LISTA DE COMPRAS ({data_br}) ---*\n"
        if motivo:
            cabecalho += f"\n*MOTIVO:* {motivo.upper()}\n"
        corpo = "\n" + "\n".join([f"[X] {item}" for item in lista_final])
        assinatura = "\n\nby ®rvrs"
        return f"https://wa.me/?text={urllib.parse.quote(cabecalho + corpo + assinatura)}"

# --- Layout Mobile ---
st.set_page_config(page_title="Lista rvrs", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main-title { font-family: 'Arial Black', sans-serif; text-align: center; border-bottom: 3px solid #000; padding: 10px; font-size: 24px; }
    .stMarkdown h3 { background-color: #000; color: #fff !important; padding: 10px; text-align: center; font-size: 14px !important; border-radius: 8px; margin-top: 20px; }
    .stCheckbox { padding: 12px 0; border-bottom: 1px solid #f9f9f9; }
    div.stButton > button { height: 3.5em; font-weight: bold; border-radius: 12px; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

app = ListaComprasPro()
st.markdown('<h1 class="main-title">Lista de Compras</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 CONFIGURAÇÃO")
    motivo_compra = st.text_input("📍 Motivo / Local:", placeholder="Ex: Festa na Fazenda", key=f"motivo_ti_{st.session_state.reset_trigger}")
    
    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        app.limpar_tudo()
    
    st.divider()
    with st.form("add_item_form", clear_on_submit=True):
        novo = st.text_input("➕ Novo Item:")
        if st.form_submit_button("ADICIONAR À LISTA", use_container_width=True):
            app.adicionar_item(novo)
    
    st.divider()
    selecionados = [k.split("_")[1] for k, v in st.session_state.items() if k.startswith("check_") and v]

    if selecionados:
        url_wa = app.gerar_whatsapp_texto(selecionados, motivo_compra)
        st.markdown(f'<a href="{url_wa}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white;padding:20px;border-radius:15px;text-align:center;font-weight:bold;margin-bottom:15px;font-size:18px;box-shadow: 0 4px 6px rgba(0,0,0,0.1);">📲 ENVIAR WHATSAPP</div></a>', unsafe_allow_html=True)
        
        img_bytes = app.gerar_imagem(sorted(selecionados, key=remover_acentos), motivo_compra)
        st.download_button(label="🖼️ BAIXAR IMAGEM DA LISTA", data=img_bytes, file_name=f"lista_{motivo_compra or 'compras'}.png", mime="image/png", use_container_width=True)

# Exibição da Lista
col1, col2, col3 = st.columns(3)
todas_cats = list(st.session_state.categorias.items())
for i, (cat, produtos) in enumerate(todas_cats):
    target_col = [col1, col2, col3][i % 3]
    with target_col:
        st.subheader(cat)
        for p in produtos:
            st.checkbox(p, key=f"check_{p}_{cat}")

st.markdown("<br><hr><p style='text-align:center; color:grey;'>2026 | Desenvolvido por ®rvrs</p>", unsafe_allow_html=True)
