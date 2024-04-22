import pandas as pd
import streamlit as st
from deta import Deta

deta = Deta(st.secrets["deta_key"])
