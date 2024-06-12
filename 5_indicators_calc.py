import pandas as pd
import pyodbc
import numpy as np

# Definir la cadena de conexión
connStr = (
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-C87BDC00\SQLSERVER2K22;'
    'DATABASE=CyBot;'
    'UID=sa;'
    'PWD=Pa$$w0rd'
)

# Funciones para calcular indicadores técnicos
def calculate_sma(close, window=20):
    return close.rolling(window=window).mean()

def calculate_ema(close, window=20):
    return close.ewm(span=window, min_periods=0, adjust=True, ignore_na=False).mean()

def calculate_rsi(close, window=14):
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(close, window_slow=26, window_fast=12):
    ema_slow = close.ewm(span=window_slow, min_periods=0, adjust=True, ignore_na=False).mean()
    ema_fast = close.ewm(span=window_fast, min_periods=0, adjust=True, ignore_na=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=9, min_periods=0, adjust=True, ignore_na=False).mean()
    macd_histogram = macd_line - signal_line
    return macd_line, signal_line, macd_histogram

def calculate_bollinger_bands(close, window=20, num_std=2):
    sma = calculate_sma(close, window=window)
    rolling_std = close.rolling(window=window).std()
    upper_band = sma + (rolling_std * num_std)
    lower_band = sma - (rolling_std * num_std)
    return upper_band, lower_band

def calculate_atr(high, low, close, window=14):
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=window).mean()
    return atr

def calculate_obv(close, volume):
    return (volume * ((close - close.shift(1)).apply(lambda x: 1 if x > 0 else -1))).cumsum()

def calculate_stoch(high, low, close, window=14):
    stoch_k = ((close - close.rolling(window=window).min()) / (close.rolling(window=window).max() - close.rolling(window=window).min())) * 100
    stoch_d = stoch_k.rolling(window=3).mean()
    return stoch_k, stoch_d

def calculate_cci(high, low, close, window=20):
    typical_price = (high + low + close) / 3
    sma_tp = calculate_sma(typical_price, window=window)
    mean_deviation = (typical_price - sma_tp).abs().rolling(window=window).mean()
    cci = (typical_price - sma_tp) / (0.015 * mean_deviation)
    return cci

try:
    with pyodbc.connect(connStr) as conn:
        print("Conexión exitosa a la base de datos")
        query = "SELECT * FROM BitcoinData"
        df = pd.read_sql(query, conn)
        df.fillna(0.0, inplace=True)
        for index, row in df.iterrows():


            # Calcula los indicadores técnicos
            df['sma'] = calculate_sma(df['Close'])
            df['ema'] = calculate_ema(df['Close'])
            df['rsi'] = calculate_rsi(df['Close'])
            macd_line, signal_line, macd_histogram = calculate_macd(df['Close'])
            df['macd_line'] = macd_line
            df['signal_line'] = signal_line
            df['macd_histogram'] = macd_histogram
            upper_band, lower_band = calculate_bollinger_bands(df['Close'])
            df['bollinger_hband'] = upper_band
            df['bollinger_lband'] = lower_band
            df['atr'] = calculate_atr(df['High'], df['Low'], df['Close'])
            df['obv'] = calculate_obv(df['Close'], df['Volume'])
            stoch_k, stoch_d = calculate_stoch(df['High'], df['Low'], df['Close'])
            df['stoch_k'] = stoch_k
            df['stoch_d'] = stoch_d
            df['cci'] = calculate_cci(df['High'], df['Low'], df['Close'])

            # Reemplaza NaN con 0.0
            df.fillna(0.0, inplace=True)

            # Itera sobre cada fila y guarda los datos en la base de datos
            for index, row in df.iterrows():
                print(row[['Close', 'sma', 'ema', 'rsi', 'macd_line', 'signal_line', 'macd_histogram', 'bollinger_hband', 'bollinger_lband', 'atr', 'obv', 'stoch_k', 'stoch_d', 'cci']])
                input("Presiona Enter para continuar...")
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE BitcoinData
                    SET sma=?, ema=?, rsi=?, macd_line=?, signal_line=?, macd_histogram=?, bollinger_hband=?, bollinger_lband=?, atr=?, obv=?, stoch_k=?, stoch_d=?, cci=?
                """, (
                    row['sma'], row['ema'], row['rsi'], row['macd_line'], row['signal_line'], row['macd_histogram'], row['bollinger_hband'], row['bollinger_lband'], row['atr'], row['obv'], row['stoch_k'], row['stoch_d'], row['cci']
                ))
                conn.commit()
                cursor.close()

        print("Datos de los indicadores técnicos guardados en la base de datos.")

except pyodbc.Error as e:
    print("Error al conectar a la base de datos o al leer los datos: ", e)
