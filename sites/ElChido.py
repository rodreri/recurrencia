import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

# Con estos hago los reportes individuales de cada SiteScope
nums = ['Sis1.csv', 'Sis2.csv', 'Sis3.csv', 'Sis5.csv']
for n in nums:
    data = pd.read_csv(n, skiprows=1,index_col=False)
    data = data.drop(['Tipo', 'Estado', 'Mensaje', 'Unnamed: 6'], axis=1)

    update=data[data["Monitor"].str.contains("UPDATE", case=False)].index
    data=data.drop(update)
    relay=data[data["Monitor"].str.contains("RELAY", case=False)].index
    data=data.drop(relay)
    healt=data[data["Monitor"].str.contains("HEALT", case=False)].index
    data=data.drop(healt)
    top=data[data["Monitor"].str.contains("TOPREPORT", case=False)].index
    data=data.drop(top)

    data.to_csv('Reporte'+n)

# Ahora junto los reportes en uno
data1 = pd.read_csv("ReporteSis1.csv")
data2 = pd.read_csv("ReporteSis2.csv")
data3 = pd.read_csv("ReporteSis3.csv")
data5 = pd.read_csv("ReporteSis5.csv")  

datas = pd.concat([data1, data2, data3, data5], axis=0)
datas = datas.drop(['Unnamed: 0'], axis=1)

vcenter=datas[datas["Grupo"].str.contains("VCENTER", case=False)].index
datas=datas.drop(vcenter)

datas.to_csv('FULL.csv')