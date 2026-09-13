from conexion.conexion import obtener_conexion

try:
    conexion = obtener_conexion()

    if conexion.is_connected():
        print("CONEXIÓN EXITOSA A MYSQL")
        print("Base de datos: ferreteria")

    conexion.close()

except Exception as e:
    print("ERROR DE CONEXIÓN:")
    print(e)
    