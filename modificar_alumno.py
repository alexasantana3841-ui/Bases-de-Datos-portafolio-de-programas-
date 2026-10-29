import mysql.connector

# Datos a modificar
nuevo_nombre = "Alexa Santana (Modificado)"
matricula_alumno = 4

try:
    # 1. Conexión a tu base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="TU_PASSWORD",
        database="MiUniversidad"
    )

    # 2. Cursor
    cursor = conexion.cursor()

    # 3. Consulta UPDATE
    sql = "UPDATE Alumnos SET nombre = %s WHERE matricula = %s"

    # 4. Valores
    valores = (nuevo_nombre, matricula_alumno)

    # 5. Ejecutar
    cursor.execute(sql, valores)

    # 6. Guardar cambios
    conexion.commit()

    # 7. Verificar filas afectadas
    print(f"Se actualizaron {cursor.rowcount} registro(s).")

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print("Conexión cerrada")