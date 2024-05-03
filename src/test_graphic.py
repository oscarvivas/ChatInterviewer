import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Datos de ejemplo: estudiantes y calificaciones
data = {
    'name': ['Juan', 'María', 'Pedro', 'Ana', 'Luis'],
    'Rating': [90, 85, 75, 95, 80]
}

# Crear un DataFrame a partir de los datos
df = pd.DataFrame(data)

# Configurar el estilo de Seaborn para hacer el gráfico más vistoso
sns.set_style("whitegrid")

# Crear un gráfico de barras horizontal utilizando Seaborn
plt.figure(figsize=(10, 6))
barplot = sns.barplot(x='Rating', hue='name', data=df)

# Configurar título y etiquetas del gráfico
plt.title('Rating Candidates')
plt.xlabel('Rating')
plt.ylabel('Name')

# Mostrar el gráfico utilizando Streamlit
st.pyplot(barplot.figure)
