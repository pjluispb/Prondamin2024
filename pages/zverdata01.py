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
def load_dttoAndino():
    ProndaAndino = deta.Base('Prondamin2024C')
    PAndino = ProndaAndino.fetch({'distrito':'Andino'})
    PAndinoitems = PAndino.items
    dfAndino = pd.DataFrame(PAndinoitems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfAndino

@st.cache_data
def load_dttoCentro():
    ProndaCentro = deta.Base('Prondamin2024C')
    PCentro = ProndaCentro.fetch({'distrito':'Centro'})
    PCentroitems = PCentro.items
    dfCentro = pd.DataFrame(PCentroitems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfCentro
    
@st.cache_data
def load_dttoCentroLLanos():
    ProndaCentroLLanos = deta.Base('Prondamin2024C')
    PCentroLLanos = ProndaCentroLLanos.fetch({'distrito':'Centro Llanos'})
    PCentroLLanositems = PCentroLLanos.items
    dfCentroLLanos = pd.DataFrame(PCentroLLanositems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfCentroLLanos

@st.cache_data
def load_dttoFalcon():
    ProndaFalcon = deta.Base('Prondamin2024C')
    PFalcon = ProndaFalcon.fetch({'distrito':'Falcón'})
    PFalconitems = PFalcon.items
    dfFalcon = pd.DataFrame(PFalconitems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfFalcon

@st.cache_data
def load_dttoLara():
    ProndaLara = deta.Base('Prondamin2024C')
    PLara = ProndaLara.fetch({'distrito':'Lara'})
    PLaraitems = PLara.items
    dfLara = pd.DataFrame(PLaraitems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfLara

@st.cache_data
def load_dttoLlanosO():
    ProndaLlanosO = deta.Base('Prondamin2024C')
    PLlanosO = ProndaLlanosO.fetch({'distrito':'Llanos Occidentales'})
    PLlanosOitems = PLlanosO.items
    dfLlanosO = pd.DataFrame(PLlanosOitems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfLlanosO

@st.cache_data
def load_dttoMetropolitano():
    ProndaMetropolitano = deta.Base('Prondamin2024C')
    PMetropolitano = ProndaMetropolitano.fetch({'distrito':'Metropolitano'})
    PMetropolitanoitems = PMetropolitano.items
    dfMetropolitano = pd.DataFrame(PMetropolitanoitems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfMetropolitano

@st.cache_data
def load_dttoNorOriente():
    ProndaNorOriente = deta.Base('Prondamin2024C')
    PNorOriente = ProndaNorOriente.fetch({'distrito':'Nor Oriente'})
    PNorOrienteitems = PNorOriente.items
    dfNorOriente = pd.DataFrame(PNorOrienteitems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfNorOriente

@st.cache_data
def load_dttoSurOriente():
    ProndaSurOriente = deta.Base('Prondamin2024C')
    PSurOriente = ProndaSurOriente.fetch({'distrito':'Sur Oriente'})
    PSurOrienteitems = PSurOriente.items
    dfSurOriente = pd.DataFrame(PSurOrienteitems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfSurOriente

@st.cache_data
def load_dttoYaracuy():
    ProndaYaracuy = deta.Base('Prondamin2024C')
    PYaracuy = ProndaYaracuy.fetch({'distrito':'Yaracuy'})
    PYaracuyitems = PYaracuy.items
    dfYaracuy = pd.DataFrame(PYaracuyitems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfYaracuy

@st.cache_data
def load_dttoZulia():
    ProndaZulia = deta.Base('Prondamin2024C')
    PZulia = ProndaZulia.fetch({'distrito':'Zulia'})
    PZuliaitems = PZulia.items
    dfZulia = pd.DataFrame(PZuliaitems, columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ])
    #dfall_items_color = dfall_items.style.apply(row_style, axis=1)
    return dfZulia
    
    
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

tab1, tab3, tab4, tab5, tab6, tab7, tab2 = st.tabs(["Todo", "Por Confirmar", "Confirmado", "SI++", "P X D", "Por Distrito", "Todo_color"])
with tab1:
    st.subheader('Todos los distritos')
    st.divider()
    df2 = load_data02()
    df2
# df2 = df2.reindex(columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ]) #Reordena las columnas como se mostraran

with tab3:
    st.subheader('Inscritos con Pagos PENDIENTES')
    st.write('Inscritos Pendientes de confirmación de pago')
    st.caption('paycon = PENDIENTE')
    st.divider()
    df3 = load_datapendiente()
    df3
with tab4:
    st.subheader('Inscritos con Pagos Confirmados  ')
    st.caption('paycon = SI')
    st.divider()
    df4 = load_datasi()
    df4
with tab5:
    st.subheader('Inscritos con Pagos Confirmados con exceso')
    st.caption('paycon = SI++')
    st.divider()
    df4 = load_datasimas()
    df4
with tab6:
    st.subheader('Inscritos con Pagos Confirmados en Déficit ')
    st.caption('paycon = PENDIENTE X DIFERENCIA')
    st.divider()
    df4 = load_datadeficit()
    df4

with tab7:
    st.subheader('Por Distrito')
    st.divider()
    with st.expander("Andino"):
        df5 = load_dttoAndino()
        df5_color = df5.style.apply(row_style, axis=1)
        df5_color
    with st.expander("Centro"):
        df6 = load_dttoCentro()
        df6_color = df6.style.apply(row_style, axis=1)
        df6_color
    with st.expander("Centro Llanos"):
        df7 = load_dttoCentroLLanos()
        df7_color = df7.style.apply(row_style, axis=1)
        df7_color
    with st.expander("Falcón"):
        df8 = load_dttoFalcon()
        df8_color = df8.style.apply(row_style, axis=1)
        df8_color
    with st.expander("Lara"):
        df8 = load_dttoLara()
        df8_color = df8.style.apply(row_style, axis=1)
        df8_color
    with st.expander("Llanos Occidentales"):
        df8 = load_dttoLlanosO()
        df8_color = df8.style.apply(row_style, axis=1)
        df8_color
    with st.expander("Metropolitano"):
        df9 = load_dttoMetropolitano()
        df9_color = df9.style.apply(row_style, axis=1)
        df9_color
    with st.expander("Nor Oriente"):
        df10 = load_dttoNorOriente()
        df10_color = df10.style.apply(row_style, axis=1)
        df10_color
    with st.expander("Sur Oriente"):
        df11 = load_dttoSurOriente()
        df11_color = df11.style.apply(row_style, axis=1)
        df11_color
    with st.expander("Yaracuy"):
        df12 = load_dttoYaracuy()
        df12_color = df12.style.apply(row_style, axis=1)
        df12_color
    with st.expander("Zulia"):
        df13 = load_dttoZulia()
        df13_color = df13.style.apply(row_style, axis=1)
        df13_color

with tab2:
    st.subheader('Todos los distritos')
    st.write('Coloreado a partir del campo paycon')
    st.divider()
    df2_color = df2.style.apply(row_style, axis=1)  #Coloriza las filas
    df2_color
    
    
