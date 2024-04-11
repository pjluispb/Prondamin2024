import streamlit as st
import pandas as pd

def main():
    st.title('Cargar y mostrar un archivo CSV')

    # Sección para cargar el archivo CSV
    st.sidebar.title('Cargar archivo CSV')
    uploaded_file = st.sidebar.file_uploader("Selecciona un archivo CSV", type=['csv'])

    # Sección para mostrar el DataFrame
    st.header('Contenido del archivo CSV')

    if uploaded_file is not None:
        # Leer el archivo CSV
        df = pd.read_csv(uploaded_file)

        # Verificar si el archivo es CSV
        if not uploaded_file.name.lower().endswith('.csv'):
            st.error('El archivo seleccionado no es un archivo CSV válido.')
            return

        # Verificar si la cabecera cumple con los campos requeridos
        if not check_csv_header(df.columns):
            st.error('El archivo CSV debe tener las siguientes columnas: Fecha, Descripcion, Referencia, Egreso, Ingreso.')
            return

        # Mostrar el DataFrame si todas las verificaciones son exitosas
        st.header('Contenido del archivo CSV')
        st.write(df)
    else:
        st.write('Carga un archivo CSV utilizando el panel lateral.')

if __name__ == '__main__':
    main()
