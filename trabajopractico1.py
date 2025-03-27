# -*- coding: utf-8 -*-
"""TrabajoPractico1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VNfCbORT1FozdlVGR4Us-6wPwTcF1CSE

# Trabajo de: Sandra Blázquez Arriero.

Este conjunto de datos nos da diversas caracteristicas sobre la calidad del vino.
Las carácteristicas que nos dan son las siguientes:


*   Fixed_acidity: Los ácidos del vino, pero que no se van.
*   Volatile_acidity: Los ácidos del vino que pueden evaporarse.
*   Citric_acid: El ácido cítrico.
*   Residual_sugar: La cantidad de azúcar que tiene el vino.
*   Chlorides: Es la cantidad de sal que tiene el vino.
*   Free_sulfur_dioxide: Dióxido de azufle libre, que no está unido a otros componentes del vino.
*   Total_sulfur_dioxide: Dióxido de azufre pero total.
*   Density: La densidad del vino.
*   PH: El PH del vino.
*   Sulphates: Los sulfatos del vino.
*   Alcohol: El alcohol que contiene el vino de manera concentrada.

Lo primero que hacemos es importar los datos sobre los cuales vamos a trabajar:
"""

pip install ucimlrepo

"""Aqui lo que hacemos es, separar los datos en caracteristicas (features) y etiquetas (targets) y lo imprimimos para poder verlos antes de trabajar con ellos."""

from ucimlrepo import fetch_ucirepo
wine_quality = fetch_ucirepo(id=186)
X = wine_quality.data.features
y = wine_quality.data.targets
print(wine_quality.metadata)
print(wine_quality.variables)

"""##**KNN FOR CLASSIFICATIONS**

Importamos todo lo que nos va a hacer falta para poder realizar un KNN por clasificación:
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import metrics

"""Vamosa a imprimir las diversas columnas que tenemos tanto de X como de y, para poder ver toda la información que tenemos."""

print(X.head())

print(y.head())

"""Y luego diversa información de cada una de esas clasificaciones que hemos realizado al inicio de la practica, en las cuales hemos separado en X (features) y en y (targets)."""

print(X.info())

print(y.value_counts())

"""Vamos a seleccionar las caracterisiticas con las cuales vamos a trabajar en este caso y con las que vamos a ir realizando los siguientes métodos."""

features_selected = ['alcohol', 'volatile_acidity', 'sulphates', 'citric_acid']
df = X[features_selected].copy()
df['quality'] = y

"""Ahora, los datos que tenemos tanto en X como en y los vamos a dividir para poder entrenarlos, con el 0,2 del test_size, estamos indicando que solo el 20% de los datos se usa para prueba, mientras que el 80% restante se usará para entrenamiento."""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""Y además, vamos a escalar los datos, es decir, normalizar las características"""

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""Y convertimos y_train e y_test a arrays de numpy"""

y_train = y_train.to_numpy().reshape(-1)
y_test = y_test.to_numpy().ravel()

"""Con esta siguiente parte, lo que estamos realizando es una busqueda de los mejores parametros para este modelo usando los datos de entrenamiento que hemos creado con anterioridad.
Y para finalizar, creamos una gráfica para poder ver de una manera más visual esos datos que hemos elegido.
"""

neighbors_range = range(1, 31)
weights_options = ['uniform', 'distance']
metric_options = ['euclidean', 'manhattan', 'minkowski']

best_score = 0
best_params = {}


for weight in weights_options:
  for metric_option in metric_options:
    total_scores = []
    for neighbors in neighbors_range:

            knn = KNeighborsClassifier(n_neighbors=neighbors, weights=weight, metric=metric_option)
            scores = cross_val_score(knn, X_train, y_train, cv=4)
            mean_score = scores.mean()
            total_scores.append(mean_score)
            if mean_score > best_score:
                best_score = mean_score
                best_params = {'n_neighbors': neighbors, 'weights': weight, 'metric': metric_option}
    plt.plot(range(1,len(total_scores)+1), total_scores, marker='o', label=f"{weight}_{metric_option}")

plt.ylabel('Acc')
plt.legend()
plt.show()
print("Best parameters:", best_params)
print("Best cross-validation score:", best_score)

"""Ahora entrenamos el código y evaluamos el modelo con los mejores parámetros que hemos visto con anterioridad para poder calcular la precisión (acc)."""

n_neighbors = best_params["n_neighbors"]
weights = best_params["weights"]
metric = best_params["metric"]

knn = KNeighborsClassifier(n_neighbors= n_neighbors, weights=weights, metric = metric)

knn.fit(X = X_train, y = y_train)
y_pred = knn.predict(X = X_test)

acc_knn = accuracy_score(y_test, y_pred)
print ('Acc knn clasif', acc_knn)

"""Calculamos el resto de parámetros que son la precision, el recall y el f1 score, cada uno de estos nos indica lo siguiente:


