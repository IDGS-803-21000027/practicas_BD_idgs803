from flask_sqlalchemy import SQLAlchemy

import datetime

db=SQLAlchemy()

class Empleados(db.Model):
    __tablename__='empleado'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    telefono=db.Column(db.String(20))
    direccion=db.Column(db.String(50))
    sueldo=db.Column(db.Double)
    email=db.Column(db.String(50))
    create_date=db.Column(db.DateTime,default=datetime.datetime.now)