from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship


db=SQLAlchemy()

class Empleados(db.Model):
    __tablename__='empleado'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    telefono=db.Column(db.String(20))
    direccion=db.Column(db.String(50))
    sueldo=db.Column(db.Double)
    email=db.Column(db.String(50))
    create_date=db.Column(db.DateTime,default=datetime.now)

class Pizzas(db.Model):
    __tablename__='pizzas'
    id=db.Column(db.Integer, primary_key=True)
    tamano=db.Column(db.String(20))
    ingredientes=db.Column(db.String(100))
    cantidad=db.Column(db.Integer)
    subtotal=db.Column(db.Float)
        # Agregar la clave externa para la relación con Cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    cliente = relationship("Cliente", back_populates="pizzas")
    
class Cliente(db.Model):
    __tablename__='clientes'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    direccion=db.Column(db.String(100))
    telefono=db.Column(db.String(20))
    fecha = db.Column(db.DateTime)  # Agregar el campo de fecha

    # Establecer la relación uno a muchos con Pizzas
    pizzas = relationship("Pizzas", back_populates="cliente")