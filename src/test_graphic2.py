import streamlit as st
import pandas as pd
import plotly.express as px

# Datos de ejemplo: estudiantes y calificaciones
data = {
    'Estudiante': ['Juan', 'María', 'Pedro', 'Ana', 'Luis'],
    'Calificación': [90, 85, 75, 95, 80]
}

# Crear un DataFrame a partir de los datos
df = pd.DataFrame(data)

# Configurar el título de la aplicación
st.title('Calificaciones de Estudiantes')

# Crear un gráfico de barras horizontal utilizando Plotly Express
fig = px.bar(df, x='Calificación', y='Estudiante', orientation='h', color='Calificación', 
             color_continuous_scale=px.colors.sequential.Viridis, labels={'Estudiante': 'Estudiante', 'Calificación': 'Calificación'})

# Configurar el diseño del gráfico
fig.update_layout(title='Calificaciones de Estudiantes', xaxis_title='Calificación', yaxis_title='Estudiante',
                  font=dict(family="Arial", size=12, color="black"),
                  plot_bgcolor='rgba(0,0,0,0)',
                  paper_bgcolor='rgba(0,0,0,0)')

# Mostrar el gráfico utilizando Streamlit
st.plotly_chart(fig)
