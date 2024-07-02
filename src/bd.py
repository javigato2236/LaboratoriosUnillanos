import pymysql





def iniciar_conexion():
    return pymysql.connect( host='localhost', user= 'root', passwd='monus2236', db='unillanos' )
   