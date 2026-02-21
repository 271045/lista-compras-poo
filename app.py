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

# Função para garantir ordenação correta e evitar erros
def remover_acentos(texto):
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
            st.session_state.categorias = {k: sorted(v, key=remover_acentos) for k, v in raw_data.items()}
        
        if 'reset_trigger' not in st.session_state:
            st.session_state.reset_trigger = 0

    def limpar_tudo(self):
        for chave in list(st.session_state.keys()):
            if chave.startswith("check_"):
                st.session_state[chave] = False
        st.session_state.reset_trigger += 1
        st.rerun()

    def gerar_imagem(self, itens, motivo):
        largura = 550
        espaco_item = 35
        y_pos = 140 if motivo else 100
        altura_total = y_pos + (len(itens) * espaco_item) + 80
        img = Image.new('RGB', (largura, altura_total), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        try:
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            f_bold = ImageFont.truetype(font_path, 22)
            f_norm = ImageFont.truetype(font_path, 18)
        except:
            f_bold = f_norm = ImageFont.load_default()
        
        fuso_br = pytz.timezone('America/Sao_Paulo')
        data_br = datetime.now(fuso_br).strftime("%d/%m/%Y")
        d.text((30, 30), "LISTA DE COMPRAS", fill=(0, 0, 0), font=f_bold)
        d.text((30, 65), f"DATA: {data_br}", fill=(100, 100, 100), font=f_norm)
        
        y_linha = 100
        if motivo:
            d.text((30, 95), f"MOTIVO: {str(motivo).upper()}", fill=(0, 51, 153), font=f_bold)
            y_linha = 135
        d.line((30, y_linha, largura-30, y_linha), fill=(0, 0, 0), width=2)
        y = y_linha + 25
        for item in itens:
            d.text((40, y), f"[X] {item}", fill=(0, 0, 0), font=f_norm)
            y += espaco_item
        d.text((30, y + 20), "by ®rvrs", fill=(150, 150, 150), font=f_norm)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()

# --- Interface ---
st.set_page_config(page_title="Lista rvrs", layout="wide", initial_sidebar_state="collapsed")

app = ListaComprasPro()
st.markdown("<h1 style='text-align:center;'>Lista de Compras</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 OPÇÕES")
    
    # GARANTIA: O segredo é salvar o motivo no session_state imediatamente
    motivo_compra = st.text_input(
        "Motivo da Compra:", 
        placeholder="Ex: Mercado Central", 
        key=f"motivo_ti_{st.session_state.reset_trigger}"
    )

    st.divider()
    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        app.limpar_tudo()

    st.divider()
    with st.form("add_form", clear_on_submit=True):
        novo = st.text_input("➕ Novo Item:")
        if st.form_submit_button("ADICIONAR") and novo:
            app.adicionar_item(novo)

    st.divider()
    selecionados = [k.split("_")[1] for k, v in st.session_state.items() if k.startswith("check_") and v]

    if selecionados:
        # Gerar Texto WA com o motivo capturado
        fuso_br = pytz.timezone('America/Sao_Paulo')
        data_br = datetime.now(fuso_br).strftime("%d/%m/%Y")
        
        # Montagem manual do texto para garantir que o motivo_compra está aqui
        texto_wa = f"*--- LISTA DE COMPRAS ({data_br}) ---*\n"
        if motivo_compra:
            texto_wa += f"\n*MOTIVO:* {motivo_compra.upper()}\n"
        texto_wa += "\n" + "\n".join([f"[X] {i}" for i in sorted(selecionados, key=remover_acentos)])
        texto_wa += "\n\nby ®rvrs"
        
        url_wa = f"https://wa.me/?text={urllib.parse.quote(texto_wa)}"
        
        st.markdown(f'<a href="{url_wa}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-align:center;font-weight:bold;margin-bottom:10px;">📲 ENVIAR TEXTO</div></a>', unsafe_allow_html=True)
        
        img_data = app.gerar_imagem(sorted(selecionados, key=remover_acentos), motivo_compra)
        st.download_button("🖼️ BAIXAR IMAGEM", data=img_data, file_name="lista.png", mime="image/png", use_container_width=True)

# Grid principal
col1, col2, col3 = st.columns(3)
for i, (cat, itens) in enumerate(st.session_state.categorias.items()):
    with [col1, col2, col3][i % 3]:
        st.subheader(cat)
        for p in itens:
            st.checkbox(p, key=f"check_{p}_{cat}")
