import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from PIL import Image

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

deta = Deta(st.secrets["deta_key"])
accesos = deta.Base('minec-accesos')
res=accesos.fetch()
#res.items
logina = st.session_state['logina']
#logina

st.image(imagen1)
st.image(imagen2)
st.subheader('Bienvenid@ ' + logina['user'])
if logina['tipou']=='Registrador Financiero':
    acciones = ['procesar pagos', 'revisar pagos']
else:
    st.switch_page('home2024.py')    
st.subheader('Que deseas hacer?')
selector = st.radio('****Seleccionar Acción****', acciones, horizontal=True, label_visibility='collapsed', index=None)
#st.write(selector)
if selector=='procesar pagos':
    st.write('procesar pagos')
    st.switch_page('pages/procesapago.py')
if selector=='revisar pagos':
    st.write('procesar pagos')
    st.switch_page('pages/pagoverif.py')


st.page_link("home2024.py", label="Inicio", icon="🏠")

