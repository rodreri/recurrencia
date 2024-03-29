import streamlit as st
import pandas as pd
import numpy as np

st.title('Reporte de recurrencia SiteScope')

data = pd.DataFrame()

uploaded_files = st.file_uploader("Elige los 5 CSV de los sites", accept_multiple_files=True)
for uploaded_file in uploaded_files:

    datas = pd.read_csv(uploaded_file, skiprows=1,index_col=False)
    shape = datas.shape

    if(shape[1] == 5):
        datas = datas.drop(['Tipo', 'Mensaje'], axis=1)
        datas.columns = ['Fecha','Monitor','Grupo']
    else:
        datas = datas.drop(['Tipo', 'Estado', 'Mensaje', 'Unnamed: 6'], axis=1)
    
    update=datas[datas["Monitor"].str.contains("UPDATE", case=False)].index
    datas=datas.drop(update)
    relay=datas[datas["Monitor"].str.contains("RELAY", case=False)].index
    datas=datas.drop(relay)
    healt=datas[datas["Monitor"].str.contains("HEALT", case=False)].index
    datas=datas.drop(healt)
    top=datas[datas["Monitor"].str.contains("TOPREPORT", case=False)].index
    datas=datas.drop(top)

    data = pd.concat([data, datas], axis=0)

# Variables para resumen

# st.write(data.shape[0])
totalAlertas = data.shape[0]
alertasProcesadas = 0
df = pd.DataFrame()


# Borramos vcenter que no sirve para absoluatamente nada
vcenter=data[data["Grupo"].str.contains("VCENTER", case=False)].index
data=data.drop(vcenter)

# Borramos datamart que no sirve para absoluatamente nada
datamart=data[data["Grupo"].str.contains("DATAMART", case=False)].index
data=data.drop(datamart)

# Desde aqui no tocar

# Datos originales antes de procesar
if st.checkbox('Mostrar tabla original'):
    st.subheader('Alertas...')
    st.write(data)
    st.write(data.shape)
alertasProcesadas = data.shape[0]

st.subheader("Resumen")

st.write(f"""
  Una vez eliminadas las alertas de Update, Relay, Healt y TopReport, se tienen {totalAlertas} alertas, eliminando
  las alertas de VCENTER y DATAMART nos queda la cantidad de {alertasProcesadas} alertas, con las cuales se realiza el análisis
""")

# Alertas por servicio
if st.checkbox('Alertas por servicio'):

    st.subheader('Alertas por servicio')
    names = data['Grupo'].str.split(':', expand=True)
    names.columns = ['Servicio', 'Tipo1', 'Tipo2', 'Tipo3', 'Tipo4', 'Tipo5']
    df = pd.concat([data, names], axis=1)
    # st.write(df
    st.header('Top 10')
    st.write(df["Servicio"].value_counts().head(10))
    st.bar_chart(df["Servicio"].value_counts().head(10))

    

    if st.checkbox('Ver detalle'):
        st.write(df["Servicio"].value_counts())
        st.bar_chart(df["Servicio"].value_counts())
        

    st.subheader('Mostar alertas por servicio')
    df['Agrupa'] = df[['Servicio', 'Monitor']].apply(lambda x: ' '.join(x), axis = 1) 
    df = df.drop(['Tipo1', 'Tipo2', 'Tipo3', 'Tipo4', 'Tipo5', 'Tipo3', 'Monitor', 'Grupo', 'Fecha'], axis=1)

    by_year = df.sort_values('Servicio',ascending=False)
    # st.write(by_year.groupby(['Agrupa']).count())

    df = df.drop(['Agrupa'], axis=1)
    df = df.drop_duplicates()

    option = st.selectbox('Selecciona servicio del que deseas ver detalle', (df))

    aux=by_year[by_year["Agrupa"].str.contains(option, case=False)]

    aux = aux.sort_values('Servicio',ascending=True)
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

    # df['Fecha'] = pd.to_datetime(df['Fecha'])
    # df['Fecha'] = pd.to_datetime(df['Fecha'], format='%y/%d/%m %H:%M:%S')
    df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True)
    df["Time"] = df["Fecha"].dt.time
    df["Date"] = df["Fecha"].dt.date

    # st.write(df)

    # Analisis por fecha
    st.subheader('Numero de alertas por fecha')
    # st.write(df["Date"].value_counts())
    # st.write(df["Date"].value_counts().shape)
    st.bar_chart(df["Date"].value_counts())

    # Analisis por hora
    st.subheader('Numero de alertas por hora')
    hist_values = np.histogram(df['Fecha'].dt.hour, bins=24, range=(0,24))[0]
    st.bar_chart(hist_values)

    st.write("""
    Desliza el slider para seleccionar una hora, a continuacion se mostrara el servicio y la cantidad de alertas que presento en esa hora

    """)
    # Slider para seleccionar la hora
    hour_to_filter = st.slider('hour', 0, 23, 17)
    filtered_data = df[df['Fecha'].dt.hour == hour_to_filter]
    st.write(filtered_data["Servicio"].value_counts())