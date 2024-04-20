import streamlit as st
import pandas as pd
from deta import Deta
from PIL import Image
import time

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
    diferencia = fmontoPago - fmontoApagar
    #st.toast('referencia ='+str(row['referenciaPago']))
    
    if -10 <= diferencia <= 10:
        return 'SI'
    elif diferencia < -10:
        return 'PENDIENTE X DIFERENCIA'
    elif diferencia > 10:
        return 'SI++'
    else:
        return row['paycon']  # Keep the original value if none of the conditions apply


def color_paycon(val):
    color = 'green' if val == 'SI' else 'white'
    return 'background-color: %s' % color  

@st.cache_data
def load_data02():
    Pronda24 = deta.Base('Prondamin2024C')
    res = Pronda24.fetch()
    all_items = res.items

    while res.last:
        res = Pronda24.fetch(last=res.last)
        all_items += res.items
    dfall_items = pd.DataFrame(all_items, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfall_items
    
# Carga la bd de accesos
accesos = deta.Base('minec-accesos')
res=accesos.fetch()
# try:
#     logina = st.session_state['logina']
# except:
#     st.switch_page('home2024.py')

# Prondamin24 = deta.Base('Prondamin2024C')
# Pronda24 = Prondamin24.fetch(limit=5000)
# dfPronda24 = pd.DataFrame(Pronda24.items)
# dfPronda24

# Carga el Pronda
dfPronda24 = load_data02()

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
    required_columns = ['FECHA', 'DESCRIPCION', 'REFERENCIA', 'EGRESO', 'INGRESO']
    return all(column in header for column in required_columns)
    
# Carga el archivo CSV desde el usuario
st.header('Procesar Pagos')
uploaded_file = st.file_uploader("Subir archivo CSV con los datos bancarios", type=["csv"])        

if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame
    df = pd.read_csv(uploaded_file)                                          

    # Verificar si el archivo es CSV
    if not uploaded_file.name.lower().endswith('.csv'):                     
        st.error('El archivo seleccionado no es un archivo CSV válido.')

    # Verificar si la cabecera cumple con los campos requeridos               
    elif not check_csv_header(df.columns):
        st.error('El archivo CSV debe tener las siguientes columnas: FECHA, DESCRIPCION, REFERENCIA, EGRESO, INGRESO.')

    else:
        # Mostrar el DataFrame si todas las verificaciones son exitosas
        # extrae del dataframe solo cuando la descripcion = pago movil o transferencia
        dfingresoXpmi = df[df['DESCRIPCION'] == 'NC - PAGO MOVIL INTERBANCARIO']
        dfingresoXpm = df[df['DESCRIPCION'] == 'NC - PAGO MOVIL']
        dfingresoXtrans = df[df['DESCRIPCION'] == 'NC - TRANSFERENCIA DE FONDOS VIA INTERNET']
        dfingresoXcre = df[df['DESCRIPCION'] == 'NC - CREDITO INMEDIATO CAMARA DE COMPENSACION']
        frames = [dfingresoXpmi, dfingresoXpm, dfingresoXtrans, dfingresoXcre]
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
        'DatBan = ', DatBan
        # Compara DatBan.REFERENCIA con dfPronda24.referenciaPago y cuando sean iguales
        # lo coloca en el df:DatBanVerif...
        DatBan['REFERENCIA'] = DatBan['REFERENCIA'].astype(str)
        dfPronda24['referenciaPago'] = dfPronda24['referenciaPago'].astype(str)
        dfPronda24['referenciaPago']
        DatBanVerif = DatBan[DatBan['REFERENCIA'].isin(dfPronda24['referenciaPago'])]
        DatBanVerif1 = DatBanVerif.rename(columns={'REFERENCIA': 'key'})
        st.subheader('Pagos(referencias) encontrados ')
        DatBanVerif1

        # grabo DatBanVerif en Deta BD: DBanVerif2024
        dbvreg = DatBanVerif1.to_dict('records')
        dbvreg
        cont=1
        for registro in dbvreg:
            #registro
            DBanV24.put(registro)                                                       
            st.toast('se ha cargado el registro: '+str(cont))
            cont+=1
        st.toast('--->registros bancarios guardados<---')

        referencias = set(DatBanVerif1['key'])
        dfPronda24_refO = dfPronda24[dfPronda24['referenciaPago'].isin(referencias)]
        conteopayconprondaref = dfPronda24_refO['paycon'].value_counts()
        'conteopayconprondaref : ',conteopayconprondaref

        dfPronda24_ref = dfPronda24_refO

        #-------------------------------------------------------------------------
        #A continuación selecciona de Pronda aquellos registros donde:
        #                            close == False
        #                            si close No existe, lo inicializa a False
        #try:                                                                          # Aqui se agrega campo close = False
        #    dfPronda24_ref = dfPronda24_refO.loc[dfPronda24_refO['close']==False]
        #    conteopayconprondaref2 = dfPronda24_ref['close'].value_counts()
        #    conteopayconprondaref2
        #except:
        #    dfPronda24_ref = dfPronda24_refO
        #    dfPronda24_ref['close'] = False
        #-------------------------------------------------------------------------

        'dfPronda24_ref = ', dfPronda24_ref
        DatBanVerif.rename(columns={'REFERENCIA':'referenciaPago'}, inplace=True)
        'DatBanVerif = ', DatBanVerif
        dfpyd = pd.merge(dfPronda24_ref, DatBanVerif, on='referenciaPago', how='left')   # Mezcla Pronda y DatBanVerif
        dfpyd['montoPago'] = dfpyd['INGRESO'].fillna(dfpyd['montoPago'])
        'dfpyd = ', dfpyd
        #------------------------------st.stop()
        '**************************************'
        dfpyd = dfpyd.drop(columns=['FECHA', 'DESCRIPCION', 'INGRESO'])
        dfpyd['paycon'] = dfpyd.apply(update_paycon, axis=1)                  # Actualiza paycon en dfpyd

        dfpyd['Status'] = dfpyd['Status'].fillna('-')                         # Coloca Status = '-' cuando valga None
        dfpyd['ReporteCertif'] = dfpyd['ReporteCertif'].fillna('-')           # Coloca ReporteCertif = '-' cuando valga None
        dfpyd['curso'] = dfpyd['curso'].fillna('-')                           # Coloca curso = '-' cuando valga None
        dfpyd['Categoría Actual'] = dfpyd['Categoría Actual'].fillna('-')     # Coloca Categoría Actual = '-' cuando valga None
        dfpyd['Cédula'] = dfpyd['Cédula'].fillna('-')                         # Coloca Cédula = '-' cuando valga None
        dfpyd.loc[dfpyd['paycon']=='SI', 'close'] = True                       # Coloca close = True si paycon = SI
        dfpyd.loc[dfpyd['paycon']=='SI++', 'close'] = False                    # Coloca close = False si paycon = SI++
        dfpyd.loc[dfpyd['paycon']=='PENDIENTE X DIFERENCIA', 'close'] = False  # Coloca close = False si paycon = PENDIENTE X DIFERENCIA
        dfpyd.loc[dfpyd['paycon']=='PENDIENTE', 'close'] = False               # Coloca close = False si paycon = PENDIENTE
        dfpyd_ordenado = dfpyd.sort_values(by='paycon', ascending=False)      # Ordena el dataframe por columna paycon
        dfpyd_color = dfpyd_ordenado.style.apply(row_style, axis=1)           # Coloriza filas del dataframe
        st.subheader('Registros con pagos verificados')
        dfpyd_color
        conteopaycon = dfpyd_ordenado['paycon'].value_counts()
        conteodistrito = dfpyd_ordenado['distrito'].value_counts()
        st.subheader('Status de pagos procesados')
        conteopaycon
        st.subheader('Pagos verificados X distrito') 
        conteodistrito
        #-----------------------------------------st.stop()
        dfpydReg = dfpyd_ordenado.to_dict('records')
        contador = 1
        for registro in dfpydReg:
            #contador, registro
            rkey = registro['key']
            st.toast('se ha cargado el registro: '+str(contador)+' RegCed# '+str(rkey))
            Prondamin24.put(registro)
            contador+=1

st.page_link("home2024.py", label="Inicio", icon="🏠")
#st.stop()

