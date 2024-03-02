from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask import g, redirect

from config import DevelopmentConfig
from flask import flash
import forms
from models import db
from models import Empleados

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

if __name__=="__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()