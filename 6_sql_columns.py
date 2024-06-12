
import pyodbc


# Definir la cadena de conexión
connStr = (
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-C87BDC00\SQLSERVER2K22;'
    'DATABASE=CyBot;'
    'UID=sa;'
    'PWD=Pa$$w0rd'
)



# Conectarse a la base de datos



with pyodbc.connect(connStr) as conn:
    # Obtener el cursor
    cursor = conn.cursor()

    # Ejecutar la consulta para obtener los nombres de las columnas
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'BitcoinData'")

    # Obtener los resultados
    columns = cursor.fetchall()

    # Imprimir los nombres de las columnas
    for column in columns:
        print(column[0])