*   Precision: mide la proporción de predicciones positivas correctas sobre el total de predicciones positivas.
*   Recall: es la sensibilidad, mide la proporción de casos positivos correctamente identificados por el modelo.
*   F1 Score: es la media armónica entre la precisión y el recall


"""

precision = metrics.precision_score(y_test, y_pred, average='weighted', zero_division=0)
print(f"Precision: {precision}")


recall = metrics.recall_score(y_test, y_pred, average='weighted')
print(f"Recall: {recall}")


f1_score = metrics.f1_score(y_test, y_pred, average='weighted')
print(f"F1 Score: {f1_score}")

"""Ahora vamos a crear la matriz de confusión para poder ver una comparación de los valores de las predicciones del modelo con los datos que son reales, para así poder ver cuantas están bien predichas y cuales no."""

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=wine_quality.target_names)
disp.plot()
plt.grid(False)
plt.show()

"""##**KNN FOR REGRESSION**

Importamos todo lo que nos va a hacer falta para poder realizar un KNN por regresión:
"""

import seaborn as sns

from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

"""Con el siguiente comando vamos a conseguir realizar la matriz de correlación para poder ver la relación entre las distintas variables."""

sns.set()
correlation_matrix = X.corr()

"""Ahora vamos a crear pequeños subplots (es decir, como unas mini gráficas) para poder ver los datos que tenemos en X relacionados con cada una de las caracteristicas que tiene.
Este en un principio era más grande, pero al hablarlo vimos que era mejor centrarse solo en los graficos centrales entonces saqué la grafica unicamente de esos que eran más relevantes.
"""

sns.set()
fig, axes = plt.subplots(4, 3, figsize=(12, 12))
sns.histplot(X['fixed_acidity'], ax=axes[0, 0])
sns.histplot(X['volatile_acidity'], ax=axes[0, 1])
sns.histplot(X['citric_acid'], ax=axes[0, 2])
sns.histplot(X['residual_sugar'], ax=axes[1, 0])
sns.histplot(X['chlorides'], ax=axes[1, 1])
sns.histplot(X['free_sulfur_dioxide'], ax=axes[1, 2])
sns.histplot(X['total_sulfur_dioxide'], ax=axes[2, 0])
sns.histplot(X['density'], ax=axes[2, 1])
sns.histplot(X['pH'], ax=axes[2, 2])
sns.histplot(X['sulphates'], ax=axes[3, 0])
sns.histplot(X['alcohol'], ax=axes[3, 1])
plt.tight_layout()
plt.show()

"""Ahora indicamos las caracteristicas que vamos a seleccionar para hacer el estudio de las caracteristicas del vino, que vamos a utilizar en este y el resto de métodos."""

features_selected = ['alcohol', 'volatile_acidity', 'sulphates', 'citric_acid']
df = X[features_selected].copy()
df['quality'] = y

"""Ahora, los datos que tenemos tanto en X como en y los vamos a dividir para poder entrenarlos, con el 0,2 del test_size, estamos indicando que solo el 20% de los datos se usa para prueba, mientras que el 80% restante se usará para entrenamiento."""

X_train, X_test, y_train, y_test = train_test_split(df[features_selected], df['quality'], test_size=0.2, random_state=42)
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X, y['quality'], test_size=0.2, random_state=42)

"""Con esto vamos a escalar los datos (o normalizarlos) a través de un StardardScaler(), para poder tener todos los datos iguales y poder utilizarlos juntos."""

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_train_reg_scaled = scaler.fit_transform(X_train_reg)
X_test_reg_scaled = scaler.transform(X_test_reg)

"""Este código implementa la búsqueda de hiperparámetros para nuestro modelo de KNN for Regresion utilizando validación cruzada para series temporales, con esto se evalúa el rendimiento del modelo con diferentes combinaciones de hiperparámetros y unicamente realizamos una selección de los mejores."""

from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)



neighbors_range = range(1, 31)
weights_options = ['uniform', 'distance']
metric_options = ['euclidean', 'manhattan', 'minkowski']

best_score = float('-inf')
best_params = {}


for weight in weights_options:
  for metric_option in metric_options:
    total_scores = []
    for neighbors in neighbors_range:
      knn_regressor = KNeighborsRegressor(n_neighbors=neighbors, weights=weight, metric=metric_option)


      scores = cross_val_score(knn_regressor, X_train, y_train, cv=tscv, scoring='neg_mean_absolute_error')

      mean_score = scores.mean()
      total_scores.append(mean_score)
      if mean_score > best_score:
          best_score = mean_score
          best_params = {'n_neighbors': neighbors, 'weights': weight, 'metric': metric_option}

    plt.plot(range(1,len(total_scores)+1), total_scores, marker='o', label=f"{weight}_{metric_option}")

plt.ylabel('MAE')
plt.legend()
plt.show()

print("Best parameters:", best_params)
print("Best average negative MAE:", best_score)

"""Ahora vamos a entrenar el modelo de regresión utilizando los mejores hiperparámetros encontrados previamente (codigo anterior) y luego realiza predicciones sobre los datos de prueba."""

knn_regressor = KNeighborsRegressor(n_neighbors=best_params["n_neighbors"], weights=best_params["weights"], metric=best_params["metric"])
knn_regressor.fit(X_train_reg_scaled, y_train_reg)
y_pred_knn_reg = knn_regressor.predict(X_test_reg_scaled)

"""Y calculamos los diversos valores: MAE, MSE y R² los cuales significan lo siguiente:


