from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect
from flask import g, redirect
from datetime import datetime
from sqlalchemy import func

from config import DevelopmentConfig
from flask import flash
import forms
from models import db
from models import Empleados, Cliente, Pizzas

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

#--------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route("/index",methods=["GET","POST"])
def index():
    emp_form = forms.EmpForm(request.form)
    if request.method == 'POST':
        emp=Empleados(nombre=emp_form.nombre.data,
                     email=emp_form.email.data,
                     direccion=emp_form.direccion.data,
                     telefono=emp_form.telefono.data,
                     sueldo=emp_form.sueldo.data)
        db.session.add(emp)
        db.session.commit()
    return render_template("index.html", form=emp_form)

@app.route("/ABC_Completo")
def ABC_Completo():
    emp_form=forms.EmpForm(request.form)
    empleados=Empleados.query.all()
    return render_template("ABC_Completo.html", empleados=empleados)

@app.route("/eliminar",methods=["GET","POST"])
def eliminar():
    emp_form=forms.EmpForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        emp1=db.session.query(Empleados).filter(Empleados.id==id).first()
        emp_form.id.data=request.args.get('id')
        emp_form.nombre.data=emp1.nombre
        emp_form.telefono.data=emp1.telefono
        emp_form.email.data=emp1.email
        emp_form.direccion.data=emp1.direccion
        emp_form.sueldo.data=emp1.sueldo
    if request.method=='POST':
        id=emp_form.id.data
        emp=Empleados.query.get(id)
        db.session.delete(emp)
        db.session.commit()
        return redirect('ABC_Completo')
    return render_template("eliminar.html", form=emp_form)

@app.route("/modificar",methods=["GET","POST"])
def modificar():
    emp_form=forms.EmpForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        emp1=db.session.query(Empleados).filter(Empleados.id==id).first()
        emp_form.id.data=request.args.get('id')
        emp_form.nombre.data=emp1.nombre
        emp_form.telefono.data=emp1.telefono
        emp_form.email.data=emp1.email
        emp_form.direccion.data=emp1.direccion
        emp_form.sueldo.data=emp1.sueldo
    if request.method=='POST':
        id=emp_form.id.data
        emp1=db.session.query(Empleados).filter(Empleados.id==id).first()
        emp1.nombre = emp_form.nombre.data
        emp1.telefono = emp_form.telefono.data
        emp1.email = emp_form.email.data
        emp1.direccion = emp_form.direccion.data
        emp1.sueldo = emp_form.sueldo.data
        db.session.add(emp1)
        db.session.commit()
        return redirect('ABC_Completo')
    return render_template("modificar.html", form=emp_form)

@app.route("/empleados",methods=["GET","POST"])
def alum():
    nom=''
    email=''
    tel=''
    suel=''
    dir=''
    emp_form = forms.EmpForm(request.form)
    if request.method == 'POST' and emp_form.validate():
        nom=emp_form.nombre.data
        email=emp_form.email.data
        tel=emp_form.telefono.data
        suel=emp_form.sueldo.data
        dir=emp_form.direccion.data

        #Agregar mensajes a la lista de flash
        mensaje='bienvenido a la app {}'.format(nom)
        flash(mensaje)
        
    return render_template("empleados.html", form=emp_form,nom=nom,tel=tel,suel=suel,dir=dir,email=email)

# Ruta para obtener la información del cliente
@app.route('/obtener_informacion_cliente')
def obtener_informacion_cliente():
    cliente_id = request.args.get('id')
    # Consultar la base de datos para obtener el cliente por su ID
    cliente = Cliente.query.filter_by(id=cliente_id).first()
    if cliente:
        # Crear un diccionario con la información del cliente
        info_cliente = {
            'id': cliente.id,
            'nombre': cliente.nombre,
            'direccion': cliente.direccion,
            'telefono': cliente.telefono
        }
        # Devolver la información del cliente en formato JSON
        return jsonify(info_cliente)
    else:
        # Devolver un mensaje de error si el cliente no se encuentra
        return jsonify({'error': 'Cliente no encontrado'}), 404

