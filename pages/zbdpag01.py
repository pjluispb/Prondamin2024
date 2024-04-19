
import streamlit as st
import pandas as pd
from deta import Deta


deta = Deta(st.secrets["deta_key"])

# Simulando la conexión a la base de datos y obteniendo el DataFrame
# data = pd.read_sql_query("SELECT * FROM tabla", connection)
# Supongamos que tienes un DataFrame llamado 'data'


# # Carga el Pronda
Prondamin24 = deta.Base('Prondamin2024C')
Pronda24 = Prondamin24.fetch(limit=3500).items
#dfPronda24 = pd.DataFrame(Pronda24)

# Simulación de un DataFrame con 4000 filas
#data = pd.DataFrame({"key": range(4000), "nombre": range(4000), "apellido": range(4000), "categoría": range(4000), "distrito": range(4000), "paycon": range(4000)})
data = pd.DataFrame(Pronda24)

# Ordenar el DataFrame por una columna específica
columna_orden = st.sidebar.selectbox("Selecciona la columna para ordenar:", options=data.columns)
data_sorted = data.sort_values(by=columna_orden)

# Número de filas por página
rows_per_page = 100

# Número total de páginas
total_pages = len(data) // rows_per_page + 1

# Barra lateral para seleccionar la página
page_number = st.sidebar.number_input("Selecciona la página:", min_value=1, max_value=total_pages)

# Calcular los índices de inicio y fin para la página seleccionada
start_index = (page_number - 1) * rows_per_page
end_index = min(start_index + rows_per_page, len(data))

# Filtrar el DataFrame para mostrar solo las filas de la página seleccionada
page_data = data.iloc[start_index:end_index]

# Mostrar el DataFrame
st.write(page_data)
