import pandas as pd
import streamlit as st
from deta import Deta
from PIL import Image

imagen1 = Image.open('minecLogo.jpeg')
imagen2 = Image.open('minecLogoTitle.jpeg')

deta = Deta(st.secrets["deta_key"])


def row_style(row):
    if row['paycon'] == 'SI++':
        return pd.Series('background-color: #7986cb; color:#000000', row.index)
    elif row['paycon'] == 'PENDIENTE X DIFERENCIA':
        return pd.Series('background-color: #ff5079; color:#000000', row.index)
    elif row['paycon'] == 'SI':
        return pd.Series('background-color: #8ede99; color:#000000', row.index)
    elif row['paycon'] == 'PENDIENTE':
        return pd.Series('background-color: #fdd834; color:#000000', row.index)
    elif row['paycon'] == 'En Revisión':
        return pd.Series('background-color: #d8bfd8; color:#000000', row.index)
    else:
        return pd.Series('', row.index)

def highlight_cells(val):
    return 'background-color: yellow' if val == val else ''
    
# Carga la bd de accesos
accesos = deta.Base('minec-accesos')
res=accesos.fetch()
# try:
#     logina = st.session_state['logina']
# except:
#     st.switch_page('home2024.py')

# Carga el Pronda
Prondamin24 = deta.Base('Prondamin2024C')
Pronda24 = Prondamin24.fetch(limit=5000)
dfPronda24 = pd.DataFrame(Pronda24.items)
# dfPronda24

# Carga el DBanVerif2024 ...Datos Bancarios ya procesados
DBanV24 = deta.Base('DBanVerif2024')
DBanV24f = DBanV24.fetch().items
dfDBanV24 = pd.DataFrame(DBanV24f)

st.image(imagen1)
st.image(imagen2)

#df = dfPronda24.dropna(subset=['close'])
#df
df = dfPronda24
df_ordenado = df.sort_values(by='paycon', ascending=False)
df_ordenado = df_ordenado.reindex(columns=['distrito', 'categoría', 'key',  'emails', 'teléfonos', 'nombre', 'apellido', 'modalidad', 'paycon', 'referenciaPago', 'montoPago', 'fechaPago', 'fuenteOrigen', 'montoApagar', 'close' ]) #Reordena las columnas como se mostraran

'df_ordenado : ', df_ordenado
cuentapaycon = df_ordenado['paycon'].value_counts()
cuentapaycon
#df_color = df_ordenado.style.apply(row_style, axis=1)
#df_color
#cuentaref = df_ordenado['referenciaPago'].value_counts()
#cuentaref
st.stop()
#claves = cuentaref.keys()
filas_a_revisar = df[df.duplicated(subset='referenciaPago', keep=False)]
filas_a_revisar
#df.loc[filas_a_revisar.index, 'paycon'] = 'En Revisión'
#df.loc[filas_a_revisar.index, 'close'] = False

#df = df.reindex(columns=['distrito', 'categoría', 'key',  'emails', 'teléfonos', 'nombre', 'apellido', 'modalidad', 'paycon', 'referenciaPago', 'montoPago', 'fechaPago', 'fuenteOrigen', 'montoApagar', 'close' ]) #Reordena las columnas como se mostraran
df_ordenado = df_ordenado.reindex(columns=['distrito', 'categoría', 'key',  'emails', 'teléfonos', 'nombre', 'apellido', 'modalidad', 'paycon', 'referenciaPago', 'montoPago', 'fechaPago', 'fuenteOrigen', 'montoApagar', 'close' ]) #Reordena las columnas como se mostraran

#df.style.apply(row_style, axis=1)  #Coloriza las filas

df_color = df_ordenado.style.apply(row_style, axis=1)    #Coloriza las filas 
st.subheader('Pagos Verificados')
df_color

conteopaycon = df['paycon'].value_counts()
conteopayconAll = dfPronda24['paycon'].value_counts()
st.subheader('Resumen de Pagos Verificados')
conteopaycon
'---'
st.subheader('Resumen de Pagos Completo')
conteopayconAll
st.subheader('Tabla completa de usuarios')
dfpronda_color = dfPronda24.style.apply(row_style, axis=1)    #Coloriza las filas
dfpronda_color
st.page_link("home2024.py", label="Inicio", icon="🏠")
st.stop()