*   MAE: Mide el error promedio absoluto entre los valores reales y las predicciones.
*   MSE: Mide el error cuadrático medio (eleva al cuadrado los errores antes de promediarlos).
*   R²: Mide qué tan bien el modelo explica la variabilidad de los datos reales.


"""

mae_knn = mean_absolute_error(y_test_reg, y_pred_knn_reg)
mse_knn = mean_squared_error(y_test_reg, y_pred_knn_reg)
r2_knn = r2_score(y_test_reg, y_pred_knn_reg)
print('MAE', mae_knn)
print('MSE', mse_knn)
print('R2', r2_knn)

"""Con este código vamos a generar una gráfica de comparación entre los valores reales (y_test) y las predicciones (y_pred) de nuestro modelo."""

xx = np.arange(y_test.shape[0])
plt.plot(xx, y_test.values, c='r', label='Real')
plt.plot(xx, y_pred, c='g', label='Predicción')
plt.axis('tight')
plt.legend()
plt.title("KNeighborsRegressor (k = %i, weights = '%s')" % (best_params["n_neighbors"], best_params["weights"]))
plt.show()

"""##**NAIVE BAYES**

Importamos todo lo necesario para poder trabajar con el modelo de Naive Bayes.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_auc_score, roc_curve, log_loss, ConfusionMatrixDisplay
from ucimlrepo import fetch_ucirepo

"""Aqui tenemos una gráfica de la calidad del vino"""

sns.set(style="whitegrid")
ax = sns.countplot(x='quality', data=df)
ax.set_title('Distribución de Clases')
ax.set_xlabel('Calidad del Vino')
ax.set_ylabel('Frecuencia')
plt.show()

