# 🌞 Predicción de Radiación Solar en Tunja mediante Dinámica de Sistemas

Sistema de simulación y predicción de la radiación solar en la ciudad de **Tunja, Boyacá**, utilizando **Dinámica de Sistemas**, análisis estadístico y modelos de regresión implementados en **Python**.

---

## 📌 Descripción del proyecto

Este proyecto tiene como propósito analizar el comportamiento histórico de la radiación solar en Tunja a partir de datos meteorológicos reales obtenidos desde una estación climática, para posteriormente construir un modelo capaz de:

* Simular escenarios futuros
* Predecir niveles de radiación solar
* Evaluar relaciones entre variables atmosféricas
* Apoyar decisiones en energías renovables

El modelo considera la interacción entre:

* ☁️ Nubosidad
* 💧 Humedad relativa
* 🌧️ Pluviosidad
* ☀️ Horas de brillo solar
* 🌞 Radiación solar

---

## 🎯 Objetivos

### Objetivo general

Desarrollar un modelo computacional que permita predecir la radiación solar utilizando dinámica de sistemas y datos meteorológicos históricos.

### Objetivos específicos

* Analizar datos meteorológicos históricos.
* Identificar relaciones causales entre variables.
* Implementar un modelo matemático predictivo.
* Simular comportamiento futuro de la radiación.
* Validar la precisión del modelo.

---

## 🧠 Metodología aplicada

El proyecto se desarrolló en cuatro etapas principales:

### 1. Recolección y depuración de datos

Se procesaron archivos `.xlsx` con información meteorológica histórica para generar un dataset limpio en formato `.csv`.

### 2. Modelado causal

Se construyó un diagrama de relaciones entre variables:

* Mayor nubosidad → menor radiación
* Mayor brillo solar → mayor radiación
* Mayor pluviosidad → mayor humedad relativa

### 3. Regresión lineal múltiple

Se implementaron modelos matemáticos para estimar el comportamiento de las variables:

Y = β₀ + β₁X₁ + β₂X₂ + ... + βₙXₙ

### 4. Simulación

Se generaron predicciones día a día usando:

* Números pseudoaleatorios
* Distribuciones normales
* Modelos de regresión

---

## 🏗️ Arquitectura del sistema

El proyecto sigue una estructura modular:

```bash
project/
│── data/                # Datos meteorológicos
│── models/              # Modelos matemáticos
│── utils/               # Generación de números aleatorios
│── presenters/          # Patrón MVP
│── views/               # Interfaz gráfica
│── main.py              # Punto de entrada
```

---

## ⚙️ Tecnologías utilizadas

* 🐍 Python
* 📊 Pandas
* 🔢 NumPy
* 📈 Matplotlib
* 🤖 Scikit-learn

---

## 📉 Variables del modelo

| Variable         | Tipo      | Influencia          |
| ---------------- | --------- | ------------------- |
| Radiación solar  | Principal | Variable a predecir |
| Brillo solar     | Estado    | Positiva            |
| Nubosidad        | Estado    | Negativa            |
| Humedad relativa | Flujo     | Indirecta           |
| Precipitación    | Flujo     | Indirecta           |

---

## 📊 Resultados obtenidos

El sistema logró:

* Simular radiación solar diaria
* Comparar datos reales vs simulados
* Obtener errores entre:

```bash
3% hasta 20%
```

Dependiendo de la cantidad de datos y condiciones iniciales.

---

## 🖥️ Ejecución del proyecto

Clonar el repositorio:

```bash
git clone https://github.com/tuusuario/prediccion-radiacion-solar.git
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar:

```bash
python main.py
```

---

## 📷 Ejemplo de salida

El sistema genera:

* Gráficas comparativas
* Fórmulas del modelo
* Error porcentual
* Simulación por días

Ejemplo:

```bash
Promedio real:      456.96 cal/cm²
Promedio simulado:  371.14 cal/cm²
Error:              18.78%
```

---

## 🌱 Aplicaciones del proyecto

Este sistema puede utilizarse en:

* Instalación de paneles solares
* Planeación energética
* Agricultura de precisión
* Estudios climáticos
* Investigación académica

---

## 👨‍💻 Autores

* David Santiago Lotero Rodríguez
* Luis Eduardo Hernández Rincón
* Gabriel Esteban Infante Acosta
* Edison Ferney Gutiérrez Buitrago
* Harold Ricardo Alvarado Leandro

---

## 📚 Referencias

El proyecto se fundamenta en:

* Dinámica de Sistemas
* Regresión lineal múltiple
* Simulación estadística
* Modelado climático

---

## 📄 Licencia

Proyecto desarrollado con fines académicos en la:

**Universidad Pedagógica y Tecnológica de Colombia – UPTC**


