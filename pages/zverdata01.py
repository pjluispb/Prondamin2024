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
    return (pd.Dataframe(PPendiente.items))
    
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
    return pd.DataFrame(dfall_items)
    
#df, lastdf, countdf = load_data()
#df,  lastdf,  countdf

tab1, tab2, tab3 = st.tabs(["Todo", "Todo_color", "Pendiente"])
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
