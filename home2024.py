
import streamlit as st

#from deta import Deta
from PIL import Image
import time

st.set_page_config(
    page_title="Minec Reg App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

st.image(imagen1)
st.image(imagen2)

st.header('Bienvenido a MINEC')
st.subheader('Ministerio de Educación Cristiana de las Asambleas de Dios Venezuela')
ingresou = st.popover(' $$ \large 👉PRONDAMIN 2024👈 \\newline Ingresar $$')

uministro = ingresou.toggle(' $$ \Large Ministro \small \\newline Ministro \,acreditado \,que \,desee \\newline actualizar \,su \,data \,y/o \,\, inscribirse \\newline en \,curso \,PRONDAMIN $$')
uminec = ingresou.toggle(' $$ \large Usuario \,MINEC $$')


if uminec:
    st.switch_page('pages/logmi.py')
if uministro:
    st.toast('Aviso: el proceso de matriculación de Prondamin2024 ha finalizado')
    #with st.spinner('Matriculación Prondamin2024 cerrada):
    #    time.sleep(5)
    st.switch_page('pages/logministro.py')
