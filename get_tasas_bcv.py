# Utilities
import pandas as pd

# Models
from models.tasas_cambio import Tasas_Cambio

# Custom Functions
from utils.tasas_bcv import get_book, get_data_sheets

# Conexion a base de datos
import db

# fecha maxima a partir de la cual buscar los datos
query_fecha_max = """SELECT	MAX(fecha)
FROM public.tasas_cambio
WHERE fuente = 'BCV' """

fecha_max = pd.read_sql(query_fecha_max, db.engine)
fecha_max = pd.to_datetime(fecha_max['max'][0]).date()

# Paginas para colsultar
HOME_URL = 'http://www.bcv.org.ve/estadisticas/otras-monedas'

data = pd.DataFrame()
for i in range(1,11):
    XPATH_TO_FILE = '//*[@id="block-system-main"]/div/div[1]/div/div[1]/table/tbody/tr[{}]/td[2]/span/a'.format(i)
    book = get_book(HOME_URL,XPATH_TO_FILE)
    sheets = book.sheet_names

    for sheet in sheets:
        sheet = book.parse(sheet)
        for row in get_data_sheets(sheet).itertuples():
            if row.Fecha_Valor.date() > fecha_max:
                tasa = Tasas_Cambio(
                    row.Fecha_Valor,
                    row.Moneda,
                    'BCV',
                    row.Tasa,
                    row.Pais
                )
                tasa.insert_data()
            else:
                break;
            
    book.close()