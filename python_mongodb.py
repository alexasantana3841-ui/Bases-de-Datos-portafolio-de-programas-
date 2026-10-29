"""Programa 4: vínculo de Python a MongoDB (MongoDB Atlas con pymongo)."""
import os
import pandas as pd
from pymongo import MongoClient

# La cadena de conexión NO se escribe en el código: se lee de una variable de entorno.
# PowerShell:  $env:MONGO_URI = "mongodb+srv://usuario:password@cluster0.2jtvffc.mongodb.net/"
URI = os.environ.get("MONGO_URI", "mongodb+srv://USUARIO:PASSWORD@cluster0.2jtvffc.mongodb.net/")

try:
    cliente = MongoClient(URI, serverSelectionTimeoutMS=5000)
    cliente.admin.command("ping")
    print("Conexión exitosa a MongoDB Atlas")

    coleccion = cliente["BancoMundialdb"]["indicadores"]

    # 1. Contar documentos
    print("Documentos en la colección:", coleccion.count_documents({}))

    # 2. Consultar (find): indicador general PMR de México en 2023
    filtro = {"REF_AREA": "MEX", "INDICATOR": "PTY_MR_PMR", "TIME_PERIOD": 2023}
    for doc in coleccion.find(filtro, {"_id": 0, "REF_AREA_LABEL": 1, "TIME_PERIOD": 1, "OBS_VALUE": 1}):
        print("Consulta:", doc)

    # 3. Insertar un documento de prueba
    prueba = {"REF_AREA": "TST", "INDICATOR": "PRUEBA", "TIME_PERIOD": 2024, "OBS_VALUE": 1.5}
    id_nuevo = coleccion.insert_one(prueba).inserted_id
    print("Insertado:", id_nuevo)

    # 4. Actualizar el documento de prueba
    r = coleccion.update_one({"_id": id_nuevo}, {"$set": {"OBS_VALUE": 2.0}})
    print("Documentos modificados:", r.modified_count)

    # 5. Eliminar el documento de prueba
    r = coleccion.delete_one({"_id": id_nuevo})
    print("Documentos eliminados:", r.deleted_count)

    # 6. Agregación: PMR promedio por país en 2023 (los 5 más regulados)
    pipeline = [
        {"$match": {"INDICATOR": "PTY_MR_PMR", "TIME_PERIOD": 2023, "OBS_VALUE": {"$ne": None}}},
        {"$group": {"_id": "$REF_AREA_LABEL", "pmr": {"$avg": "$OBS_VALUE"}}},
        {"$sort": {"pmr": -1}},
        {"$limit": 5},
    ]
    print("Top 5 países con mayor PMR en 2023:")
    for fila in coleccion.aggregate(pipeline):
        print(f"  {fila['_id']}: {fila['pmr']:.2f}")

    # 7. Exportar la colección a CSV para el programa de limpieza
    df = pd.DataFrame(list(coleccion.find({}, {"_id": 0})))
    df.to_csv("BancoMundialdb_indicadores.csv", index=False)
    print("Exportado a BancoMundialdb_indicadores.csv:", df.shape)

except Exception as e:
    print("Ocurrió un error:", e)

finally:
    if "cliente" in locals():
        cliente.close()
        print("Conexión cerrada")
