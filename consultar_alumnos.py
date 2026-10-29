import mysql.connector

# 1. Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="TU_PASSWORD",
    database="MiUniversidad"
)

# 2. Cursor
cursor = conexion.cursor()

# 3. Consulta SQL (Cambiamos id por matricula)
sql = "SELECT matricula, nombre, edad, email FROM Alumnos"
cursor.execute(sql)

# 4. Obtener resultados
resultados = cursor.fetchall()

# 5. Imprimir en pantalla (Cambiamos ID por Matrícula)
print("\n--- LISTA DE ALUMNOS DE MIUNIVERSIDAD ---\n")
for fila in resultados:
    print(f"Matrícula: {fila[0]} | Nombre: {fila[1]} | Edad: {fila[2]} | Email: {fila[3]}")

# 6. Cerrar conexión
conexion.close()
print("\n🔒 Conexión cerrada.")