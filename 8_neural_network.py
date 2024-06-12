import pandas as pd
import pyodbc
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Definir la cadena de conexión
connStr = (
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-C87BDC00\SQLSERVER2K22;'
    'DATABASE=CyBot;'
    'UID=sa;'
    'PWD=Pa$$w0rd'
)

try:
    # Conectar a la base de datos y leer los datos
    with pyodbc.connect(connStr) as conn:
        print("Conexión exitosa a la base de datos")
        query = "SELECT * FROM BitcoinData"
        df = pd.read_sql(query, conn)

        # Imprimir la tabla con los datos de "Close", "compra" y "venta"
        print(df[['compra', 'venta', 'Close']])

        # Verificar las columnas presentes en el DataFrame
        print(df.columns)

        # Dividir el conjunto de datos en características (X) y etiquetas (y)
        X = df.drop(columns=['compra', 'venta'])
        y_compra = df['compra'].values.reshape(-1, 1)  # Etiquetas para compra
        y_venta = df['venta'].values.reshape(-1, 1)    # Etiquetas para venta

        # Dividir el conjunto de datos en conjuntos de entrenamiento y prueba (70% - 30%)
        X_train_compra, X_test_compra, y_train_compra, y_test_compra = train_test_split(X, y_compra, test_size=0.3, random_state=42)
        X_train_venta, X_test_venta, y_train_venta, y_test_venta = train_test_split(X, y_venta, test_size=0.3, random_state=42)

        # Escalar los datos para mejorar el rendimiento del modelo
        scaler = StandardScaler()
        columnas_numericas = ['Open', 'High', 'Low', 'Close', 'Volume', 'sma', 'ema', 'rsi', 'macd_line', 'signal_line',
                              'macd_histogram', 'bollinger_hband', 'bollinger_lband', 'atr', 'obv', 'stoch_k', 'stoch_d', 'cci']
        
        X_train_compra_scaled = scaler.fit_transform(X_train_compra[columnas_numericas])
        X_test_compra_scaled = scaler.transform(X_test_compra[columnas_numericas])
        
        model_compra = tf.keras.Sequential([
            tf.keras.layers.Dense(100, activation='relu'),
            tf.keras.layers.Dense(50, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model_compra.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        
        # Entrenar el modelo para la señal de compra
        history_compra = model_compra.fit(X_train_compra_scaled, y_train_compra, epochs=100, batch_size=32, validation_data=(X_test_compra_scaled, y_test_compra), verbose=0)
        
        # Visualizar la pérdida durante el entrenamiento para la señal de compra
        plt.plot(history_compra.history['loss'], label='Compra - Pérdida del Entreamiento')
        plt.plot(history_compra.history['val_loss'], label='Compra - Pérdida del Entreamiento')

        # Escalar los datos para la señal de venta
        X_train_venta_scaled = scaler.fit_transform(X_train_venta[columnas_numericas])
        X_test_venta_scaled = scaler.transform(X_test_venta[columnas_numericas])

        model_venta = tf.keras.Sequential([
            tf.keras.layers.Dense(100, activation='relu'),
            tf.keras.layers.Dense(50, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model_venta.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        
        # Entrenar el modelo para la señal de venta
        history_venta = model_venta.fit(X_train_venta_scaled, y_train_venta, epochs=100, batch_size=32, validation_data=(X_test_venta_scaled, y_test_venta), verbose=0)
        
        # Visualizar la pérdida durante el entrenamiento para la señal de venta
        plt.plot(history_venta.history['loss'], label='Venta - Pérdida del Entreamiento')
        plt.plot(history_venta.history['val_loss'], label='Venta - Pérdida del Entreamiento')
        plt.xlabel('Epochs-Ciclos')
        plt.ylabel('Loss-Perdida')
        plt.title('Modelo de perdida - Compra y Venta')
        plt.legend()
        
        plt.show()

        ## Evaluar el modelo para la señal de compra y venta
        test_loss_compra, test_accuracy_compra = model_compra.evaluate(X_test_compra_scaled, y_test_compra)
        test_loss_venta, test_accuracy_venta = model_venta.evaluate(X_test_venta_scaled, y_test_venta)
        
        num_transacciones = len(X_test_compra_scaled)
        print("Número de transacciones analizadas:", num_transacciones)
        print("Precisión del modelo para la señal de compra: {:.2f}%".format(test_accuracy_compra * 100))
        print("Precisión del modelo para la señal de venta: {:.2f}%".format(test_accuracy_venta * 100))

        # Obtener las predicciones para la señal de compra y venta
        predictions_compra = model_compra.predict(X_test_compra_scaled)
        predictions_venta = model_venta.predict(X_test_venta_scaled)

        # Ajustar las predicciones a 0 o 1
        predictions_compra = (predictions_compra > 0.5).astype(int)
        predictions_venta = (predictions_venta > 0.5).astype(int)

        # Calcular la precisión de las predicciones
        accuracy_compra = np.mean(predictions_compra == y_test_compra)
        accuracy_venta = np.mean(predictions_venta == y_test_venta)

        print("Precisión de las predicciones para la señal de compra: {:.2f}%".format(accuracy_compra * 100))
        print("Precisión de las predicciones para la señal de venta: {:.2f}%".format(accuracy_venta * 100))

except pyodbc.Error as ex:
    print("Error al conectar a la base de datos:", ex)
except Exception as ex:
    print("Error:", ex)
