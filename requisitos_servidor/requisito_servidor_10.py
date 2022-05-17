import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

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

class NoExisteConexionCliente1(Exception):
    """Excepcion que actua cuando no se detecta conexión con el cliente 1"""
    pass

class NoExisteConexionCliente2(Exception):
    """Excepcion que actua cuando no se detecta conexión con el cliente 2"""
    pass

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