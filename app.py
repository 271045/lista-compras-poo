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

# Função para garantir que os acentos não buguem na ordenação
def remover_acentos(texto):
    if not texto: return ""
    return ''.join(c for c in unicodedata.normalize('NFD', str(texto))
                  if unicodedata.category(c) != 'Mn')

# Função para limpar texto especificamente para a imagem (segurança extra)
def tratar_texto_imagem(texto):
    if not texto: return ""
    return str(texto).upper()

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
        espaco_item = 35
        y_pos_inicial = 140 if motivo else 100
        altura_total = y_pos_inicial + (len(itens) * espaco_item) + 80
        
        img = Image.new('RGB', (largura, altura_total), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        
        try:
            # Fonte padrão em servidores Linux/Streamlit
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            font_bold = ImageFont.truetype(font_path, 22)
            font_norm = ImageFont.truetype(font_path, 18)
        except:
            font_bold = font_norm = ImageFont.load_default()

        fuso_br = pytz.timezone('America/Sao_Paulo')
        data_br = datetime.now(fuso_br).strftime("%d/%m/%Y")
        
        d.text((30, 30), "LISTA DE COMPRAS", fill=(0, 0, 0), font=font_bold)
        d.text((30, 65), f"DATA: {data_br}", fill=(100, 100, 100), font=font_norm)
        
        y_linha = 100
        if motivo:
            motivo_txt = f"MOTIVO: {tratar_texto_imagem(motivo)}"
            d.text((30, 95), motivo_txt, fill=(0, 51, 153), font=font_bold)
            y_linha = 135
            
        d.line((30, y_linha, largura-30, y_linha), fill=(0, 0, 0), width=2)
        y = y_linha + 25
        for item in itens:
            d.text((40, y), f"[X] {item}", fill=(0, 0, 0), font=font_norm)
            y += espaco_item
            
        d.text((30, y + 20), "by ®rvrs", fill=(150, 150, 150), font=font_norm)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()

    def gerar_whatsapp_texto(self, lista_final, motivo):
        lista_final.sort(key=remover_acentos)
        fuso_br = pytz.timezone('America/Sao_Paulo')
        data_br = datetime.now(fuso_br).strftime("%d/%m/%Y")
        
        texto = f"*--- LISTA DE COMPRAS ({data_br}) ---*\n"
        if motivo:
            texto += f"\n*MOTIVO:* {motivo.upper()}\n"
        
        texto += "\n" + "\n".join([f"[X] {item}" for item in lista_final])
        texto += "\n\nby ®rvrs"
        
        return f"https://wa.me/?text={urllib.parse.quote(texto)}"

# --- Layout ---
st.set_page_config(page_title="Lista Pro rvrs", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main-title { font-family: 'Arial Black', sans-serif; text-align: center; border-bottom: 3px solid #000; padding: 10px; text-transform: uppercase; font-size: 28px; }
    .stMarkdown h3 { background-color: #000; color: #fff !important; padding: 8px; text-transform: uppercase; font-size: 15px !important; border-radius: 5px; }
    .stCheckbox { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

app = ListaComprasPro()
st.markdown('<h1 class="main-title">Lista de Compras</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 CONFIGURAÇÃO")
    
    # Captura o motivo
    motivo_compra = st.text_input(
        "Motivo da Compra:", 
        placeholder="Ex: Festa na Fazenda", 
        key=f"motivo_ti_{st.session_state.reset_trigger}"
    )
    
    st.divider()
    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        app.limpar_tudo()
    
    st.divider()
    with st.form("add_item_form", clear_on_submit=True):
        novo = st.text_input("➕ Adicionar Item:")
        if st.form_submit_button("ADICIONAR ITEM", use_container_width=True) and novo:
            app.adicionar_item(novo)
    
    st.divider()
    selecionados = [k.split("_")[1] for k, v in st.session_state.items() if k.startswith("check_") and v]

    if selecionados:
        # Botão WhatsApp (Texto)
        url_wa = app.gerar_whatsapp_texto(selecionados, motivo_compra)
        st.markdown(f'<a href="{url_wa}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white;padding:15px;border-radius:8px;text-align:center;font-weight:bold;margin-bottom:10px;">📲 ENVIAR TEXTO (WA)</div></a>', unsafe_allow_html=True)
        
        # Botão Baixar Imagem
        img_bytes = app.gerar_imagem(sorted(selecionados, key=remover_acentos), motivo_compra)
        st.download_button(label="🖼️ BAIXAR IMAGEM", data=img_bytes, file_name=f"lista_{remover_acentos(motivo_compra) or 'compras'}.png", mime="image/png", use_container_width=True)

# Grid de Categorias
col1, col2, col3 = st.columns(3)
cats = list(st.session_state.categorias.items())

for i, (cat, produtos) in enumerate(cats):
    with [col1, col2, col3][i % 3]:
        st.subheader(cat)
        for p in produtos:
            st.checkbox(p, key=f"check_{p}_{cat}")

st.markdown("<br><hr><p style='text-align:center; color:grey;'>2026 | Desenvolvido por ®rvrs</p>", unsafe_allow_html=True)
