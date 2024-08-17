# PROYECTO l - SISTEMA DE RECOMENDACIÓN DE PELíCULAS 

[![SISTEMA-DE-RECOMENDACION.jpg](https://i.postimg.cc/pL6tz45M/SISTEMA-DE-RECOMENDACION.jpg)](https://postimg.cc/YvYVwXxd)

## Contenido
- Objetivo
- Transformación de los Datos - ETL
- Análisis de los datos - EDA
- Creación de la API con FastAPI
- Documentos
- Requirements

## Objetivo
Desarrollar un sistema de recomendación de películas para una start-up que agrega plataformas de streaming, incluyendo la transformación de datos, la creación de una API para consultas y el desarrollo de un sistema de recomendación.

## Transformación de los datos - ETL
La transformación de datos busca preparar el dataset para el análisis y modelado mediante la limpieza, estructuración y enriquecimiento de la información. El objetivo es lograr un dataset limpio, bien estructurado y libre de valores nulos o inconsistencias, lo que facilita la creación de modelos de Machine Learning precisos y efectivos y permite realizar análisis significativos.

## Análisis de los datos - EDA
Se realiza un Análisis Exploratorio de Datos (EDA) para comprender en profundidad el dataset de películas. El EDA implica examinar la distribución de los datos, identificar patrones y outliers mediante histogramas y diagramas de caja, y analizar las relaciones entre variables con matrices de correlación y gráficos de dispersión. También se exploran datos categóricos y tendencias temporales usando gráficos de barras y líneas. Este análisis ayuda a detectar problemas en los datos y a preparar el dataset para el modelado, asegurando que el sistema de recomendación sea preciso y eficaz.

## Creación de la API con FastAPI
En este proyecto, hemos desarrollado una API utilizando FastAPI para ofrecer consultas interactivas sobre el dataset de películas. La API permite obtener información detallada sobre la cantidad de estrenos por mes y día, así como el score y los votos de películas específicas. También proporciona datos sobre el éxito de actores y directores, y ofrece recomendaciones de películas similares basadas en el título ingresado. La implementación de esta API facilita el acceso a la información y a las funcionalidades del sistema de recomendación de manera eficiente y escalable.


## Documentos
En esta sección se proporciona la documentación relacionada con diferentes aspectos del proyecto. A continuación, se ofrece un resumen de cada archivo de documentación y su propósito:

[EDA](Documentos/EDA_movies_credits.md): Documentación sobre el análisis exploratorio de datos (EDA). Explica los métodos y técnicas utilizados para examinar y entender el conjunto de datos de las películas.

[ETL](Documentos/ETL_movies_credits.md): Documentación sobre el proceso de extracción, transformación y carga (ETL). Describe cómo se preparó y limpió el conjunto de datos de las películas.

[API](Documentos/Main.md): Documentación sobre el modelo de recomendación implementado en el proyecto. Detalla el algoritmo usado, las características de entrada y el proceso para generar las recomendaciones.

## Requirement

[Requirements.txt](requeriments.txt)

Puede acceder a cada documento haciendo clic en los nombres de archivo correspondientes.

## AUTOR

Alejandra Aguas          
Correo alejaguasv@hotmail.com