"""Este código genera un heatmap con las correlaciones entre las variables que tenemos. Con esto lo que hacemos es:

* Identificar relaciones entre variables.

* Detectar multicolinealidad en modelos de Machine Learning.

* Seleccionar variables importantes eliminando redundancias.
"""

sns.heatmap(df.corr(), square=True, annot=True)
plt.show()

"""Ahora, los datos que tenemos tanto en X como en y los vamos a dividir para poder entrenarlos, con el 0,2 del test_size, estamos indicando que solo el 20% de los datos se usa para prueba, mientras que el 80% restante se usará para entrenamiento."""

X_train, X_test, y_train, y_test = train_test_split(df[features_selected], df['quality'], test_size=0.2, random_state=42)

"""Entrena un modelo de clasificación con el modo Gaussiano utilizando los anteriormente creados datos de entrenamiento y pruebas: X_train, y_train.


"""

gnb = GaussianNB()
gnb.fit(X_train, y_train)

"""Ahora hacemos predicciones sobre el conjunto de prueba X_test con el modelo Gaussiano."""

y_pred = gnb.predict(X_test)
y_pred_proba = gnb.predict_proba(X_test)

"""Calculamos los siguientes valores para nuestro modelo de Naive Bayes Gaussiano, accuray score, precision, recall, f1 score que significan lo siguiente:

* Accuracy_score: es una métrica de evaluación utilizada para medir qué tan bien predice un modelo comparando las etiquetas reales (y_test) con las predichas (y_pred).
*   Precision: mide la proporción de predicciones positivas correctas sobre el total de predicciones positivas.
*   Recall: es la sensibilidad, mide la proporción de casos positivos correctamente identificados por el modelo.
*   F1 Score: es la media armónica entre la precisión y el recall
"""

from sklearn import metrics

acc_naive = metrics.accuracy_score(y_test, y_pred)
print(f"Acc Naive: {acc_naive}")


precision = metrics.precision_score(y_test, y_pred, average='weighted', zero_division=0)
print(f"Precision: {precision}")


recall = metrics.recall_score(y_test, y_pred, average='weighted')
print(f"Recall: {recall}")


f1_score = metrics.f1_score(y_test, y_pred, average='weighted')
print(f"F1 Score: {f1_score}")

"""Ahora vamos a crear la matriz de confusión, esta vez para Naive Bayes, para poder ver una comparación de los valores de las predicciones del modelo con los datos que son reales, para así poder ver cuantas están bien predichas y cuales no."""

from sklearn.metrics import ConfusionMatrixDisplay

cm = metrics.confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=gnb.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.show()


print(metrics.classification_report(y_test, y_pred, zero_division=0))

"""Calculamos la probabilidad de pertenencia a cada clase para cada muestra en X_test y posteriormente guardamos una matriz de probabilidades, donde cada fila representa una muestra y cada columna representa la probabilidad de pertenecer a una clase específica.


"""

y_pred_proba = gnb.predict_proba(X_test)
y_pred_proba

"""Calculamos el ROC_AUC que es una métrica utilizada para evaluar modelos de clasificación binaria o multiclase."""

ROC_AUC = metrics.roc_auc_score(y_test, y_pred_proba, average='macro', multi_class='ovo')

print('ROC AUC : {:.4f}'.format(ROC_AUC))

"""##**SVM**

Importamos todo lo necesario para poder utilizar el modelo de SVM
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

"""Ahora, los datos que tenemos tanto en X como en y los vamos a dividir para poder entrenarlos, con el 0,2 del test_size, estamos indicando que solo el 20% de los datos se usa para prueba, mientras que el 80% restante se usará para entrenamiento."""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X, y['quality'], test_size=0.2, random_state=42)

"""Con esto vamos a escalar los datos (o normalizarlos) a través de un StardardScaler(), para poder tener todos los datos iguales y poder utilizarlos juntos."""

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_train_reg_scaled = scaler.fit_transform(X_train_reg)
X_test_reg_scaled = scaler.transform(X_test_reg)

"""Creamos un modelo de clasificación SVM con un kernel lineal, en el cual usa los siguientes parametros:
* C=1.0: controla la penalización por errores en la clasificación.
* probability=True: nos permite poder calcular probabilidades con predict_proba().

