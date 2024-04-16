import streamlit as st
import pandas as pd
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
    else:
        return pd.Series('', row.index)

def update_paycon(row):
    fmontoPago = float(row['montoPago']) if row['montoPago'] not in ('-', None, '') else 0
    fmontoApagar = float(row['montoApagar']) if row['montoApagar'] not in ('-', None, '') else 0
    #if row['paycon'] not in ('PENDIENTE', 'NO'):
    diferencia = fmontoPago - fmontoApagar
    #st.write(diferencia, row['referenciaPago'])
    #if diferencia!=0:
    if -10 <= diferencia <= 10:
        return 'SI'
    elif diferencia < -10:
        return 'PENDIENTE X DIFERENCIA'
    elif diferencia > 10:
        return 'SI++'
    else:
        return row['paycon']  # Keep the original value if none of the conditions apply
    #else:
    #    return row['paycon']

def color_paycon(val):
    color = 'green' if val == 'SI' else 'white'
    return 'background-color: %s' % color  


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

# if logina['tipou']=='Registrador Financiero':
#     st.subheader('Bienvenid@ ' + logina['user'])
# else:
#     st.switch_page('home2024.py')

def check_csv_header(header):
    #required_columns = ['Fecha', 'Descripcion', 'Referencia', 'Egreso', 'Ingreso']
    required_columns = ['FECHA', 'DESCRIPCION', 'REFERENCIA', 'EGRESO', 'INGRESO']
    return all(column in header for column in required_columns)
    
# Carga el archivo CSV desde el usuario
uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])        
#uploaded_file = 'CTAPRONDAMIN1-1.csv'

if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame
    df = pd.read_csv(uploaded_file)                                          
    # Lee el DataFrame En modo local:
    #df = pd.read_csv('C:/Users/user/Downloads/CTAPRONDAMIN1-1.csv')

    # Verificar si el archivo es CSV
    if not uploaded_file.name.lower().endswith('.csv'):                     
        st.error('El archivo seleccionado no es un archivo CSV válido.')

    # Verificar si la cabecera cumple con los campos requeridos               
    elif not check_csv_header(df.columns):
        st.error('El archivo CSV debe tener las siguientes columnas: Fecha, Descripcion, Referencia, Egreso, Ingreso.')

    else:
        #trabajaEldf = True
        #if trabajaEldf:
        # Mostrar el DataFrame si todas las verificaciones son exitosas
        # extrae del dataframe solo cuando la descripcion = pago movil o transferencia
        dfingresoXpm = df[df['DESCRIPCION'] == 'NC - PAGO MOVIL INTERBANCARIO']
        dfingresoXtrans = df[df['DESCRIPCION'] == 'NC - TRANSFERENCIA DE FONDOS VIA INTERNET']
        frames = [dfingresoXpm, dfingresoXtrans]
        dfingreso = pd.concat(frames)
        # Muestra el DataFrame
        st.header('Ingresos registrados por el banco')
        st.write('solamente pago móvil y transferencias')
        st.write(dfingreso)
        st.stop()

