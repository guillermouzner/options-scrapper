from pyhomebroker import HomeBroker
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import pandas as pd

import datosPersonales

hb = HomeBroker(int(datosPersonales.broker))

hb.auth.login(dni=datosPersonales.dni, user=datosPersonales.user, password=datosPersonales.password, raise_exception=True)


# Get intraday information from platform
GD30 = hb.history.get_intraday_history('GD30')
GD30['date'] = pd.to_datetime(GD30['date'])
GD30['date'] = GD30['date'].dt.strftime('%H:%M:%S')
GD30 = GD30[['date', 'close', 'volume']]

AL30 = hb.history.get_intraday_history('AL30')
AL30['date'] = pd.to_datetime(AL30['date'])
AL30['date'] = AL30['date'].dt.strftime('%H:%M:%S')
AL30 = AL30[['date', 'close', 'volume']]

# Convertir la columna 'date' a datetime y establecerla como índice para AL30
AL30['date'] = pd.to_datetime(AL30['date'])
AL30.set_index('date', inplace=True)

# Convertir la columna 'date' a datetime y establecerla como índice para GD30
GD30['date'] = pd.to_datetime(GD30['date'])
GD30.set_index('date', inplace=True)

# Remuestrear los datos de AL30 a intervalos de 3 minutos
resampled_AL30 = AL30.resample('3T').agg({
    'close': 'last',
    'volume': 'sum'
}).dropna()

resampled_AL30['percentage_diff'] = resampled_AL30['close'].pct_change().mul(100).round(2)

# Remuestrear los datos de GD30 a intervalos de 3 minutos
resampled_GD30 = GD30.resample('3T').agg({
    'close': 'last',
    'volume': 'sum'
}).dropna()

resampled_GD30['percentage_diff'] = resampled_GD30['close'].pct_change().mul(100).round(2)

# Alinear ambos DataFrames por índice y calcular el ratio
aligned_GD30, aligned_AL30 = resampled_GD30.align(resampled_AL30, join='inner')
ratio = aligned_GD30['close'] / aligned_AL30['close']

# Convertir las horas de AL30 a un formato de cadena
time_strings_AL30 = resampled_AL30.index.strftime('%H:%M')

# Convertir las horas de GD30 a un formato de cadena
time_strings_GD30 = resampled_GD30.index.strftime('%H:%M')

# Convertir las horas del ratio a un formato de cadena
time_strings_ratio = ratio.index.strftime('%H:%M')

# Función para formatear las etiquetas del eje y con puntos como separadores de miles
def thousands_with_dots(x, pos):
    return '{:,.0f}'.format(x).replace(",", ".")

# Creando gráficos para AL30, GD30 y el ratio
fig, axs = plt.subplots(5, sharex=True, figsize=(10, 12), gridspec_kw={'height_ratios': [2, 1, 2, 1, 2]})
fig.subplots_adjust(hspace=0.5)

# Graficando el precio de cierre de AL30 en axs[0]
axs[0].plot(time_strings_AL30, resampled_AL30['close'], color='blue', marker='o', linestyle='-', linewidth=1.5)
axs[0].set_ylabel("Precio de Cierre AL30")
axs[0].set_title("Gráfico de TradingView AL30 (Datos Remuestreados)")
axs[0].grid(True, which='both', linestyle='--', linewidth=0.5)

# Graficando el volumen de AL30 en axs[1]
axs[1].bar(time_strings_AL30, resampled_AL30['volume'], color='gray')
axs[1].yaxis.set_major_formatter(FuncFormatter(thousands_with_dots))
axs[1].set_ylabel("Volumen AL30")
axs[1].grid(True, which='both', linestyle='--', linewidth=0.5)

# Graficando el precio de cierre de GD30 en axs[2]
axs[2].plot(time_strings_GD30, resampled_GD30['close'], color='green', marker='o', linestyle='-', linewidth=1.5)
axs[2].set_ylabel("Precio de Cierre GD30")
axs[2].set_title("Gráfico de TradingView GD30 (Datos Remuestreados)")
axs[2].grid(True, which='both', linestyle='--', linewidth=0.5)

# Graficando el volumen de GD30 en axs[3]
axs[3].bar(time_strings_GD30, resampled_GD30['volume'], color='gray')
axs[3].yaxis.set_major_formatter(FuncFormatter(thousands_with_dots))
axs[3].set_ylabel("Volumen GD30")
axs[3].grid(True, which='both', linestyle='--', linewidth=0.5)

# Graficando el ratio en axs[4]
axs[4].plot(time_strings_ratio, ratio, color='red', marker='o', linestyle='-', linewidth=1.5)
axs[4].set_ylabel("Ratio GD30/AL30")
axs[4].set_title("Relación entre precios de cierre GD30 y AL30")
axs[4].grid(True, which='both', linestyle='--', linewidth=0.5)

# Rotando las etiquetas del eje x para mejor visualización
plt.xticks(rotation=90)

# Mostrando el gráfico
plt.tight_layout()
plt.show()