Por último entrenamos el modelo.
"""

model = SVC(kernel='linear', C=1.0, probability=True)
model.fit(X_train_scaled, y_train)

"""Toma los datos de prueba y usa el modelo para predecir sus etiquetas de clase."""

y_pred = model.predict(X_test_scaled)

"""Calculamos el accuracy_score para el modelo de SVM, el cual es: una métrica de evaluación utilizada para medir qué tan bien predice un modelo comparando las etiquetas reales (y_test) con las predichas (y_pred)."""

acc_svm = accuracy_score(y_test, y_pred)
print(f'Accuracy del modelo SVM: {acc_svm:.4f}')

"""Este código calcula y visualiza el AUC ROC para el modelo, además de mostrar las curvas ROC para cada clase en un problema multiclase."""

from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.preprocessing import label_binarize


n_classes = len(np.unique(y_test))
y_test_bin = label_binarize(y_test, classes=np.unique(y_test))
y_pred_proba = model.predict_proba(X_test_scaled)


ROC_AUC = roc_auc_score(y_test_bin, y_pred_proba, multi_class="ovo", average="macro")
print("ROC AUC: {:.4f}".format(ROC_AUC))


plt.figure(figsize=(8,6))
for i in range(n_classes):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_pred_proba[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'Clase {np.unique(y_test)[i]} (AUC = {roc_auc:.2f})')

plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Curvas ROC para cada clase')
plt.legend()
plt.show()

"""Lo primero que hemos aqui es entrenar el modelo de SVM para regresión y calculamos los valores de predicción de y con respecto a los valores de X.

Por último, calculamos los diversos valores: MAE, MSE y R² los cuales significan lo siguiente:


*   MAE: Mide el error promedio absoluto entre los valores reales y las predicciones.
*   MSE: Mide el error cuadrático medio (eleva al cuadrado los errores antes de promediarlos).
*   R²: Mide qué tan bien el modelo explica la variabilidad de los datos reales.
"""

from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


svm_reg = SVR(kernel='rbf')
svm_reg.fit(X_train_reg_scaled, y_train_reg)


y_pred_svm_reg = svm_reg.predict(X_test_reg_scaled)


mae_svm = mean_absolute_error(y_test_reg, y_pred_svm_reg)
mse_svm = mean_squared_error(y_test_reg, y_pred_svm_reg)
r2_svm = r2_score(y_test_reg, y_pred_svm_reg)

print(f'MAE SVM Regresión: {mae_svm:.4f}')
print(f'MSE SVM Regresión: {mse_svm:.4f}')
print(f'R² SVM Regresión: {r2_svm:.4f}')

"""##**ARBOLES**

Importamos todo lo necesario para poder trabajar con este modelo.
"""

from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

"""Ahora indicamos las caracteristicas que vamos a seleccionar para hacer el estudio de las caracteristicas del vino, que vamos a utilizar en este y el resto de métodos."""

features_selected = ['alcohol', 'volatile_acidity', 'sulphates', 'citric_acid']
X = wine_quality.data.features[features_selected].values
y = wine_quality.data.targets.astype(int).values

"""Ahora, los datos que tenemos tanto en X como en y los vamos a dividir para poder entrenarlos, con el 0,2 del test_size, estamos indicando que solo el 20% de los datos se usa para prueba, mientras que el 80% restante se usará para entrenamiento."""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X, y, test_size=0.2, random_state=42)

"""Con esto vamos a escalar los datos (o normalizarlos) a través de un StardardScaler(), para poder tener todos los datos iguales y poder utilizarlos juntos."""

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""Ahora vamos a crear y entrenar un árbol de decisión utilizando un límite de profundidad de 5 para evitar el sobreajuste.

El modelo es entrenado con los datos de entrenamiento escalados y sus etiquetas correspondientes.
"""

tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree.fit(X_train_scaled, y_train)

"""Toma los datos de prueba y usa el modelo para predecir sus etiquetas de clase."""

