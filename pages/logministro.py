import streamlit as st

from deta import Deta
from PIL import Image

st.set_page_config(
    page_title="Minec Reg App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

deta = Deta(st.secrets["deta_key"])
encprof = deta.Base('Prondamin2024D')
photosys = deta.Drive(name='modphotos')

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

st.image(imagen1)
st.image(imagen2)

st.header('Bienvenido a MINEC')
st.subheader('Ministerio de Educación Cristiana de las Asambleas de Dios Venezuela')
'---'
#st.subheader('Bienvenido Ministro')
#cedulaministro = st.text_input('$$ \large Introduce \,tu \,número \,de \,cédula\,:\,\, $$')
encontrada = False
cedulaministro = st.text_input('$$ \large Introduce \,el \,número \,de \,tu \,cédula \,y/o \\newline documento \,de \,identidad $$ :id:',key='iced',placeholder='ingrese su ID')
try:
    first = encprof.get(cedulaministro)
except:
    st.write('Ingrese número de cédula')
    first=None
if first == None:
    st.write('Cedula No encontrada - intente de nuevo')
else:
    #colsa = st.columns(2)
    imagenCer = photosys.get('testigo2.png')
    content = imagenCer.read()
    
    st.image(content)
    st.subheader('Hola '+first['nombre']+'  '+first['apellido'])
    st.error('El proceso de matriculación de Prondamin2024 ha finalizado')
    vercertificados = st.toggle('Ver/Consultar Certificados')
    #actualizamin = st.toggle('Actualizar data y/o inscribir curso')
    st.session_state['cedulaministro'] = first['key']
    if vercertificados:
        st.switch_page('pages/certifi6.py')
    #if actualizamin:
    #    st.switch_page('pages/actualizar2024B.py')
    #    'voy a actualizar'
st.page_link("home2024.py", label="Inicio", icon="🏠")