@app.route("/pizzaIndex",methods=["GET","POST"])
def pizzaIndex():
    pizzaForm = forms.pizzasForm(request.form)
    clienteForm = forms.clienteForm(request.form)
    if request.method == 'GET':
        clientes = Cliente.query.all()
        
        return render_template("pizzas.html", formC=clienteForm, formP=pizzaForm, clientes=clientes)
    clienteForm = forms.clienteForm(request.form)
    if request.method == 'POST' and pizzaForm.validate() and clienteForm.validate():
        fecha_busqueda = request.form.get('fecha')
        cli = Cliente(nombre=clienteForm.nombre.data,
                     direccion=clienteForm.direccion.data,
                     telefono=clienteForm.telefono.data,
                     fecha=fecha_busqueda)
        db.session.add(cli)
        db.session.commit()

        subtotal = (int(pizzaForm.tamano.data) + 10)*pizzaForm.cantidad.data
        pi = Pizzas(tamano=pizzaForm.tamano.data,
                     ingredientes=pizzaForm.ingredientes.data,
                     cantidad=pizzaForm.cantidad.data,
                     subtotal=subtotal,
                     cliente_id=cli.id)
        db.session.add(pi)
        db.session.commit()
        return redirect('ABCPizza')
        


@app.route("/ABCPizza",methods=["GET","POST"])
def ABC_Pizza():
    pizzaForm=forms.pizzasForm(request.form)
    if request.method=='GET':
        pizzas=Pizzas.query.all()
    if request.method=='POST':
        #fecha_actual = str(datetime.now().date())
        #fecha_actual = fecha_actual[:10]
        #fecha_busqueda = request.form.get('fecha')
        busqueda = request.form.get('busqueda')

        #print(fecha_busqueda)

        if busqueda == 'dia_semana':
            dia_semana = request.form.get('dia_semana')
            # Convertir el día de la semana a un número (1 para lunes, 2 para martes, etc.)
            dia_semana_numero = ['domingo','lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado'].index(dia_semana) + 1
            print(dia_semana_numero)
            # Realizar la consulta utilizando el día de la semana
            pizzasHoy = db.session.query(Cliente, Pizzas).filter(
                func.DAYOFWEEK(Cliente.fecha) == dia_semana_numero,
                Cliente.id == Pizzas.cliente_id
            ).all()
            
        elif busqueda == 'mes':
            mes = request.form.get('mes')
            # Convertir el nombre del mes a su número correspondiente
            mes_numero = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'].index(mes) + 1
            # Realizar la consulta utilizando el mes del año
            pizzasHoy = db.session.query(Cliente, Pizzas).filter(
                func.extract('month', Cliente.fecha) == mes_numero,
                Cliente.id == Pizzas.cliente_id
            ).all()


        # pizzasHoy = db.session.query(Cliente, Pizzas).filter(
        #     func.substr(Cliente.fecha, 1, 10) == fecha_busqueda,
        #     Cliente.id == Pizzas.cliente_id
        # ).all()
        
        suma_subtotales = sum(pizza.subtotal for cliente, pizza in pizzasHoy)
    
        return render_template("ABCPizza.html", pizzasHoy=pizzasHoy, suma_subtotales=suma_subtotales)

    return render_template("ABCPizza.html", pizzas=pizzas)

@app.route("/modificarPizza",methods=["GET","POST"])
def modificarPizza():
    pizzaForm=forms.pizzasForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        pi=db.session.query(Pizzas).filter(Pizzas.id==id).first()
        pizzaForm.id.data=request.args.get('id')
        pizzaForm.tamano.data=pi.tamano
        pizzaForm.ingredientes.data=pi.ingredientes
        pizzaForm.cantidad.data=pi.cantidad
        

    if request.method=='POST':
        id=pizzaForm.id.data
        pi=db.session.query(Pizzas).filter(Pizzas.id==id).first()
        pi.tamano = pizzaForm.tamano.data
        pi.ingredientes = pizzaForm.ingredientes.data
        pi.cantidad = pizzaForm.cantidad.data
        subtotal = (int(pizzaForm.tamano.data) + 10)*pizzaForm.cantidad.data
        pi.subtotal = subtotal
        db.session.add(pi)
        db.session.commit()
        return redirect('ABCPizza')
    return render_template("modificarPizza.html", form=pizzaForm)

@app.route("/eliminarPizza",methods=["GET","POST"])
def eliminarPizza():
    pizzaForm=forms.pizzasForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        pi=db.session.query(Pizzas).filter(Pizzas.id==id).first()
        pizzaForm.id.data=request.args.get('id')
        pizzaForm.tamano.data=pi.tamano
        pizzaForm.ingredientes.data=pi.ingredientes
        pizzaForm.cantidad.data=pi.cantidad

    if request.method=='POST':
        id=pizzaForm.id.data
        pi=Pizzas.query.get(id)
        db.session.delete(pi)
        db.session.commit()
        return redirect('ABCPizza')
    return render_template("eliminarPizza.html", form=pizzaForm)




if __name__=="__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=5001)