y_pred_tree = tree.predict(X_test_scaled)

"""Calculamos el valor de accuray score:

* Accuracy_score: es una métrica de evaluación utilizada para medir qué tan bien predice un modelo comparando las etiquetas reales (y_test) con las predichas (y_pred).
"""

acc_tree = accuracy_score(y_test, y_pred_tree)
print(f'Accuracy del Árbol de Decisión: {acc_tree:.4f}')

"""Generamos el grafo de arbol con las características"""

plt.figure()
plot_tree(tree, feature_names=features_selected, filled=True)
plt.title("Árbol de Decisión para la Calidad del Vino")
plt.show()

"""Ahora generamos una visualización de la frontera de decisión utilizando PCA. Esto lo usamos para reducir sus dimensiones para que se pueda visualizar en un gráfico 2D, ya que, al tener 4 características en X nos daba un error."""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def visualize_classifier_2d(model, X, y, ax=None, cmap='rainbow'):
    """Visualización de la frontera de decisión del clasificador en 2D usando PCA"""


    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    ax = ax or plt.gca()

    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=y, s=30, cmap=cmap)

    legend = ax.legend(*scatter.legend_elements(), title="Clases")
    ax.add_artist(legend)

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    xx, yy = np.meshgrid(np.linspace(*xlim, num=200), np.linspace(*ylim, num=200))
    Z = model.predict(pca.inverse_transform(np.c_[xx.ravel(), yy.ravel()])).reshape(xx.shape)

    ax.contourf(xx, yy, Z, alpha=0.3, cmap=cmap)
    ax.set(xlim=xlim, ylim=ylim)

plt.figure(figsize=(8, 6))
visualize_classifier_2d(tree, X_train_scaled, y_train)
plt.show()

"""Lo primero que hemos aqui es entrenar el modelo de Arbol de Regresión para regresión y calculamos los valores de predicción de y con respecto a los valores de X.

Por último, calculamos los diversos valores: MAE, MSE y R² los cuales significan lo siguiente:


*   MAE: Mide el error promedio absoluto entre los valores reales y las predicciones.
*   MSE: Mide el error cuadrático medio (eleva al cuadrado los errores antes de promediarlos).
*   R²: Mide qué tan bien el modelo explica la variabilidad de los datos reales.
"""

from sklearn.tree import DecisionTreeRegressor

tree_reg = DecisionTreeRegressor(max_depth=5, random_state=42)
tree_reg.fit(X_train_reg_scaled, y_train_reg)

y_pred_tree_reg = tree_reg.predict(X_test_reg_scaled)

mae_tree = mean_absolute_error(y_test_reg, y_pred_tree_reg)
mse_tree = mean_squared_error(y_test_reg, y_pred_tree_reg)
r2_tree = r2_score(y_test_reg, y_pred_tree_reg)

print(f'MAE Árbol de Decisión Regresión: {mae_tree:.4f}')
print(f'MSE Árbol de Decisión Regresión: {mse_tree:.4f}')
print(f'R² Árbol de Decisión Regresión: {r2_tree:.4f}')

"""##**RANDOM** **FOREST**

Importamos lo necesario para trabajar con este modelo.
"""

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, BaggingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error, r2_score, confusion_matrix

"""Extraemos de nuevo la variable quality, ya que sino el resto del código me daba error."""

y = wine_quality.data.targets
y_class = y['quality'].astype(int)

"""Ahora, los datos que tenemos tanto en X como en y los vamos a dividir para poder entrenarlos, con el 0,2 del test_size, estamos indicando que solo el 20% de los datos se usa para prueba, mientras que el 80% restante se usará para entrenamiento."""

X_train, X_test, y_train_class, y_test_class = train_test_split(X, y, test_size=0.2, random_state=42)
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X, y['quality'], test_size=0.2, random_state=42)

"""Con esto vamos a escalar los datos (o normalizarlos) a través de un StardardScaler(), para poder tener todos los datos iguales y poder utilizarlos juntos."""

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_train_reg_scaled = scaler.fit_transform(X_train_reg)
X_test_reg_scaled = scaler.transform(X_test_reg)

