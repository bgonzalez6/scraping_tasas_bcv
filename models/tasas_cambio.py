import db
from sqlalchemy import Column, Integer, String, Float, DateTime


class Tasas_Cambio(db.Base):
    __tablename__ = 'tasas_cambio'

    id = Column(Integer, nullable=False, primary_key=True)
    fecha = Column(DateTime)
    moneda = Column(String)
    fuente = Column(String)
    tasa = Column(Float)
    pais = Column(String)

    def __init__(self, fecha, moneda, fuente, tasa, pais):
        self.fecha = fecha
        self.moneda = moneda
        self.fuente = fuente
        self.tasa = tasa
        self.pais = pais

    def __repr__(self):
        return f'Operacion({self.fecha}, {self.moneda}, {self.fuente}, {self.tasa}, {self.pais})'

    def __str__(self):
        return str(self.fecha) + ' - ' + str(self.moneda) + ' - ' + self.fuente + ' - ' + str(self.tasa)

    def insert_data(self):
        db.session.add(self)
        db.session.commit()