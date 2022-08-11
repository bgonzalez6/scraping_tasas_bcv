import pandas as pd
import dateparser as dp

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import warnings


def get_book(url,xpath):
    # Abro una instancia del navegador y agrego configuraciones
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--verbose')
    options.add_argument('--disable-gpu')
    options.add_argument("--headless")

    # Ignore dateparser warnings regarding pytz
    warnings.filterwarnings(
        "ignore",
        message="The localize method is no longer necessary, as this time zone supports the fold attribute",
    )

    # Inicio el navegador
    ser = Service("../ChromeDriver/chromedriver.exe")
    driver = webdriver.Chrome(service=ser, options=options )

    # consulto la pagina
    driver.get(url)
    # extraigo los datos de la pagina
    file_web = driver.find_elements(By.XPATH, xpath)
    file_web = file_web[0].get_attribute('href')

    # Cierro el navegador
    driver.close()

    # abro el archivo con pandas
    return pd.ExcelFile(file_web)


def get_data_sheets(sheet):
    data = []
    fecha_valor = sheet.iloc[3][3].split(':')[1].strip()
    fecha_valor = dp.parse(fecha_valor, settings={'DATE_ORDER': 'YMD'})
    for i in range(9,45):
        if sheet.iloc[i][1].strip() == 'DEG' or sheet.iloc[i][6] == '----------------':
            pass
        else:
            bs = float(sheet.iloc[i][6])
            data.append({'Fecha_Valor': fecha_valor, 'Pais': sheet.iloc[i][2].strip(), 'Moneda': sheet.iloc[i][1].strip(), 'Tasa': bs})

    return pd.DataFrame(data)

if __name__ == '__main__':
    book = get_book('http://www.bcv.org.ve/estadisticas/otras-monedas','//*[@id="block-system-main"]/div/div[1]/div/div[1]/table/tbody/tr[1]/td[2]/span/a')
    sheets = book.sheet_names

    for sheet in sheets:
        sheet = book.parse(sheet)
        data = get_data_sheets(sheet)
        print(data)

    book.close()