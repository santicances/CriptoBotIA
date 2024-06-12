import pandas as pd
import pyodbc

# Definir la cadena de conexión
connStr = (
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-C87BDC00\SQLSERVER2K22;'
    'DATABASE=CyBot;'
    'UID=sa;'
    'PWD=Pa$$w0rd'
)

# Conectar a la base de datos y leer los datos
try:
    conn = pyodbc.connect(connStr)
    print("Conexión exitosa a la base de datos")

    query = "SELECT * FROM BitcoinData"
    df = pd.read_sql(query, conn)

    conn.close()

    # Imprimir el DataFrame
    print(df)
except Exception as e:
    print("Error al conectar a la base de datos o al leer los datos: ", e)
