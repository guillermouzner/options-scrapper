from pyhomebroker import HomeBroker
import pandas as pd

import datosPersonales

hb = HomeBroker(int(datosPersonales.broker))

hb.auth.login(dni=datosPersonales.dni, user=datosPersonales.user, password=datosPersonales.password, raise_exception=True)


file_path = "D:/datos/mi_archivo.xlsx"
writer = pd.ExcelWriter(file_path, engine='openpyxl')

# Get intraday information from platform
GD30 = hb.history.get_intraday_history('GD30')
GD30['date'] = pd.to_datetime(GD30['date'])
GD30['date'] = GD30['date'].dt.strftime('%H:%M:%S')
GD30 = GD30[['date', 'open', 'close', 'volume']]

AL30 = hb.history.get_intraday_history('AL30')
AL30['date'] = pd.to_datetime(AL30['date'])
AL30['date'] = AL30['date'].dt.strftime('%H:%M:%S')
AL30 = AL30[['date', 'open', 'close', 'volume']]

data = {
  "Date GD30": GD30['date'],
  "GD30": GD30['close'],
  "volume GD30": GD30['volume'],

  "Date AL30": AL30['date'],
  "AL30": AL30['close'],
  "volume AL30": AL30['volume'],
}


df = pd.DataFrame(data)


df.to_excel(writer, sheet_name="Hoja1", startrow=0, startcol=0, index=False)
writer.save()
