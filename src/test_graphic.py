import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Datos proporcionados
datos = {
    'Habilidad':  ['Smart', 'Thoughtful', 'Open', 'Adaptable', 'Trusted'],
    'Nivel': ['medium', 'low', 'high', 'high', 'medium']
}

datos = {'Habilidad': ['smart', 'thoughtful', 'open', 'adaptable', 'trusted'], 
         'Nivel': ['high', 'medium', 'low', 'high', 'medium']
         }

# Crear un DataFrame a partir de los datos
df = pd.DataFrame(datos)

# Definir el orden de las categorías en el eje x
orden_x = ['low', 'medium', 'high']

# Mapear los valores de 'Nivel' para que coincidan con el orden definido en 'orden_x'
df['Nivel'] = df['Nivel'].map({'low': 0, 'medium': 1, 'high': 2})

# Ordenar el DataFrame por los valores de 'Nivel'
df = df.sort_values(by='Nivel')

# Restaurar los valores originales de 'Nivel' para el etiquetado del gráfico
df['Nivel'] = df['Nivel'].map({0: 'low', 1: 'medium', 2: 'high'})

# Configurar el título de la aplicación
st.title('Niveles de Habilidades')

# Crear un gráfico de barras utilizando matplotlib
plt.figure(figsize=(10, 6))
plt.barh(df['Habilidad'], df['Nivel'], color='skyblue')
plt.xlabel('Nivel')
plt.ylabel('Habilidad')
plt.title('Niveles de Habilidades')
plt.grid(axis='x')

# Establecer el orden de las etiquetas del eje x
plt.xticks(ticks=[0, 1, 2], labels=orden_x)

# Mostrar el gráfico utilizando Streamlit
st.pyplot(plt)
