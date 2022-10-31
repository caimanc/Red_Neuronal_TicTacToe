# -*- coding: utf-8 -*-
"""Red Neuronal Perceptrón Multicapa.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NP81qckzeOP9pcCMCOf_XOKjBNGSReYe

# Implementación sencilla de Red Neuronal con Sklearn

Las **redes neuronales** son modelos creados al ordenar operaciones matemáticas siguiendo una determinada estructura.

Diego Lizarazo

# Recolección de información

Para este ejercicio vamos a implementar un conjunto de información sencillo y fácil de entender denominado **Iris**.

El Iris Dataset contiene cuatro características (largo y ancho de sépalos y pétalos) de 50 muestras de tres especies de Iris (Iris setosa, Iris virginica e Iris versicolor).

Se puede encontrar facilmente por la web pero para facilidad lo vamos a insertar como una url que contiene un archivo .csv.

No obstante, utilizaremos conceptos básicos de la librería `Pandas` y `NumpY` para la manipulación de la información
"""

# Importación de la librería pandas con su acrónimo
import pandas as pd
import numpy as np

from google.colab import drive
drive.mount('/content/drive')

# Carga de datos y visualuzación del header
df = pd.read_csv("/content/drive/MyDrive/2022-3/IA2/ia2/tareas/redes neuronales/TICTAC.csv")
df.head()

# Información básica del conjunto (comprobar que no hay datos existentes y tipo de variables)
df.info()

"""# Conjuntos de entrenamiento y testeo

Es indispensable dividir nuestro conjunto de información para que la Red Neuronal pueda aprender y reproducir. Esto normalmente se realiza con una proporción de 70%-30% ó 80%-20% (entrenamiento - testeo).

La librería función `train_test_split` de `sklearn.model_selection` nos permitirá dividir y estratificarlo mediante la variable objetivo para una proporción entre estas.

Primero separamos la información, es decir, extraer las etiquetas en un subconjunto diferente, lo denominaremos **Y**.
El conjunto de atributos lo denominaremos **x**
"""

# Se selecciona solamente la columna objetivo
y = df['resultado']
y

df.value_counts('resultado')

# Se selecciona el DataFrame complejo sin la columba objetivo
X = df.drop(['resultado'], axis=1)
X

"""Realizamos la separación"""

# Llamado de la librería

from sklearn.model_selection import train_test_split

"""Convertimos los valores a numerico"""

x_auxiliar=X.replace({"o": 0, "x": 1, "b": 2})

x_auxiliar

# Conjuntos de entrenamiento y testeo para X y Y respectivamente
X_train, X_test, y_train, y_test = train_test_split(x_auxiliar, y, test_size=0.3, random_state=0, stratify=y)

X_train[:1]

# Comparamos con el DataFrame original
print(f'Cantidad de elementos en el DF original en X: {df.shape[0]}')
print(f'Cantidad de elementos de entrenamiento en X: {X_train.shape[0]}')
print(f'Cantidad de elementos de testeo en X: {X_test.shape[0]}')

"""# Modelo de Red Neuronal

Sklearn nos ofrece una utilidad para implementar una Red Neuronal tipo **Clasificador Perceptron Multicapa**.
Este modelo optimiza la función de pérdida de registro utilizando LBFGS o descenso de gradiente estocástico.

Para su implementación, la utilidad `MLPClassifier` de `sklearn.neural_network`.

Las siguientes celdas muestra su implementación en este caso con un manejo de Hiperparámetros sencillos. Si desea amplificarlos puede consultar en: [MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
"""

# Llamado de librería
from sklearn.neural_network import MLPClassifier

# Declaración de nuestra red neuronal
model_mlp = MLPClassifier(
    hidden_layer_sizes = (60,60,60), # Cantidad de capas ocultas y su respectivo tamaño
    max_iter = 1000 # Cantidad máxima de iteraciones en el modelo
)

# Entrenamiento de nuestro modelo
model_mlp.fit(X_train, y_train)

"""# Predicción

Inicialmente podríamos realizar una predicción con los valores de testeo que tenemos, para ello basta con llamar el parámetro `.predict()` y adjutarle estos valores, así:
"""

# Realizamos la predicción de nuestro conjunto de Testeo
y_predict= model_mlp.predict(X_test)
y_predict

"""Pero también podemos adjuntarle otros valores desconocidos para usar esta red. Para ello basta con agregar los valores en el mismo orden y que sea la misma cantidad total de atributos. Así:"""

# Recordemos las columnas de nuestro DataFrame
x_auxiliar.columns.tolist()

# Creamos un arreglo con nuestra información para que el modelo pueda reconocerlo
new_info = [[0,2,2,1,0,1,2,1,0]]

# Eviamos la anterior información para su predicción (método .predict[array] )
print(model_mlp.predict(new_info))

# Creamos un arreglo con nuestra información para que el modelo pueda reconocerlo
new_info = [[1,2,2,0,1,0,2,0,1]]

# Eviamos la anterior información para su predicción (método .predict[array] )
print(model_mlp.predict(new_info))

"""# Evaluación

Existen diversas formas de evaluar el modelo. En este caso evaluaremos el score, la matriz de confusión y la gráfica de pérdida

Primero, el método `.score()` nos permite obtener la exactitud media. Es inispensable enviarle el conjunto de testeo, tanto de X como de y
"""

model_mlp.score(X_test, y_test)

"""Por otra parte, la matriz de confusión es una herramienta que nos permitirá permite visualizar el desempeño de este algoritmo.

Las utilidades `classification_report` y `confusion_matrix` del paquete `sklearn.metrics` nos permitirá evaluar este modelo mediante nuestro resultado de predicciones y el conjunto de información para testeo.
"""

# Importación de la libreria
from sklearn.metrics import classification_report, confusion_matrix

# Visualizacmos la matriz de confusión
print(confusion_matrix( y_test, y_predict))

# Visualización del reporte de clasificación
print(classification_report( y_test, y_predict))

"""Para finalizar podríamos observar la gráfica de pérdida. La dea es obtener una buena curva que sea lo más cercana a 0.

Para interpretar esta y otras curvas puede visitar: [Interpreta las curvas de pérdida](https://developers.google.com/machine-learning/testing-debugging/metrics/interpretic)
"""

# Guardamos la información de la curva de pérdida que nos ofrece el modelo
loss_curve = model_mlp.loss_curve_

# Observamos el tamaño, coincide con nuestro número de iteraciones
len(loss_curve)

# Visualizamos sencillamente
import matplotlib.pyplot as plt

plt.plot(loss_curve)
plt.show()

"""No menos importante, el método `.get_params()` nos permitirá ver todos aquellos los hiperparámetros con los que funciona nuestra red neuronal."""

model_mlp.get_params()