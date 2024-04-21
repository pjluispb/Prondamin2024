import pandas as pd
import streamlit as st
from deta import Deta

deta = Deta(st.secrets["deta_key"])
Pronda = deta.Base('Prondamin2024C')

Pronda.delete(" 15733073 ")

