import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Inicializa el driver
driver = webdriver.Chrome()  # O especifica el path a tu ChromeDriver si es necesario
url = "https://www.pccomponentes.com/portatiles"  # Cambia por la URL real de la página que quieres scrapear
driver.get(url)

# Espera a que la página cargue completamente
wait = WebDriverWait(driver, 10)

# Abrir el archivo CSV en modo de escritura
with open("productos_pccomponentes.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Escribir los encabezados del archivo CSV
    writer.writerow(["Nombre", "Precio", "Descuento"])

    try:
        # Espera a que los elementos estén presentes en el DOM
        productos = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@data-testid='normal-link']"))
        )
        
        # Recorre cada producto y extrae la información deseada
        for producto in productos:
            try:
                # Extrae los datos del producto
                nombre = producto.get_attribute("data-product-name")
                precio = producto.get_attribute("data-product-price")
                descuento = producto.get_attribute("data-product-total-discount") or "Sin descuento"
                
                # Imprime los resultados en la terminal
                print(f"Producto: {nombre}, Precio: {precio}, Descuento: {descuento}")
                
                # Guarda los datos en el archivo CSV
                writer.writerow([nombre, precio, descuento])

            except NoSuchElementException as e:
                print(f"Error extrayendo información de un producto: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")

    except TimeoutException:
        print("Tiempo de espera agotado. No se encontraron los productos.")

    finally:
        # Cierra el navegador tras unos segundos para ver los resultados
        time.sleep(5)
        driver.quit()
