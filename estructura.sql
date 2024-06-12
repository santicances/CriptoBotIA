use [CyBot]
go
CREATE TABLE BitcoinData (
    Timestamp DATETIME NOT NULL,
    [Open] FLOAT NOT NULL,
    High FLOAT NOT NULL,
    Low FLOAT NOT NULL,
    [Close] FLOAT NOT NULL,
    Volume FLOAT NOT NULL
);

use [CyBot]
go
DELETE FROM BitcoinData;


IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'BitcoinData' AND COLUMN_NAME IN ('compra', 'venta')) BEGIN ALTER TABLE BitcoinData ADD compra INT DEFAULT 0; ALTER TABLE BitcoinData ADD venta INT DEFAULT 0; END;

-- Agregar columnas para los indicadores técnicos
ALTER TABLE BitcoinData
ADD sma FLOAT,
    ema FLOAT,
    rsi FLOAT,
    macd_line FLOAT,
    signal_line FLOAT,
    macd_histogram FLOAT,
    bollinger_hband FLOAT,
    bollinger_lband FLOAT,
    atr FLOAT,
    obv FLOAT,
    stoch_k FLOAT,
    stoch_d FLOAT,
    cci FLOAT;

	select * from [dbo].[BitcoinData]