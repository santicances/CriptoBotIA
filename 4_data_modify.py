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

    # Transformar los datos agregando las nuevas columnas
    df['DayOfWeek'] = df['Timestamp'].dt.dayofweek + 1  # Monday=0, Sunday=6 -> Monday=1, Sunday=7
    df['HourOfDay'] = df['Timestamp'].dt.hour           # 0-23

    # Imprimir el DataFrame resultante
    print(df)

except Exception as e:
    print("Error al conectar a la base de datos o al leer los datos: ", e)
