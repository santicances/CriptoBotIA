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

try:
    with pyodbc.connect(connStr) as conn:
        print("Conexión exitosa a la base de datos")
        query = "SELECT * FROM BitcoinData"
        df = pd.read_sql(query, conn)

        # Calcular compra y venta basado en el criterio proporcionado
        df['compra'] = 0
        df['venta'] = 0
        high_low_diff = (df['High'] - df['Low']) / df['High'].shift(1)
        df.loc[high_low_diff > 0.01, 'compra'] = 1
        df.loc[high_low_diff <= 0.01, 'venta'] = 1

        # Imprimir el DataFrame resultante con las columnas "Close", "compra" y "venta"
        print(df[['Close', 'compra', 'venta']])

        # Guardar los datos actualizados en la base de datos
        cursor = conn.cursor()
        for index, row in df.iterrows():
            cursor.execute("UPDATE BitcoinData SET compra=?, venta=? WHERE Timestamp=?", row['compra'], row['venta'], row['Timestamp'])
        conn.commit()
        cursor.close()
        print("Datos actualizados en la base de datos.")

except pyodbc.Error as e:
    print("Error al conectar a la base de datos o al leer los datos: ", e)
