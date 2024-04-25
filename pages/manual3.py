import streamlit as st
import pandas as pd
from deta import Deta
from PIL import Image
import time



dfsis = dfPronda[dfPronda['paycon'] == 'SI']
dfsim = dfPronda[dfPronda['paycon'] == 'SI++']
dfSI = pd.concat([dfsis, dfsim])
dfnoSI = dfPronda.loc[~dfPronda.index.isin(dfSI.index)]
dfPronda24 = dfnoSI
