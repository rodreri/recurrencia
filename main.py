import streamlit as st
import pandas as pd
import numpy as np

st.title('Reporte de recurrencia SiteScope')

# Fucnion para poder cargar los CSV
def load_data():
    data = pd.read_csv('sites/FULL.csv')
    data = data.drop(['Unnamed: 0'], axis=1)
    return data

# Cargamos los csv
data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Datos cargados con exito")

# Datos originales antes de procesar
if st.checkbox('Mostrar tabla original'):
    st.subheader('Alertas...')
    st.write(data)
    
# Alertas por servicio
if st.checkbox('Alertas por servicio'):
    st.subheader('Alertas por servicio')
    names = data['Grupo'].str.split(':', expand=True)
    names.columns = ['Servicio', 'Tipo1', 'Tipo2', 'Tipo3', 'Tipo4', 'Tipo5']
    df = pd.concat([data, names], axis=1)
    # st.write(df
    st.write(df["Servicio"].value_counts())
    st.bar_chart(df["Servicio"].value_counts())

    if st.checkbox('Ver TOP 10'):
        st.header('Top 10')
        st.write(df["Servicio"].value_counts().head(10))
        st.bar_chart(df["Servicio"].value_counts().head(10))

    st.subheader('Mostar alertas por servicio')
    df['Agrupa'] = df[['Servicio', 'Monitor']].apply(lambda x: ' '.join(x), axis = 1) 
    df = df.drop(['Tipo1', 'Tipo2', 'Tipo3', 'Tipo4', 'Tipo5', 'Tipo3', 'Monitor', 'Grupo', 'Fecha'], axis=1)

    by_year = df.sort_values('Servicio',ascending=False)
    # st.write(by_year.groupby(['Agrupa']).count())

    df = df.drop(['Agrupa'], axis=1)
    df = df.drop_duplicates()

    option = st.selectbox('Selecciona servicio del que deseas ver detalle', (df))

    aux=by_year[by_year["Agrupa"].str.contains(option, case=False)]

    aux = aux.sort_values('Servicio',ascending=False)
    st.write(aux.groupby(['Agrupa']).count())

# Metricas
if st.checkbox('Alerta por metrica'):
    st.header('Monitores alertados')
    st.write(data["Monitor"].value_counts())

# Analisis de los datos 
if st.checkbox('Analisis de los datos'):
    names = data['Grupo'].str.split(':', expand=True)
    names.columns = ['Servicio', 'Tipo1', 'Tipo2', 'Tipo3', 'Tipo4', 'Tipo5']
    df = pd.concat([data, names], axis=1)

    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df["Time"] = df["Fecha"].dt.time
    df["Date"] = df["Fecha"].dt.date

    # Analisis por fecha
    st.subheader('Numero de alertas por fecha')
    st.write(df["Date"].value_counts())
    st.bar_chart(df["Date"].value_counts())

    # Analisis por hora
    st.subheader('Numero de alertas por hora')
    hist_values = np.histogram(df['Fecha'].dt.hour, bins=24, range=(0,24))[0]
    st.bar_chart(hist_values)

    # Slider para seleccionar la hora
    hour_to_filter = st.slider('hour', 0, 23, 17)
    filtered_data = df[df['Fecha'].dt.hour == hour_to_filter]
    st.write(filtered_data["Servicio"].value_counts())