# 👁️ Reconocimiento de Patrones e Imágenes en Python (Desde Cero)

Bienvenido a este repositorio. Este proyecto es una implementación práctica de los fundamentos de la **Visión Artificial**, demostrando cómo una computadora puede "leer" y reconocer números escritos utilizando procesamiento matemático puro, sin depender de modelos preentrenados de Inteligencia Artificial como TensorFlow o PyTorch.

---

## 🎯 Motivación del Proyecto

**¿Por qué este proyecto?** 
Elegí desarrollar este sistema porque actualmente estoy cursando la materia de **Visión Artificial**. Este proyecto me permitió sacar la teoría de los libros e implementarla en código real. En lugar de usar una librería que haga todo el trabajo pesado como una "caja negra", este proyecto me obligó a entender las matemáticas y la lógica fundamental: desde cómo se leen los canales de color (RGBA) hasta cómo se binariza una matriz de píxeles.

El código está basado en la excelente serie de tutoriales *"Basic Image Recognition"* de Harrison Kinsley (PythonProgramming.net), unificando sus 5 etapas en un solo script robusto y optimizado.

---

## ⚙️ ¿Cómo funciona? (El Algoritmo Paso a Paso)


El proyecto no usa redes neuronales, sino un enfoque lógico de **comparación de matrices**. Se divide en 4 fases principales:

### 1. Binarización (Thresholding)
Las imágenes del mundo real tienen sombras, difuminados y canales de opacidad. La función `threshold()` lee el brillo promedio (RGB) de la imagen y establece un umbral. Todo píxel más claro que el promedio se convierte en **blanco puro** y todo lo más oscuro en **negro puro**. Esto estandariza los datos.

### 2. Creación del "Cerebro" (Base de Datos)
La función `createExamples()` toma un set de imágenes de entrenamiento (números del 0 al 9 con diferentes tipografías). Las binariza y convierte sus matrices matemáticas bidimensionales en largas cadenas de texto (Strings). Toda esta información se guarda en un archivo de texto plano llamado `numArEx.txt`.

### 3. Reconocimiento (Testeo)
La función `whatNumIsThis()` toma una imagen nueva de prueba, la binariza y la convierte en texto. Luego, el algoritmo realiza un escaneo **píxel por píxel** (texto contra texto) comparando la imagen nueva contra la base de datos. Cada vez que un píxel coincide exactamente en la misma posición, el número correspondiente recibe un "voto".

### 4. Visualización
Utilizando la librería `Matplotlib`, el programa cuenta los votos totales. La barra más alta en la gráfica representa el número que la computadora cree haber identificado basándose en la máxima similitud de patrones.

---

## 🚀 Cómo ejecutar este proyecto

### Requisitos previos
Asegúrate de tener instaladas las siguientes librerías de Python:
* `numpy` (Para el manejo de matrices matemáticas)
* `matplotlib` (Para la visualización de datos)
* `Pillow` / `PIL` (Para la manipulación de imágenes y canales RGBA)

### Instrucciones
1. Clona este repositorio.
2. Asegúrate de tener una carpeta llamada `imagenes/numbers/` que contenga tus imágenes de entrenamiento (ej. `0.1.png`, `0.2.png`, etc.).
3. Ejecuta `main.py`.
4. El programa generará automáticamente el archivo `numArEx.txt`.
5. Revisa la gráfica generada para ver los resultados de la predicción de la imagen de prueba.

---

## 💼 Viabilidad Comercial y Aplicaciones Reales

Aunque el script exacto de este repositorio es netamente educativo (ya que el método de píxel exacto es vulnerable a rotaciones o cambios de escala), **la tecnología y teoría demostradas aquí son altamente monetizables.** Este proyecto es la base cruda del **OCR (Reconocimiento Óptico de Caracteres)**. Escalar estos principios básicos integrando librerías más avanzadas (como OpenCV) permite crear software comercial muy lucrativo en la industria actual, como por ejemplo:

* **Automatización de peajes:** Sistemas de lectura automática de placas vehiculares en estacionamientos.
* **Fintech y Contabilidad:** Software de digitalización corporativa que extrae automáticamente números de cuenta y montos de facturas o recibos escaneados.
* **Control de Calidad (Industria 4.0):** Cámaras de visión artificial en líneas de ensamblaje que verifican la correcta impresión de códigos, etiquetas o formas en los productos físicos.
