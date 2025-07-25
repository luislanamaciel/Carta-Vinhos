import streamlit as st
import pandas as pd

# Carrega a base
df = pd.read_excel('CVV.xlsx')

st.title("Carta de Vinhos Virtual")

# Inicializa o estado da sessão para o código
if 'codigo' not in st.session_state:
    st.session_state.codigo = ''

def limpar_codigo():
    st.session_state.codigo = ''

# Campo de entrada do código de barras
codigo = st.text_input("Digite o código de barras do vinho:", value=st.session_state.codigo)

if codigo:
    vinho = df[df['Código de Barras'].astype(str) == str(codigo)]
    
    if not vinho.empty:
        vinho = vinho.iloc[0]

        nome = vinho.get('Nome', 'Nome não disponível')
        tipo = vinho.get('Tipo', 'Não informado')
        uva = vinho.get('Uva', 'Não informado')
        origem = vinho.get('Origem', 'Não informado')
        safra = vinho.get('Safra', 'Não informado')
        harmonização = vinho.get('Harmonização', '')
        link_imagem = vinho.get('Link da Imagem', '')

        # Layout horizontal: duas colunas
        col1, col2 = st.columns([1, 2])

        with col1:
            if pd.notna(link_imagem) and str(link_imagem).startswith("http"):
                st.image(link_imagem, width=320, caption=".")

        with col2:
            st.markdown(
                f"""
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
                    <p><strong>Harmonização:</strong> {harmonização}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

      #  st.button("Novo código", on_click=limpar_codigo)
    else:
        st.warning("Vinho não encontrado.")