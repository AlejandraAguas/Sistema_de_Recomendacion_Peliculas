# Documentación del Código 

Este documento proporciona una descripción general del código utilizado para analizar un dataset de películas. El objetivo es mostrar cómo se procesaron y visualizaron los datos para obtener insights útiles. A continuación se detalla el flujo de trabajo y las visualizaciones realizadas.

**Código:**
```python

## 1. Importación de Librerías

El código comienza importando las siguientes librerías:

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

## 2. Carga del Dataset
Se carga el dataset desde un archivo CSV

df = pd.read_csv("data_transf.csv")

## 3. Distribución de Géneros de Películas
Se visualiza la distribución de géneros de películas mediante un gráfico de barras:

genre_counts = df['genres_name'].str.split(', ').explode().value_counts()
genre_counts.plot(kind='bar', figsize=(10, 6))
plt.xlabel('Género')
plt.ylabel('Cantidad de Películas')
plt.title('Distribución de Géneros')
plt.show()

Este gráfico muestra la cantidad de películas por género.

## 4. Tendencia de Lanzamientos por Año
Se representa la cantidad de películas lanzadas por año en un gráfico de líneas:

df['release_year'] = pd.to_datetime(df['release_date']).dt.year
year_counts = df['release_year'].value_counts().sort_index()
year_counts.plot(kind='line', marker='o', figsize=(10, 6))
plt.xlabel('Año de Lanzamiento')
plt.ylabel('Cantidad de Películas')
plt.title('Tendencia de Lanzamientos por Año')
plt.show()

Este gráfico ilustra cómo ha cambiado la cantidad de películas lanzadas a lo largo de los años.

## 5. Distribución de Puntuaciones Promedio
Se crea un histograma para mostrar la distribución de las puntuaciones promedio de las películas:

df['vote_average'].hist(bins=20)
plt.xlabel('Puntuación Promedio')
plt.ylabel('Frecuencia')
plt.title('Distribución de Puntuaciones')
plt.show()

Este histograma muestra la frecuencia de las diferentes puntuaciones promedio.

## 6. Directores Más Frecuentes
Se identifican los directores más involucrados en las películas mediante un gráfico de barras:

director_counts = df['director'].value_counts()
director_counts[:10].plot(kind='bar', figsize=(10, 6))
plt.xlabel('Director')
plt.ylabel('Cantidad de Películas')
plt.title('Directores más Frecuentes')
plt.show()

Este gráfico presenta los diez directores que han dirigido más películas.

## 7. Nube de Palabras para Títulos de Películas
Se genera una nube de palabras a partir de los títulos de las películas:

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df['title']))
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Nube de Palabras para Títulos de Películas')
plt.show()

La nube de palabras proporciona una representación visual de las palabras más comunes en los títulos de las películas.

Este análisis permite explorar diferentes aspectos del dataset de películas y facilita la comprensión de patrones y tendencias en los datos.