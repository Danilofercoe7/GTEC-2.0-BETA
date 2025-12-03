import mysql.connector
from mysql.connector import Error

try:
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",     
        database="Banco"
    )
    if con.is_connected():
        print("Conectado ao MySQL! Versão:", con.get_server_info())  
        cursor = con.cursor()
        cursor.execute("SELECT DATABASE();")
        print("Banco atual:", cursor.fetchone())
except Error as e:
    print("Erro ao conectar:", e)
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'con' in locals() and con.is_connected():
        con.close()
        print("Conexão encerrada")
