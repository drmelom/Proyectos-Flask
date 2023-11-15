from .models.ModeloUsuario import ModeloUsuario
from flask import Flask, render_template, request, redirect, url_for,flash,jsonify
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user,logout_user,login_required,current_user
from flask_mail import Mail

from .models.ModeloLibro import ModeloLibro
from .models.ModeloCompra import ModeloCompra
from .models.entities.Usuario import Usuario
from .consts import* 
from .emails import confirmacion_compra
from .models.entities.Compra import Compra
from .models.entities.Libro import Libro



app = Flask(__name__)


db = MySQL(app)

login_manager_app = LoginManager(app)
mail = Mail()

@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.optener_por_id(db,id)


@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.tipousuario.id == 1:
            try:
                libros_vendidos=ModeloLibro.listar_libros_vendidos(db)
                data ={
                    'titulo':'Libros Vendidos',
                    'libros_vendidos': libros_vendidos
                }
            
                return render_template('index.html', data=data)
            except Exception as ex:
                return render_template('errores/error.html', mensaje=format(ex))
        else:
            try:
                compras = ModeloCompra.listar_compras_usuario(db, current_user)
                data = {
                    'titulo':'Mis compras',
                    'compras' : compras
                }
                return render_template('index.html', data=data)
            except Exception as ex:
                return render_template('errores/error.html', mensaje=format(ex))     
        
    else:
        return redirect(url_for('login'))
        


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        usuario = Usuario(
            None, request.form['usuario'], request.form['password'], None)
        usuario_loggeado = ModeloUsuario.login(db, usuario)
        if usuario_loggeado != None:
            login_user(usuario_loggeado)
            flash(MENSAJE_BIENVENIDA,'success')
            return redirect(url_for('index'))
        else:
            flash(LOGIN_CREDENCIALESINVALIDAS,'warning')
            return render_template('auth/login.html')

    else:
        return render_template('auth/login.html')


@app.route("/logaut")
def logout ():
    flash(LOGOUT,'success')
    logout_user()
    return redirect(url_for('login'))
    
@app.route('/libros')
@login_required
def listado_libros():
    try:
        libros = ModeloLibro.listar_libros(db)
        data = {
            'titulo':'Listado de libros',
            'libros': libros
        }
        return render_template('listado_libros.html', data=data)
    except Exception as ex:
        return render_template('errores/error.html', mensaje=format(ex))

@app.route('/comprarLibro',methods = ['POST'])
@login_required
def comprar_libro():
    data_request = request.get_json()
    data = {}
    try:
        #libro=Libro(data_request['isbn'],None,None,None,None)
        libro=ModeloLibro.leer_libro(db,data_request['isbn'])
        compra = Compra( None,libro,current_user)
        data['exito']= ModeloCompra.registar_compra(db,compra)
        confirmacion_compra(app,mail,current_user,libro)
    except Exception as ex:
        data['mensaje']=format(ex)
        data['exito']= False    
    return jsonify(data)


def Page_not_found(error):
    return render_template('errores/404.html'), 404
def Page_not_autorizada(error):
    return redirect(url_for('login'))


def inicializar_app(config):
    app.config.from_object(config)
    mail.init_app(app)
    app.register_error_handler(404, Page_not_found)
    app.register_error_handler(401, Page_not_autorizada)
    return app
