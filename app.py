# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime
import urllib.parse
import unicodedata
import io
from PIL import Image, ImageDraw

try:
    import pytz
except ImportError:
    pass

# Função para garantir que o texto saia limpo na imagem (sem bugar acento)
def limpar_texto_imagem(texto):
    if not texto: return ""
    # Transforma AÇÚCAR em ACUCAR para a imagem não sair com erros
    return ''.join(c for c in unicodedata.normalize('NFD', str(texto))
                  if unicodedata.category(c) != 'Mn').upper()

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
            st.session_state.categorias = {k: sorted(v, key=limpar_texto_imagem) for k, v in raw_data.items()}
        
        if 'reset_trigger' not in st.session_state:
            st.session_state.reset_trigger = 0

    def adicionar_item(self, nome):
        nome_upper = str(nome).upper()
        if nome_upper and nome_upper not in st.session_state.categorias["OUTROS"]:
            st.session_state.categorias["OUTROS"].append(nome_upper)
            st.session_state.categorias["OUTROS"].sort(key=limpar_texto_imagem)
            st.rerun()

    def limpar_tudo(self):
        for chave in list(st.session_state.keys()):
            if chave.startswith("check_"):
                st.session_state[chave] = False
        st.session_state.reset_trigger += 1
        st.rerun()

    def gerar_imagem(self, itens, motivo):
        largura = 500
        # Aumentamos o cabeçalho para garantir que o motivo apareça
        y_linha_divisoria = 120 
        altura_total = y_linha_divisoria + (len(itens) * 30) + 80
        
        img = Image.new('RGB', (largura, altura_total), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        fuso_br = pytz.timezone('America/Sao_Paulo')
        data_br = datetime.now(fuso_br).strftime("%d/%m/%Y")
        
        # 1. Título
        draw.text((25, 20), "LISTA DE COMPRAS", fill=(0, 0, 0))
        # 2. Data
        draw.text((25, 45), f"DATA: {data_br}", fill=(100, 100, 100))
        
        # 3. MOTIVO (Posição fixa e cor azul para destacar)
        texto_motivo = f"MOTIVO: {limpar_texto_imagem(motivo)}" if motivo else "MOTIVO: NAO INFORMADO"
        draw.text((25, 75), texto_motivo, fill=(0, 51, 153))
        
        # 4. Linha divisória (abaixo do motivo)
        draw.line((25, 110, 475, 110), fill=(0, 0, 0), width=2)
        
        # 5. Itens
        y = 130
        for item in itens:
            item_limpo = limpar_texto_imagem(item)
            draw.text((40, y), f"[X] {item_limpo}", fill=(0, 0, 0))
            y += 30
            
        draw.text((25, y + 20), "BY RVRS", fill=(180, 180, 180))
        
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()

    def gerar_whatsapp_texto(self, lista_final, motivo):
        fuso_br = pytz.timezone('America/Sao_Paulo')
        data_br = datetime.now(fuso_br).strftime("%d/%m/%Y")
        cabecalho = f"*--- LISTA DE COMPRAS ({data_br}) ---*\n"
        if motivo:
            cabecalho += f"\n*MOTIVO:* {motivo.upper()}\n"
        corpo = "\n" + "\n".join([f"[X] {item}" for item in lista_final])
        assinatura = "\n\nby ®rvrs"
        return f"https://wa.me/?text={urllib.parse.quote(cabecalho + corpo + assinatura)}"

# --- Interface ---
st.set_page_config(page_title="Lista rvrs", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main-title { text-align: center; border-bottom: 3px solid #000; padding: 10px; font-size: 24px; font-weight: bold; }
    .stMarkdown h3 { background-color: #000 !important; color: #fff !important; padding: 8px; text-align: center; font-size: 14px !important; border-radius: 8px; margin-top: 15px; }
    div.stButton > button { font-weight: bold; border-radius: 10px; height: 3.5em; background-color: #f0f2f6; }
    .stCheckbox { padding: 5px 0; }
    </style>
    """, unsafe_allow_html=True)

app = ListaComprasPro()
st.markdown('<div class="main-title">LISTA DE COMPRAS</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ CONFIGURAÇÃO")
    # Campo do Motivo com chave de reset
    motivo_compra = st.text_input("📍 Motivo / Evento:", placeholder="Ex: Churrasco", key=f"motivo_input_{st.session_state.reset_trigger}")
    
    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        app.limpar_tudo()
    
    st.divider()
    with st.form("add_form", clear_on_submit=True):
        novo = st.text_input("➕ Novo Item:")
        if st.form_submit_button("ADICIONAR", use_container_width=True):
            if novo: app.adicionar_item(novo)
    
    st.divider()
    selecionados = [k.split("_")[1] for k, v in st.session_state.items() if k.startswith("check_") and v]

    if selecionados:
        url_wa = app.gerar_whatsapp_texto(selecionados, motivo_compra)
        st.markdown(f'<a href="{url_wa}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white;padding:18px;border-radius:12px;text-align:center;font-weight:bold;margin-bottom:12px;font-size:16px;">📲 WHATSAPP (TEXTO)</div></a>', unsafe_allow_html=True)
        
        img_bytes = app.gerar_imagem(selecionados, motivo_compra)
        st.download_button(label="🖼️ BAIXAR IMAGEM", data=img_bytes, file_name="lista.png", mime="image/png", use_container_width=True)

# Listagem
col1, col2, col3 = st.columns(3)
todas_cats = list(st.session_state.categorias.items())
for i, (cat, produtos) in enumerate(todas_cats):
    target_col = [col1, col2, col3][i % 3]
    with target_col:
        st.subheader(cat)
        for p in produtos:
            st.checkbox(p, key=f"check_{p}_{cat}")

st.markdown("<br><hr><p style='text-align:center; color:grey;'>2026 | Desenvolvido por ®rvrs</p>", unsafe_allow_html=True)
