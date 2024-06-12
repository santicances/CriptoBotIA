import pyodbc

# Definir la cadena de conexión
connStr = (
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-C87BDC00\SQLSERVER2K22;'
    'DATABASE=CyBot;'
    'UID=sa;'
    'PWD=Pa$$w0rd'
)

# Intentar conectar a la base de datos
try:
    conn = pyodbc.connect(connStr)
    print("Conexión exitosa a la base de datos")
    conn.close()
except Exception as e:
    print("Error al conectar a la base de datos: ", e)
