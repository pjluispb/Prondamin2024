import streamlit as st
import pandas as pd
from deta import Deta

deta = Deta(st.secrets["deta_key"])


def row_style(row):
    if row['paycon'] == 'SI++':
        return pd.Series('background-color: #7986cb; color:#000000', row.index)
    elif row['paycon'] == 'PENDIENTE X DIFERENCIA':
        return pd.Series('background-color: #ff6f00; color:#000000', row.index)
    elif row['paycon'] == 'SI':
        return pd.Series('background-color: #8ede99; color:#000000', row.index)
    elif row['paycon'] == 'PENDIENTE':
        return pd.Series('background-color: #fdd834; color:#000000', row.index)
    else:
        return pd.Series('', row.index)

def row_style_2(row):
    if row['Distrito'] in ('Andino', 'Centro Llanos', 'Lara', 'Llanos Occidentales', 'Nor Oriente', 'Yaracuy' ):
        return pd.Series('background-color: #8eddf9; color:#000000', row.index)
    else:
        return pd.Series('background-color: #eeeeee; color:#000229', row.index)

def row_style_3(row):
    if row['index']=='Ministro Licenciado' :
        return pd.Series('background-color: #eeeeee; color:#000229', row.index)


@st.cache_data
def load_data():
    # # Carga el Pronda
    Prondamin24 = deta.Base('Prondamin2024C')
    Pronda24 = Prondamin24.fetch(limit=4500)
    Pronda24items = Pronda24.items
    Pronda24last = Pronda24.last
    Pronda24count = Pronda24.count
    return (pd.DataFrame(Pronda24items), Pronda24last, Pronda24count)

@st.cache_data
def load_datapendiente():
    ProndaPendiente = deta.Base('Prondamin2024C')
    PPendiente = ProndaPendiente.fetch({'paycon':'PENDIENTE'})
    PPenitems = PPendiente.items
    dfpend = pd.DataFrame(PPenitems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return pd.DataFrame(dfpend)

@st.cache_data
def load_datasi():
    ProndaSI = deta.Base('Prondamin2024C')
    PSI = ProndaSI.fetch({'paycon':'SI'})
    PSItems = PSI.items
    dfsi = pd.DataFrame(PSItems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfsi

@st.cache_data
def load_datasimas():
    ProndaSImas = deta.Base('Prondamin2024C')
    PSImas = ProndaSImas.fetch({'paycon':'SI++'})
    PSImasitems = PSImas.items
    dfsmas = pd.DataFrame(PSImasitems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfsmas

@st.cache_data
def load_datadeficit():
    ProndaDeficit = deta.Base('Prondamin2024C')
    PDeficit = ProndaDeficit.fetch({'paycon':'PENDIENTE X DIFERENCIA'})
    PDeficititems = PDeficit.items
    dfDeficit = pd.DataFrame(PDeficititems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfDeficit
    
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
    
#df, lastdf, countdf = load_data()
#df,  lastdf,  countdf

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Todo", "Todo_color", "Por Confirmar", "Confirmado", "SI++", "P X D"])
with tab1:
    df2 = load_data02()
    df2
# df2 = df2.reindex(columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ]) #Reordena las columnas como se mostraran
with tab2:
    df2_color = df2.style.apply(row_style, axis=1)  #Coloriza las filas
    df2_color
with tab3:
    df3 = load_datapendiente()
    df3
with tab4:
    df4 = load_datasi()
    df4
with tab5:
    df4 = load_datasimas()
    df4
with tab6:
    df4 = load_datadeficit()
    df4
    
