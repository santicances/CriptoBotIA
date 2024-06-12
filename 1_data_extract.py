import pandas as pd
import pyodbc
import ccxt

# Función para obtener datos históricos de Bitcoin desde Binance por horas
def fetch_bitcoin_data():
    binance = ccxt.binance()
    symbol = 'BTC/USDT'
    timeframe = '1h'
    since = binance.parse8601('2024-06-06T00:00:00Z')  # Cambiar la fecha inicial según sea necesario
    ohlcv = binance.fetch_ohlcv(symbol, timeframe, since)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

    # Convertir el timestamp a formato datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    return df

# Obtener datos de Bitcoin
df = fetch_bitcoin_data()
pause= input("pausa")
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

    # Crear la tabla si no existe (opcional, solo si estás seguro que no existe)
    create_table_query = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='BitcoinData' AND xtype='U')
    CREATE TABLE BitcoinData (
        id INT IDENTITY(1,1) PRIMARY KEY,
        Timestamp DATETIME NOT NULL,
        [Open] FLOAT NOT NULL,
        High FLOAT NOT NULL,
        Low FLOAT NOT NULL,
        [Close] FLOAT NOT NULL,
        Volume FLOAT NOT NULL
    );
    """
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()

    # Guardar los datos en la tabla de la base de datos
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO BitcoinData (Timestamp, [Open], High, Low, [Close], Volume) VALUES (?, ?, ?, ?, ?, ?)",
                       row['timestamp'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume'])
    conn.commit()
    cursor.close()
    print("Datos guardados en la base de datos 'CyBot'")
    
    conn.close()
except Exception as e:
    print("Error al conectar a la base de datos o al guardar los datos: ", e)
