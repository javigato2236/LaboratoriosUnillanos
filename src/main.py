from flask import Flask, render_template, url_for, redirect,request,session
from werkzeug.security import generate_password_hash, check_password_hash
import consultas
from itsdangerous import SignatureExpired




app = Flask(__name__)


app.secret_key = "abcd123"


@app.route("/")
def index():
    return render_template("PaginaPrincipal.html")

@app.route("/ventana_inicio_sesion")
def ini_sesion():
    return render_template("iniciar_sesion.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")


@app.route("/RegistrosQuimica")
def RegistrosQuimica():
    return render_template("RegistrosQuimica.html")

@app.route("/Quimica")
def Quimica():
    return render_template("quimica.html")

@app.route("/ReestablecerContraseña")
def ReestablecerContraseña():
    return render_template("ReestablecerContraseña.html")

@app.route("/registro")
def registro_usuario():
    return render_template("registro.html")










@app.route("/CambioPassword/<token>", methods = ["POST", "GET"])
def pruebaa(token):
    try:
        email = consultas.TOKEN(token)
        return render_template("CambioPassword.html", email = email )
    except: SignatureExpired
    return "pailas"


@app.route("/cambio_contraseña", methods = ["POST", "GET"])
def cambio_contra():
    if request.method == "POST":
        email = request.form["id"]
        nueva_password = request.form["nueva_password"]
        confirmar_password = request.form["confirmar_password"]
        if nueva_password == confirmar_password:
            nueva_password = generate_password_hash(request.form["nueva_password"])
            print(email)
            print(nueva_password)
            consultas.cambio_contraseña(nueva_password,email)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('ReestablecerContraseña'))
    else:
        return redirect(url_for('ReestablecerContraseña'))

    

@app.route("/reset_password", methods = ["POST", "GET"])
def reset_pss():
    if request.method == 'POST':
        email= request.form["email"]
        consultas.enviar_email(email)
        return redirect(url_for('ReestablecerContraseña'))
    else:
        redirect(url_for('ReestablecerContraseña'))
    






    


@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method =="POST" and "correo_electronico" in request.form and "password" in request.form:
        email= request.form["correo_electronico"]
        password = request.form["password"]
        registros = consultas.inicio_sesion(email)
        if registros:
            if check_password_hash(registros[2],password):
                session["login"] = True
                session["id"] = registros[0]
                return render_template("quimica.html", registros=registros)
            else:
                return redirect((url_for('ini_sesion')))
        else:
            return redirect((url_for('ini_sesion')))
    else:
        redirect((url_for('ini_sesion')))

ini_sesion

@app.route("/logout")        
def logout_sesion():
    session.clear()
    return redirect((url_for('index')))


@app.route("/registro_login", methods = ["POST", "GET"])
def registro_log():
    if request.method  == 'POST':
        email = request.form["correo_electronico"]
        password = generate_password_hash(request.form["password"])
        try:
            consultas.registrar_usuario(email,password)
        except:
            return render_template("PaginaPrincipal.html")
        finally:
            return render_template("PaginaPrincipal.html")
    return render_template("PaginaPrincipal.html")

        



if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True,port=5000)