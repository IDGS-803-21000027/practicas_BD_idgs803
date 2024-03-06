from wtforms import Form
from wtforms import StringField,SelectField,RadioField,IntegerField, EmailField, BooleanField, SelectMultipleField
from wtforms import validators
from wtforms.validators import DataRequired

class EmpForm(Form):
    id=IntegerField(id)

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
    
class clienteForm(Form):
    id=IntegerField(id)

    nombre=StringField('Nombre', [
    validators.DataRequired(message='El campo es requerido'),
    validators.length(min=4, max=10,message='Ingresa nombre valido')
    ])
    direccion=StringField('Direccion', [
    validators.DataRequired(message='El campo es requerido'),
    validators.length(min=4, max=10,message='Ingresa direccion valida')
    ])
    telefono=StringField('Telefono', [
    validators.DataRequired(message='El campo es requerido'),
    validators.length(min=4, max=10,message='Ingresa telefono valido')
    ])

class pizzasForm(Form):
    id=IntegerField(id)

    # Define choices for RadioField
    CHOICES_RADIO = [('40', 'Chica'), ('80', 'Mediana'),('120','Grande')]
    tamano = RadioField('Tamaños', choices=CHOICES_RADIO)

    # Define choices for CheckboxField
    # CHOICES_CHECKBOX = [('10', 'Jamon'), ('10', 'Piña'), ('10', 'Champiñones')]
    # ingredientes = CheckboxField('Ingredientes', choices=CHOICES_CHECKBOX)
    INGREDIENT_CHOICES = [
        ('jamon', 'Jamon'),
        ('pina', 'Piña'),
        ('champinones', 'Champiñones')
    ]
    ingredientes = SelectField('Ingredientes', choices=INGREDIENT_CHOICES, validators=[DataRequired()], coerce=str)

    cantidad=IntegerField('Cantidad', [
        validators.number_range(min=1,message='Valor no valido')
    ])