"""Entrenamos le modelo para la clasificación y luego calculamos el accuracy_score: la métrica de evaluación utilizada para medir qué tan bien predice un modelo comparando las etiquetas reales (y_test) con las predichas (y_pred)."""

rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train_scaled, y_train_class)

y_pred_rf = rf_clf.predict(X_test_scaled)

acc_rf = accuracy_score(y_test_class, y_pred_rf)
print(f'Accuracy de Random Forest Clasificación: {acc_rf:.4f}')

"""Ahora mostramos la importancia de cada característica en la clasificación realizada por Random Forest mediante un gráfico de barras."""

feature_importance = pd.Series(rf_clf.feature_importances_, index=features_selected).sort_values(ascending=False)

plt.figure(figsize=(8, 5))
sns.barplot(x=feature_importance, y=feature_importance.index, palette='rainbow')
plt.xlabel("Importancia de la Característica")
plt.ylabel("Características")
plt.title("Importancia de Características en Random Forest Clasificación")
plt.show()

"""Realizamos la matriz de confusión para poder ver una comparación de los valores de las predicciones del modelo con los datos que son reales, para así poder ver cuantas están bien predichas y cuales no."""

mat = confusion_matrix(y_test_class, y_pred_rf)

plt.figure(figsize=(6,6))
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False, cmap="Blues")
plt.xlabel('Etiqueta Real')
plt.ylabel('Etiqueta Predicha')
plt.title("Matriz de Confusión - Random Forest Clasificación")
plt.show()

"""Lo primero que hemos aqui es entrenar el modelo de Random Forest para regresión y calculamos los valores de predicción de y con respecto a los valores de X.

Por último, calculamos los diversos valores: MAE, MSE y R² los cuales significan lo siguiente:


*   MAE: Mide el error promedio absoluto entre los valores reales y las predicciones.
*   MSE: Mide el error cuadrático medio (eleva al cuadrado los errores antes de promediarlos).
*   R²: Mide qué tan bien el modelo explica la variabilidad de los datos reales.
"""

rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg.fit(X_train_reg_scaled, y_train_reg)

y_pred_rf_reg = rf_reg.predict(X_test_reg_scaled)

mae_rf = mean_absolute_error(y_test_reg, y_pred_rf_reg)
mse_rf = mean_squared_error(y_test_reg, y_pred_rf_reg)
r2_rf = r2_score(y_test_reg, y_pred_rf_reg)

print(f'MAE Random Forest Regresión: {mae_rf:.4f}')
print(f'MSE Random Forest Regresión: {mse_rf:.4f}')
print(f'R² Random Forest Regresión: {r2_rf:.4f}')

"""Realizamos una grafica para la comparación entre datos reales con las predicciones."""

plt.figure(figsize=(8,6))
plt.scatter(y_test_reg, y_pred_rf_reg, alpha=0.5, color='red')
plt.plot([min(y_test_reg), max(y_test_reg)], [min(y_test_reg), max(y_test_reg)], '--', color='black')
plt.xlabel("Valores Reales")
plt.ylabel("Predicciones")
plt.title("Random Forest Regresión - Predicciones vs Valores Reales")
plt.show()

"""## **COMPARACIONES**

Despues de haber probado todos los modelos que hay tanto para clasificación como para regresión y haber calculado el accuracy score para los de clasificación y el MAE, MSE y R² para los de regresión, podemos poner todos en conjunto (pero divididos por clases) para poder ver cual es la mejor opción de cada uno.
"""

print("\n--- Comparación de Modelos de Clasificación ---")
print("\n--- KNN CLASIFICATION ---")
print(f"KNN accuracy score:  {acc_knn:.4f}")
print("\n--- NAIVE BAYES CLASIFICATION ---")
print(f"Naive Bayes accuracy score: {acc_naive:.4f}")
print("\n--- SVM CLASIFICATION ---")
print(f"SVM accuracy score: {acc_svm:.4f}")
print("\n--- TREE CLASIFICATION ---")
print(f"Tree accuracy score: {acc_tree:.4f}")
print("\n--- RANDOM FOREST CLASIFICATION ---")
print(f"Random Forest accuracy score: {acc_rf:.4f}")

