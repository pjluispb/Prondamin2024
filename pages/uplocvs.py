
import streamlit as st
import pandas as pd
from deta import Deta

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
    if row['paycon'] not in ('PENDIENTE', 'NO'):
        diferencia = fmontoPago - fmontoApagar
        print(diferencia)
        if diferencia!=0:
            if -10 <= diferencia <= 10:
                return 'SI'
            elif diferencia < -10:
                return 'PENDIENTE X DIFERENCIA'
            elif diferencia > 10:
                return 'SI++'
            else:
                return row['paycon']  # Keep the original value if none of the conditions apply
    else:
        return row['paycon']

def color_paycon(val):
    color = 'green' if val == 'SI' else 'white'
    return 'background-color: %s' % color   

# Carga el Pronda
Prondamin24 = deta.Base('Pronda24Test')
Pronda24 = Prondamin24.fetch()
dfPronda24 = pd.DataFrame(Pronda24.items)
# dfPronda24

# Carga el DBanVerif2024 ...Datos Bancarios ya procesados
DBanV24 = deta.Base('DBanVerif2024')
DBanV24f = DBanV24.fetch().items
dfDBanV24 = pd.DataFrame(DBanV24f)

def check_csv_header(header):
    #required_columns = ['Fecha', 'Descripcion', 'Referencia', 'Egreso', 'Ingreso']
    required_columns = ['FECHA', 'DESCRIPCION', 'REFERENCIA', 'EGRESO', 'INGRESO']
    return all(column in header for column in required_columns)
    
# Carga el archivo CSV desde el usuario
uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame
    df = pd.read_csv(uploaded_file)

    # Verificar si el archivo es CSV
    if not uploaded_file.name.lower().endswith('.csv'):
        st.error('El archivo seleccionado no es un archivo CSV válido.')

    # Verificar si la cabecera cumple con los campos requeridos
    elif not check_csv_header(df.columns):
        st.error('El archivo CSV debe tener las siguientes columnas: Fecha, Descripcion, Referencia, Egreso, Ingreso.')

    else:
        # Mostrar el DataFrame si todas las verificaciones son exitosas
        
        # extrae del dataframe solo cuando la descripcion = pago movil o transferencia
        dfingresoXpm = df[df['DESCRIPCION'] == 'NC - PAGO MOVIL INTERBANCARIO']
        dfingresoXtrans = df[df['DESCRIPCION'] == 'NC - TRANSFERENCIA DE FONDOS VIA INTERNET']
        frames = [dfingresoXpm, dfingresoXtrans]
        dfingreso = pd.concat(frames)
        # Muestra el DataFrame
        st.header('Contenido del archivo CSV (solo los ingresos)')
        st.write(dfingreso)
        
        # Construye nuevo dataframe DatBan con referencia e ingreso formateados para el match con Pronda
        # es decir, los ultimos 4 digitos de la referencia y sustituir la coma por punto en los montos
        DatBan = dfingreso.reindex(columns=['FECHA', 'DESCRIPCION', 'REFERENCIA', 'INGRESO'])
        DatBan['REFERENCIA'] = df['REFERENCIA'].apply(lambda x: str(x)[-4:])

        DatBan['INGRESO'] = DatBan['INGRESO'].str.replace(',', '.').astype(float)
        DatBan['INGRESO'] = pd.to_numeric(DatBan['INGRESO'])
        
        # Compara DatBan.REFERENCIA con dfPronda24.referenciaPago y cuando sean iguales
        # lo coloca en el df:DatBanVerif...
        DatBan['REFERENCIA'] = DatBan['REFERENCIA'].astype(str)
        dfPronda24['referenciaPago'] = dfPronda24['referenciaPago'].astype(str)
        
        DatBanVerif = DatBan[DatBan['REFERENCIA'].isin(dfPronda24['referenciaPago'])]
        DatBanVerif1 = DatBanVerif.rename(columns={'REFERENCIA': 'key'})
        st.subheader('Registros del archivo CSV que coinciden con la data de las inscripciones')
        DatBanVerif1
        
        # grabo DatBanVerif en Deta BD: DBanVerif2024
        dbvreg = DatBanVerif1.to_dict('records')
        cont=1
        for registro in dbvreg:
            #registro
            DBanV24.put(registro)
            st.toast('se ha cargado el registro: '+str(cont))
            cont+=1
        
        referencias = set(DatBanVerif1['key'])
        dfPronda24.loc[dfPronda24['referenciaPago'].isin(referencias), 'paycon'] = 'SI'
        #dfPronda24.style.applymap(color_paycon, subset=['paycon'])
        dfPronda24['paycon'] = dfPronda24.apply(update_paycon, axis=1)                  # Actualiza el campo paycon en el dataframe
        dfPronda24_ordenado = dfPronda24.sort_values(by='paycon', ascending=False)      # Ordena el dataframe por columna paycon
        dfPronda24B = dfPronda24_ordenado.style.apply(row_style, axis=1)                # Coloriza las filas del dataframe
        st.header('Status de pago de los inscritos')
        dfPronda24B

        # graba dfPronda24B en Deta BD: Pronda24Test
        dbprondareg = dfPronda24.to_dict('records')
        contador = 1
        for registro in dbprondareg:
            if registro('paycon') in ('SI', 'SI++', 'PENDIENTE', 'PENDIENTE X DIFERENCIA'):
                registro
                

        



# lee csv desde detadrive
# deta = Deta(st.secrets["deta_key"])
# drive2024 = deta.Drive("datoscvsminec")
# dicPminec2024 =  drive2024.list()
# dicPminec2024

# response = drive2024.get("data2024-01bkp.csv")
# content = response.read()
# type(content)

# # content
# df = pd.read_csv(response)
# df = pd.read_csv(content)
# df
