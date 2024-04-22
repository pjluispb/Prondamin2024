import streamlit as st
import pandas as pd
from deta import Deta
from PIL import Image

st.set_page_config(
    page_title="Minec Reg App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

deta = Deta(st.secrets["deta_key"])

def update_condicion(row):
    #dfcedpay['condicion']='Bloqueo - 01' if dfcedpay['paycon']=='SI' else '-'
    condicion = 'Bloqueo en marca 01' if row['paycon'] in ['SI', 'SI++'] else '-'
    return condicion

        
@st.cache_data
def load_data02():
    Pronda24 = deta.Base('Prondamin2024C')
    res = Pronda24.fetch(limit=500)
    all_items = res.items
    while res.last:
        res = Pronda24.fetch(last=res.last)
        all_items += res.items
    dfall_items = pd.DataFrame(all_items)
    return dfall_items
    

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

#try:
#    logina = st.session_state['logina']
#except:
    # switch_page('reiniciar03')
#    st.switch_page('home2024.py') 

#logina = st.session_state['logina']
#logina
st.image(imagen1)
st.image(imagen2)

logina = {'user':'Jota', 'rol':'Admin'}

st.subheader('Hola ****' + logina['user'] + '****')
#st.write('Datos del registro de ministros del distrito: ****' + logina['Distrito'] + '****')

# Carga Pronda
Pronda = load_data02()

# Carga Marks
bdmarks = deta.Base('marks24B')
marcas = bdmarks.fetch(limit=5000)
marcas_items = marcas.items
dfmarcas = pd.DataFrame(marcas_items)

'Pronda = ', Pronda
'marks = ', dfmarcas 
if 'corte-1' in marks.columns:
    'corte-1 existe en marks'
else:
    genm = st.button('Genera Marca 1')
    if genm:
        dfcedpay = Pronda[['key','paycon']]
        dfcedpay['corte-1'] = 'Corte01 : '+dfcedpay['paycon']+' --> 22/4:4am'
        dfcedpay['condicion'] = dfcedpay.apply(update_condicion, axis=1)               # Actualiza el campo condicion en el dataframe
        'dfcedpay = ', dfcedpay
        #  Graba dfcedpay{key,paycon,corte-1,condicion}
        #---------------------------------------------------------------------------
        # para grabar en la bd en grupos de 20 registros a la vez
        num_registros_por_lista = 20
        # Crea una columna que represente el número de lista para cada registro
        dfcedpay['lista'] = dfcedpay.index // num_registros_por_lista
        # Divide el DataFrame en grupos basados en la columna 'lista'
        grupos = dfcedpay.groupby('lista')                                          # Ahora puedes acceder a cada grupo individualmente
        contador = 1
        for nombre_lista, grupo in grupos:
            st.write('Lista ', nombre_lista)
            grupo
            reggrupo = grupo.to_dict('records')
            #reggrupo
            try:
                bdmarks.put_many(reggrupo)
            except:
                'error grabando grupo',contador
            contador+=1
            #if contador>12: break
        #--------------------------------------------------------------------------
    
    st.write('---')

    
    
    
