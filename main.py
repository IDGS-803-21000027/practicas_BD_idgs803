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


@app.route("/pizzaIndex",methods=["GET","POST"])
def pizzaIndex():
    pizzaForm = forms.pizzasForm(request.form)
    clienteForm = forms.clienteForm(request.form)
    if request.method == 'POST' and pizzaForm.validate() and clienteForm.validate():
        cli = Cliente(nombre=clienteForm.nombre.data,
                     direccion=clienteForm.direccion.data,
                     telefono=clienteForm.telefono.data)
        db.session.add(cli)

        subtotal = (int(pizzaForm.tamano.data) + 10)*pizzaForm.cantidad.data
        cli = Pizzas(tamano=pizzaForm.tamano.data,
                     ingredientes=pizzaForm.ingredientes.data,
                     cantidad=pizzaForm.cantidad.data,
                     subtotal=subtotal)
        db.session.add(cli)
        db.session.commit()
        return redirect('ABCPizza')
    return render_template("pizzas.html", formC=clienteForm, formP=pizzaForm)


@app.route("/ABCPizza",methods=["GET","POST"])
def ABC_Pizza():
    pizzaForm=forms.pizzasForm(request.form)
    if request.method=='GET':
        pizzas=Pizzas.query.all()
    if request.method=='POST':
        # Obtenemos la fecha actual y la convertimos en una cadena
        fecha_actual = str(datetime.now().date())

        
        # Limitamos la cadena a los primeros 10 caracteres
        fecha_actual = fecha_actual[:10]
        print(fecha_actual)
        
        # Consultamos la base de datos para recuperar los registros de la tabla Cliente
        pizzasHoy = Cliente.query.filter(func.substr(Cliente.fecha, 1, 10) == fecha_actual).all()

        # Convertimos los resultados a un formato JSON para pasarlos al template
        # pizzasHoy_json = jsonify([pizza.serialize() for pizza in pizzasHoy])
    
        return render_template("ABCPizza.html", pizzasHoy=pizzasHoy)

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