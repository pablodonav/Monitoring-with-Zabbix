#!/usr/bin/python
# requisito_servidor_10.py

# Pablo Donate, Adnana Dragut y Diego Hernandez
# Requisito de Servidor 10
# Designación: Caída del Cliente.
# Objetivo: Información al administrador de la caída de un cliente.
# Descripción: El administrador recibirá información en el caso de caída de un cliente
#              que está monitorizado por un servidor. 

import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Clase creada para definir colores, que será utilizados para mensajes de consola.
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Clase Excepción para notificar que no existe conexion con un cliente.
class NoExisteConexionCliente1(Exception):
    """Excepcion que actua cuando no se detecta conexión con el cliente 1"""
    pass

# Clase Excepción para notificar que no existe conexion con un cliente.
class NoExisteConexionCliente2(Exception):
    """Excepcion que actua cuando no se detecta conexión con el cliente 2"""
    pass

# Subrutina que encuentra las IPs
def encontrarIPsServidores():
    ips = [0,0]
    archivo = open("/etc/zabbix/zabbix_agentd.conf")

    lineas = archivo.readlines()
    ipsServidores = lineas[97]
    ipsServidores = ipsServidores.replace("Server=127.0.0.1, 155.210.71.186, 155.210.71.164, ", "")
    
    ips[0] = ipsServidores[0:14]
    ips[1] = ipsServidores[16:30]
    return ips

# Función Ping
def ping(ip):
    response = os.system('ping -c 2 ' + ip+ ' >  /dev/null')

    if response == 0:
        return True
    else:
        return False
# Subrutina que comprueba la conexión con las IPs encontradas
def comprobarConexion(vector):
    if ping(vector[0]):
        print(bcolors.OKBLUE + "EXISTE CONEXION CON EL CLIENTE 1" + bcolors.ENDC)
    else:
        enviarEmailCliente1()
        raise NoExisteConexionCliente1

    if ping(vector[1]):
        print(bcolors.OKBLUE + "EXISTE CONEXION CON EL CLIENTE 2" + bcolors.ENDC)
    else:
        enviarEmailCliente2()
        raise NoExisteConexionCliente2  
# Subrutina que envia email al administtrados notificando caida del cliente 1
def enviarEmailCliente1():
    msg = MIMEMultipart()
    message = "Cliente 1 caido!!!"
    password = "admin2022"
    msg['From'] = "sistemas2122ingenieria@gmail.com"
    msg['To'] = "795505@unizar.es"
    msg['Subject'] = "Aviso, caida del cliente 1"
    msg.attach(MIMEText(message, 'plain'))
   
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)  
    server.sendmail(msg['From'], msg['To'], msg.as_string())
           
    server.quit()
            
    print ("Aviso enviado correctamente a  %s:" % (msg['To']))

# Subrutina que envia email al administtrados notificando caida del cliente 2
def enviarEmailCliente2():
    msg = MIMEMultipart()
    message = "Cliente 2 caido!!!"
    password = "admin2022"
    msg['From'] = "sistemas2122ingenieria@gmail.com"
    msg['To'] = "795505@unizar.es"
    msg['Subject'] = "Aviso, caida del cliente 2"
    msg.attach(MIMEText(message, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com: 587')       
    server.starttls()
    server.login(msg['From'], password)   
    server.sendmail(msg['From'], msg['To'], msg.as_string())
            
    server.quit()
            
    print ("Aviso enviado correctamente a  %s:" % (msg['To']))

    
# Subrutina main
def main() -> int:
    try:
       vectorIPs = encontrarIPsServidores()
       comprobarConexion(vectorIPs)
    except NoExisteConexionCliente1:
        print(bcolors.FAIL + bcolors.BOLD + "NO EXISTE CONEXION CON EL CLIENTE 1, AVISANDO AL ADMINISTRADOR" + bcolors.ENDC)
    except NoExisteConexionCliente2:
        print(bcolors.FAIL + bcolors.BOLD + "NO EXISTE CONEXION CON EL CLIENTE 2, AVISANDO AL ADMINISTRADOR" + bcolors.ENDC)

    return 0

# Comienzo de la ejecución
if __name__ == '__main__':
    main()