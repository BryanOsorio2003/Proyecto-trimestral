from flask import Flask, render_template, request, redirect, session, escape
from flask_mysqldb import MySQL
from flask.helpers import flash
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'agendame_2251848'

app.secret_key = "123"

mysql = MySQL(app)


@app.route("/inicio")
def inicio():

    cursor = mysql.connection.cursor()
    cursor.execute(f"select * from eventos WHERE usuarios={session['username']} ORDER BY fecha ASC")
    datos1 = cursor.fetchall()
    return render_template("inicio.html",lista1=datos1)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def login():
    N1 = request.form["nombre"]
    N2 = request.form["contraseña"]

    cursor = mysql.connection.cursor()
    cursor.execute(f"select idusuarios from usuarios where nombres='{N1}' and clave='{N2}'")
    lista = cursor.fetchone()

    if (lista) != None:
        session["username"] = lista[0]
        cursor = mysql.connection.cursor()
        cursor.execute(f"select * from eventos WHERE usuarios={session['username']} ORDER BY fecha ASC")
        datos1 = cursor.fetchall()
        return render_template("inicio.html",lista1=datos1)
    else:
        flash("El nombre y/o contraseña estan incorrectos"),("alert-warning")
        return render_template("index.html")
@app.route("/entrar")
def entrar():
    if "username" in session:
        cursor = mysql.connection.cursor()
        cursor.execute(f"select * from eventos where usuarios = '{session['username']}'")
        user = cursor.fetchone()
        return render_template("inicio.html",lista2=user)
    else:
        return redirect("/")
@app.route("/buscar/post", methods=["POST"])
def buscarpost():

    id = request.form["evento"]
    
    cursor = mysql.connection.cursor()
    cursor.execute(f"select fecha, hora, descripcion, lugar  from eventos where idevento = {id}")
    datos = cursor.fetchone()

    return render_template("consultar.html",lista=datos)
@app.route("/eliminar")
def eliminar():
    return render_template("consultar.html")
@app.route("/eliminar/post", methods=["POST"])
def eliminarpost():

    ide = request.form["eventoss"]

    cursor = mysql.connect.cursor()
    cursor.execute(f"DELETE FROM eventos WHERE idevento='{ide}'")
    cursor.connection.commit()

    return redirect("/eliminar")
@app.route("/cierre")
def cierre():
    return redirect("/")

@app.route("/logout", methods=["POST"]) 
def logout():
    session.pop("username", None)
    flash("Se ha cerrado sesión satisfactoriamente.")
    return redirect("/cierre")

@app.route("/nuevousuario")
def usuario():
    return render_template("nuevousuario.html")
@app.route("/nuevousuario", methods=["POST"])
def nuevoUsuario():
    nombre = request.form["Nombre"]
    apellido = request.form["Apellido"]
    edad=request.form["Edad"]
    ocupacion= request.form["Ocupacion"]
    correo = request.form["Correo Electronico"]
    contraseña = request.form["contraseña"]

    cursor = mysql.connection.cursor()
    cursor.execute("insert into usuarios(nombres,apellidos,fecnac,ocupacion,email,clave) values(%s,%s,%s,%s,%s,%s)",(nombre,apellido,edad,ocupacion,correo,contraseña))
    cursor.connection.commit()

    return render_template("index.html")


@app.route("/evento")
def evento():
    usuario = session["username"]
    return render_template("evento.html", user = usuario)

@app.route("/evento/post", methods=["POST"])
def eventopost():

    usuario = request.form["usuario"]
    descripcion= request.form["descripcion"]
    hora= request.form["hora"]
    fecha= request.form["fecha"]
    lugar= request.form["lugar"]

    cursor = mysql.connection.cursor()
    cursor.execute("insert into eventos(usuarios,fecha,hora,descripcion,lugar) values(%s,%s,%s,%s,%s)",(usuario,fecha,hora,descripcion,lugar))
    cursor.connection.commit()
    return redirect("/inicio")

@app.route("/consultar")
def consultar():
    return render_template("consultar.html")
@app.route("/consultar/post", methods=["POST"])
def consultarpost():
    cursor = mysql.connection.cursor()
    cursor.execute("select * from eventos")
    datos1 = cursor.fetchall()

    fecha= request.form["fecha"]
    hora= request.form["hora"]
    descripcion= request.form["descripcion"]
    lugar= request.form["lugar"]

    idee = request.form["eventos"]

    cursor = mysql.connection.cursor()
    cursor.execute(f"UPDATE eventos SET fecha = '{fecha}', hora = '{hora}', descripcion = '{descripcion}', lugar = '{lugar}'  WHERE idevento = '{idee}'")
    cursor.connection.commit()

    return render_template("consultar.html",lista1=datos1)
@app.route("/perfil")
def perfil():
    usuario = session["username"]
    return render_template("perfil.html", user = usuario)
@app.route("/perfil", methods=["POST"])
def perfilpost():

    documento = request.form["Documento"]
    nombre = request.form["Nombre"]
    apellido = request.form["Apellido"]
    edad=request.form["Edad"]
    ocupacion= request.form["Ocupacion"]
    correo = request.form["Correo Electronico"]
    contraseña = request.form["contraseña"]
    cursor = mysql.connection.cursor()
    cursor.execute(f"UPDATE usuarios SET nombres='{nombre}', apellidos='{apellido}', fecnac='{edad}', ocupacion='{ocupacion}', email='{correo}', clave='{contraseña}'  WHERE idusuarios='{documento}'")
    cursor.connection.commit()

    return redirect("/perfil")
@app.route("/eliminarperfil")
def eliminarperfil():
    return render_template("index.html")
@app.route("/eliminarperfil/post", methods=["POST"])
def eliminarperfilpost():

    id = request.form["evento"]

    cursor = mysql.connect.cursor()
    cursor.execute(f"DELETE FROM usuarios WHERE idusuarios = '{id}' ")
    cursor.connection.commit()

    return redirect("/eliminarperfil")
    #KLEVERMAN HPTA
if __name__ == "__main__":
    app.run(debug=True,port=5000)