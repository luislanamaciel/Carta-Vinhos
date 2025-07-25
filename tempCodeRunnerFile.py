import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
from pyzbar import pyzbar
import cv2

# -----------------------------
# Leitura da base de dados
@st.cache_data
def carregar_dados():
    return pd.read_excel("CVV.xlsx")

df = carregar_dados()

st.title("Carta de Vinhos Virtual")

# -----------------------------
# Sessão inicial
if "codigo" not in st.session_state:
    st.session_state.codigo = ""
if "foco" not in st.session_state:
    st.session_state.foco = False

# -----------------------------
# Leitura por câmera
class LeitorCodigo(VideoProcessorBase):
    def recv(self, frame):
        imagem = frame.to_ndarray(format="bgr24")
        codigos = pyzbar.decode(imagem)
        for codigo in codigos:
            dados = codigo.data.decode("utf-8")
            st.session_state.codigo = dados
            st.session_state.foco = True
        return av.VideoFrame.from_ndarray(imagem, format="bgr24")

# Ativa câmera
st.subheader("Ou use a câmera para ler o código de barras")
webrtc_streamer(key="leitor", video_processor_factory=LeitorCodigo)

# -----------------------------
# Campo de entrada
st.subheader("Digite ou leia o código de barras")
codigo = st.text_input("Código do vinho:", key="codigo")

# Botão de limpar
def limpar_codigo():
    st.session_state.codigo = ""
    st.session_state.foco = True

st.button("Limpar", on_click=limpar_codigo)

# Aplica foco via JavaScript
if st.session_state.get("foco", False):
    components.html("""
        <script>
        const input = window.parent.document.querySelector('input[type="text"]');
        if (input) {
            input.focus();
        }
        </script>
    """, height=0)
    st.session_state.foco = False

# -----------------------------
# Exibição do vinho
if codigo:
    vinho = df[df['Código de Barras'].astype(str) == str(codigo)]
    if not vinho.empty:
        vinho = vinho.iloc[0]
        nome = vinho.get('Nome', 'Nome não disponível')
        tipo = vinho.get('Tipo', 'Não informado')
        uva = vinho.get('Uva', 'Não informado')
        origem = vinho.get('Origem', 'Não informado')
        safra = vinho.get('Safra', 'Não informado')
        harmonizacao = vinho.get('Harmonização', '')
        link_imagem = vinho.get('Link da Imagem', '')

        col1, col2 = st.columns([1, 2])
        with col1:
            if pd.notna(link_imagem) and str(link_imagem).startswith("http"):
                st.image(link_imagem, width=320, caption=".")

        with col2:
            st.markdown(f"""
                <div style='
                    border: 1px solid #ccc;
                    border-radius: 15px;
                    padding: 20px;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                    background-color: #fdfdfd;
                '>
                    <h3 style='color: #800000;'>{nome}</h3>
                    <p><strong>Tipo:</strong> {tipo}</p>
                    <p><strong>Origem:</strong> {origem}</p>
                    <p><strong>Uva:</strong> {uva}</p>
                    <p><strong>Safra:</strong> {safra}</p>
                    <p><strong>Harmonização:</strong> {harmonizacao}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Vinho não encontrado.")