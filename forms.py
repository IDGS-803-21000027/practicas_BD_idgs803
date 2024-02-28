from wtforms import Form
from wtforms import StringField,SelectField,RadioField,IntegerField, EmailField
from wtforms import validators

class EmpForm(Form):
    nombre=StringField('nombre', [
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4, max=10,message='ingresa nombre valido')
    ])
    telefono=StringField('telefono', [
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4, max=10,message='ingresa numero valido')
    ])
    direccion=StringField('direccion', [
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4, max=50,message='ingresa direccion valida')
    ])
    sueldo=IntegerField('sueldo', [
        validators.number_range(min=1,message='Valor no valido')
    ])
    email=EmailField('email', [
        #validators.email(message='Ingrese un correo valido')
    ])
    