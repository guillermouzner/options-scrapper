import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar el navegador
driver = webdriver.Chrome()  # Requiere tener ChromeDriver instalado
url = "https://cocoscap.com/Prices/Stocks"
driver.get(url)

# Encontrar el campo dni
email_field = driver.find_element(By.NAME, "Dni")
email_field.send_keys("dni")

# Encontrar el campo usuario
email_field = driver.find_element(By.NAME, "Usuario")
email_field.send_keys("usuario")

# Encontrar el campo de contraseña
password_field = driver.find_element(By.NAME, "Password")
password_field.send_keys("contraseña")

# Encontrar el botón "Iniciar sesión" y hacer clic en él para enviar el formulario
login_button = driver.find_element(By.XPATH, "//button[@id='loginButton' and contains(text(), 'INICIAR SESIÓN')]")
login_button.click()

# Navegar a la página de cotizaciones de acciones después de iniciar sesión
url = "https://cocoscap.com/Prices/Stocks"
driver.get(url)

# Encontrar la lista y hacer clic en el tercer elemento
list_element = driver.find_elements(By.XPATH, "//ul[@id='tabs-byma']/li")[2]
list_element.click()

# Esperar a que la página web cargue completamente antes de continuar
wait = WebDriverWait(driver, 30)
wait.until(EC.presence_of_element_located((By.ID, "table_stocks-opciones")))

# Encontrar la tabla y extraer los datos
table = driver.find_element(By.ID, "table_stocks-opciones")
tbody = table.find_element(By.ID, "tbody_stock")
rows = tbody.find_elements(By.TAG_NAME, "tr")

# Crear una lista para almacenar los resultados
resultados = []

# Iterar a través de las filas y extraer los datos que cumplen con los criterios
for row in rows:
    id = row.get_attribute("id")
    if id.startswith("tr_GFGC") and (id.endswith("AB") or id.endswith("A")) and not id.endswith("MA"):
        precio_element = row.find_element(By.ID, "td_" + id.replace("tr_", "") + "_LastPrice")
        precio = precio_element.text if precio_element.text != "-" else "0"
        # Convertir el precio de string a float
        precio_float = 0 if precio == "-" else float(precio.replace(",", "."))
        if id.endswith("A"):
            # Tomar los últimos 5 caracteres del id y dividir por 100
            valor = round(int(id[-6:-1]) / 100, 2)
            resultados.append({"base": valor, "call": precio_float, "put":0})
        elif id.endswith("AB"):
            # Tomar los últimos 3 caracteres del id como número entero
            valor = int(id[-5:-2])
            resultados.append({"base": valor, "call": precio_float, "put":0})

    if id.startswith("tr_GFGV") and (id.endswith("AB") or id.endswith("A")) and not id.endswith("MA"):
        precio_element = row.find_element(By.ID, "td_" + id.replace("tr_", "") + "_LastPrice")
        precio = precio_element.text if precio_element.text != "-" else "0"
        # Convertir el precio de string a float
        precio_float = 0 if precio == "-" else float(precio.replace(",", "."))
        if id.endswith("A"):
            # Tomar los últimos 5 caracteres del id y dividir por 100
            valor = round(int(id[-6:-1]) / 100, 2)
            resultados.append({"base": valor, "call": 0, "put":precio_float})
        elif id.endswith("AB"):
            # Tomar los últimos 3 caracteres del id como número entero
            valor = int(id[-5:-2])
            resultados.append({"base": valor, "call": 0, "put":precio_float})

def max_values(arr):
    base_dict = {}
    for obj in arr:
        base = obj["base"]
        if base not in base_dict:
            base_dict[base] = {"call": obj["call"], "put": obj["put"]}
        else:
            if obj["call"] > base_dict[base]["call"]:
                base_dict[base]["call"] = obj["call"]
            if obj["put"] > base_dict[base]["put"]:
                base_dict[base]["put"] = obj["put"]
    output = [{"base": base, "call": base_dict[base]["call"], "put": base_dict[base]["put"]} for base in base_dict]
    return output

output = max_values(resultados)

# Convertir la lista de resultados a formato JSON
resultados_json = json.dumps(output)
print(resultados_json)