print("\n--- Comparación de Modelos de Regresión ---")
print("\n--- KNN REGRESION ---")
print(f"KNN Regresión MAE:  {mae_knn:.4f}")
print(f"KNN Regresión MSE:  {mse_knn:.4f}")
print(f"KNN Regresión :  {r2_knn:.4f}")
print("\n--- SVM REGRESION ---")
print(f"SVM Regresión MAE:  {mae_svm:.4f}")
print(f"SVM Regresión MSE:  {mse_svm:.4f}")
print(f"SVM Regresión :  {r2_svm:.4f}")
print("\n--- TREE REGRESION ---")
print(f"Tree Regresión MAE:  {mae_tree:.4f}")
print(f"Tree Regresión MSE:  {mse_tree:.4f}")
print(f"Tree Regresión :  {r2_tree:.4f}")
print("\n--- RANDOM FOREST REGRESION ---")
print(f"Random Forest Regresión MAE: {mae_rf:.4f}")
print(f"Random Forest Regresión MSE: {mse_rf:.4f}")
print(f"Random Forest Regresión R²: {r2_rf:.4f}")

"""##**CONCLUSIÓN**

Como hemos podido ver en la comparación, tenemos los siguientes resultados como los mejores:

**En la clasificación:**
Tenemos el Random Forest como el mejor ya que su nivel de accuracy (exactitud) es el mayor de todos los demás modelos de clasificación.
"""

print("\n--- RANDOM FOREST CLASIFICATION ---")
print(f"Random Forest accuracy score: {acc_rf:.4f}")

"""**En la regresión:** En regresión tenia duda entre KNN y Random Forest, pero estuve investigando y le daban más valor a MAE y a MSE, las cuales son menores en KNN que en Random Forest, por lo tanto, el mejor modelo en el grupo de regresión sería KNN for Regresion."""

print("\n--- KNN REGRESION ---")
print(f"KNN Regresión MAE:  {mae_knn:.4f}")
print(f"KNN Regresión MSE:  {mse_knn:.4f}")
print(f"KNN Regresión :  {r2_knn:.4f}")

"""Y ahora para poder ver, de ambos, cual es el mejor, vamos a realizar una comparación entre el mejor valor de clasificación (Random Forest) y el de regresión (KNN for Regresion).

Hacemos un redondeo para convertir los datos decimales para tener los que haría una persona lo evaluamos con MSE y MAE.
"""

from sklearn.metrics import mean_absolute_error, mean_squared_error

y_pred_knn_rounded = np.round(y_pred_knn_reg).astype(int)

mae_rf = mean_absolute_error(y_test_class, y_pred_rf)
mse_rf = mean_squared_error(y_test_class, y_pred_rf)

mae_knn = mean_absolute_error(y_test_reg, y_pred_knn_rounded)
mse_knn = mean_squared_error(y_test_reg, y_pred_knn_rounded)


print(f"Random Forest - MAE: {mae_rf:.4f}, MSE: {mse_rf:.4f}")
print(f"KNN Regresión - MAE: {mae_knn:.4f}, MSE: {mse_knn:.4f}")

"""Ahora realizamos una grafica con los datos para poder ver la comparación de una manera las visual."""

metrics_df = pd.DataFrame({
    "Comparativa": ["Random Forest", "KNN Regresión"],
    "MAE": [mae_rf, mae_knn],
    "MSE": [mse_rf, mse_knn],
})

plt.figure(figsize=(12, 5))
metrics_df.set_index("Comparativa").plot(kind="bar" , figsize=(12, 6))
plt.ylabel("Valor")
plt.legend(title="Métrica")
plt.show()

"""Despues de ver los valores y la gráfica comparativa podemos apreciar como el valor de MAE y MSE es menor en KNN for Regresion que en Random Forest, por lo tanto, el mejor modelo de todos los utilizados, incluidos los de clasficación y los de regresión es el **KNN for Regresion**."""