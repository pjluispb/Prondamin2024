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

        # Construye nuevo dataframe DatBan con referencia e ingreso formateados para el match con Pronda
        # es decir, los ultimos 4 digitos de la referencia y sustituir la coma por punto en los montos
        DatBan = dfingreso.reindex(columns=['FECHA', 'DESCRIPCION', 'REFERENCIA', 'INGRESO'])
        DatBan['REFERENCIA'] = df['REFERENCIA'].apply(lambda x: str(x)[-4:])
        try:
            DatBan['INGRESO'] = DatBan['INGRESO'].str.replace(',', '.').astype(float)
        except:
            pass
        DatBan['INGRESO'] = pd.to_numeric(DatBan['INGRESO'])
        
        # Compara DatBan.REFERENCIA con dfPronda24.referenciaPago y cuando sean iguales
        # lo coloca en el df:DatBanVerif...
        DatBan['REFERENCIA'] = DatBan['REFERENCIA'].astype(str)
        dfPronda24['referenciaPago'] = dfPronda24['referenciaPago'].astype(str)
        
        DatBanVerif = DatBan[DatBan['REFERENCIA'].isin(dfPronda24['referenciaPago'])]
        DatBanVerif1 = DatBanVerif.rename(columns={'REFERENCIA': 'key'})
        st.subheader('Pagos(referencias) encontrados ')
        DatBanVerif1

        # grabo DatBanVerif en Deta BD: DBanVerif2024
        dbvreg = DatBanVerif1.to_dict('records')
        cont=1
        for registro in dbvreg:
            #registro
            #DBanV24.put(registro)                                                       
            st.toast('se ha cargado el registro: '+str(cont))
            cont+=1
        st.toast('--->registros bancarios guardados<---')

        referencias = set(DatBanVerif1['key'])
        #dfPronda24.loc[dfPronda24['referenciaPago'].isin(referencias), 'paycon'] = 'SI'
        dfPronda24_refO = dfPronda24[dfPronda24['referenciaPago'].isin(referencias)]

        # 'dfPronda24_refO'
        # dfPronda24_refO
        conteopayconprondaref = dfPronda24_refO['paycon'].value_counts()
        # conteopayconprondaref
        #====>>> Prueba quitar los registros donde close == True                     <<<<======== Prueba
        try:
            dfPronda24_ref = dfPronda24_refO.loc[dfPronda24_refO['close']==False]
            # 'dfPronda24_ref -- donde close == Not True'
            # dfPronda24_ref
            conteopayconprondaref2 = dfPronda24_ref['close'].value_counts()
            # conteopayconprondaref2
        except:
            dfPronda24_ref = dfPronda24_refO
            # 'No aparece campo close!!!....se crea campo close=False'
            dfPronda24_ref['close'] = False
            # dfPronda24_ref
        #====>>> Prueba quitar los registros donde close == True  
        #'---'
        DatBanVerif.rename(columns={'REFERENCIA':'referenciaPago'}, inplace=True)
        dfpyd = pd.merge(dfPronda24_ref, DatBanVerif, on='referenciaPago', how='left')   # Mezcla Pronda y DatBanVerif
        dfpyd['montoPago'] = dfpyd['INGRESO'].fillna(dfpyd['montoPago'])
        '**************************************'

        dfpyd = dfpyd.drop(columns=['FECHA', 'DESCRIPCION', 'INGRESO'])
        dfpyd['paycon'] = dfpyd.apply(update_paycon, axis=1)                  # Actualiza paycon en dfpyd

        dfpyd['Status'] = dfpyd['Status'].fillna('-')                         # Coloca Status = '-' cuando valga None
        dfpyd['ReporteCertif'] = dfpyd['ReporteCertif'].fillna('-')           # Coloca ReporteCertif = '-' cuando valga None
        dfpyd['curso'] = dfpyd['curso'].fillna('-')                           # Coloca curso = '-' cuando valga None
        dfpyd['Categoría Actual'] = dfpyd['Categoría Actual'].fillna('-')     # Coloca Categoría Actual = '-' cuando valga None
        dfpyd['Cédula'] = dfpyd['Cédula'].fillna('-')                         # Coloca Cédula = '-' cuando valga None
        dfpyd.loc[dfpyd['paycon']=='SI', 'close'] = True                      # Coloca close = True si paycon = SI
        dfpyd_ordenado = dfpyd.sort_values(by='paycon', ascending=False)      # Ordena el dataframe por columna paycon
        dfpyd_color = dfpyd_ordenado.style.apply(row_style, axis=1)           # Coloriza filas del dataframe
        'dfpyd ordenado y colorizado'
        #dfpyd_ordenado
        dfpyd_color
        conteopaycon = dfpyd_ordenado['paycon'].value_counts()
        conteodistrito = dfpyd_ordenado['distrito'].value_counts()
        st.subheader('Status de pagos procesados')
        conteopaycon
        st.subheader('Pagos verificados X distrito') 
        conteodistrito

        dfpydReg = dfpyd_ordenado.to_dict('records')
        contador = 1
        for registro in dfpydReg:
            contador, registro
            #Prondamin24.put(registro)
            contador+=1
        st.stop()

