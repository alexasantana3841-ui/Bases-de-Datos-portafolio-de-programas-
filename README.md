# Portafolio de programas: Bases de datos

Alexa Estefania Santana Tapia

## Programas

| # | Programa | Archivos |
|---|----------|----------|
| 1 | Web scraping (Pinterest + MongoDB) | `scraping_pinterest.py` |
| 2 | Limpieza de base de datos | `limpieza.py`, `mongodbalexasanatana.ipynb` (celda 1: Excel a JSON) |
| 3 | Python a MySQL | `consultar_alumnos.py`, `insertar_alumno.py`, `modificar_alumno.py` |
| 4 | Python a MongoDB | `python_mongodb.py`, `mongodbalexasanatana.ipynb` |
| 5 | Analisis de datos con ML | `analisis_ml.py`, `mongodbalexasanatana.ipynb` (regresiones) |

## Datos
- `BancoMundialdb_indicadores.csv`: indicadores exportados de MongoDB Atlas.
- `indicadores_limpio.csv`: resultado de `limpieza.py`.
- `Conversaciones_chatbot.Salud_mental.xlsx` y `salud_mental_limpio.json`: datos del chatbot de salud mental.
- `Reporte_Santana_Tapia_Alexa.pdf`: reporte de la actividad de MongoDB Compass y Python.

## Cómo ejecutar
1. `pip install -r requirements.txt`
2. Credenciales: las contraseñas no están en el código.
   - MongoDB: `$env:MONGO_URI = "mongodb+srv://usuario:password@cluster0.2jtvffc.mongodb.net/"`
   - MySQL: escribir la contraseña local en los scripts de alumnos antes de ejecutar.
3. Orden sugerido: `limpieza.py`, luego `analisis_ml.py`.
