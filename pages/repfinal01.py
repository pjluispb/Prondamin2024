
import streamlit as st
import pandas as pd
from deta import Deta
from PIL import Image
import time

deta = Deta(st.secrets["deta_key"])

@st.cache_data
def load_data02():
    Pronda24 = deta.Base('jota_db')
    res = Pronda24.fetch(limit=500)
    all_items = res.items
    while res.last:
        res = Pronda24.fetch(last=res.last)
        all_items += res.items
    dfall_items = pd.DataFrame(all_items)
    return dfall_items

acceso = st.text_input('clave de acceso : ', type='password')
if acceso == 'j0tA':
    dfPronda = load_data02()
    dfPronda.drop(columns=['REPORTECERTIF'], inplace=True)
    dfPronda.rename(columns={'Total del curso (Real)':'Nota'}, inplace=True)
    #dfPronda['EMAIL'] = dfPronda['EMAIL'].apply(lambda x: str(x[0]) if x else '')
    'prondamin2024 - final : ', dfPronda

    if st.button("Clear All"):
        # Clear values from *all* all in-memory and on-disk data caches:
        # i.e. clear values from both square and cube
        st.cache_data.clear()


    '---'
    Dcentro = dfPronda.loc[dfPronda['DISTRITO']=='Centro']
    'Dcentro : ', Dcentro
    Ldcentro = Dcentro['CURSOREALIZADO'].value_counts()
    Ldcentro

    '---'
    Dcentrollanos = dfPronda.loc[dfPronda['DISTRITO']=='Centro Llanos']
    'Dcentrollanos : ', Dcentrollanos
    Ldcentrollanos = Dcentrollanos['CURSOREALIZADO'].value_counts()
    Ldcentrollanos

    '---'
    Dfalcon = dfPronda.loc[dfPronda['DISTRITO']=='Falcón']
    'Dfalcon : ', Dfalcon
    Ldfalcon = Dfalcon['CURSOREALIZADO'].value_counts()
    Ldfalcon

    '---'
    Dlara = dfPronda.loc[dfPronda['DISTRITO']=='Lara']
    'Dlara : ', Dlara
    Ldlara = Dlara['CURSOREALIZADO'].value_counts()
    Ldlara

    '---'
    Dllanosoccidentales = dfPronda.loc[dfPronda['DISTRITO']=='Llanos Occidentales']
    'Dllanosoccidentales : ', Dllanosoccidentales
    Ldllanoso = Dllanosoccidentales['CURSOREALIZADO'].value_counts()
    Ldllanoso

    '---'
    Dmetropolitano = dfPronda.loc[dfPronda['DISTRITO']=='Metropolitano']
    'Dmetropolitano : ', Dmetropolitano
    Ldmetro = Dmetropolitano['CURSOREALIZADO'].value_counts()
    Ldmetro

    '---'
    Dnororiente = dfPronda.loc[dfPronda['DISTRITO']=='Nor Oriente']
    'Dnororiente : ', Dnororiente
    Ldnoro = Dnororiente['CURSOREALIZADO'].value_counts()
    Ldnoro

    '---'
    Dsuroriente = dfPronda.loc[dfPronda['DISTRITO']=='Sur Oriente']
    'Dsuroriente : ', Dsuroriente
    Ldsuro = Dsuroriente['CURSOREALIZADO'].value_counts()
    Ldsuro

    '---'
    Dyaracuy = dfPronda.loc[dfPronda['DISTRITO']=='Yaracuy']
    'Dyaracuy : ', Dyaracuy
    Ldyara = Dyaracuy['CURSOREALIZADO'].value_counts()
    Ldyara

    '---'
    Dzulia = dfPronda.loc[dfPronda['DISTRITO']=='Zulia']
    'Dzulia : ', Dzulia
    Ldzulia = Dzulia['CURSOREALIZADO'].value_counts()
    Ldzulia