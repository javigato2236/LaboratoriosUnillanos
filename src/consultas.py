from bd import iniciar_conexion
import smtplib
from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from main import app





def registrar_usuario(email,password):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO ingreso_quimica(correo_electronico, password) VALUES (%s,%s)",(email,password)) 
        conexion.commit()
        conexion.close()

def inicio_sesion(email):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT *FROM ingreso_quimica WHERE correo_electronico=%s",(email))
        registros = cursor.fetchone()
        return registros
        
def restablecer_contraseña(email):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT correo_electronico FROM ingreso_quimica WHERE correo_electronico=%s",(email))
        registros = cursor.fetchone()
        return registros
       
       
    

def enviar_email(email):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    confir_url = url_for('pruebaa',token =confirm_serializer.dumps(email,salt='email-confirmacion-salt'), _external =True)
    remitente = "javieraugustosanchezmartinez@gmail.com"
    destinatario = email
    mensaje = f"holaaaa\n{confir_url}"
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "recupere su contraseña aqui"
    email.set_content(mensaje)
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(remitente,"ifjuomcczvhwupmf")
    server.sendmail(remitente,destinatario,email.as_string())
    
def TOKEN(token):
    token_expired = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    email = token_expired.loads(token, salt='email-confirmacion-salt',max_age=7000)  
    return email

    
        
    
def cambio_contraseña(nueva_password2,email):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE ingreso_quimica SET password=%s WHERE correo_electronico=%s",(nueva_password2,email))
        conexion.commit()
        conexion.close()

                
       




    


  
    
    



       
            

   