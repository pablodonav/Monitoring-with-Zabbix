#!/usr/bin/python
# requisito_usuario_3.py
#
# Pablo Doñate, Adnana Dragut y Diego Hernández
#   Requisito de Usuario 3
#   Designación: Fin de la ejecución del cliente
#   Objetivo: Finalización de la ejecución por parte del cliente si no existe ningún
#             servidor en ejecución.
#   Descripción: El cliente finalizará su ejecución en el caso de no existir ningún servidor
#                en el sistema en ejecución. 

import os

# Clase para cambiar el color de textos al imprimirlos por pantalla
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

class NoExisteConexionServidor1(Exception):
    """Excepcion que actua cuando no se detecta conexión con el servidor 1"""
    pass

class NoExisteConexionServidor2(Exception):
    """Excepcion que actua cuando no se detecta conexión con el servidor 2"""
    pass

def encontrarIPsServidores():
    ips = [0,0]
    archivo = open("/etc/zabbix/zabbix_agentd.conf")

    lineas = archivo.readlines()
    ipsServidores = lineas[97]
    ipsServidores = ipsServidores.replace("Server=127.0.0.1, 155.210.71.183, ", "")
    
    ips[0] = ipsServidores[0:14]
    ips[1] = ipsServidores[16:30]
    return ips

# Función Ping
def ping(ip):
    response = os.system('ping -c 2 ' + ip+ ' > dev.txt')

    if response == 0:
        return True
    else:
        return False

# Comprueba conexión con los servidores
def comprobarConexion(vector):
    if ping(vector[0]):
        print(bcolors.OKBLUE + "EXISTE CONEXION CON EL SERVIDOR 1" + bcolors.ENDC)
    else:
        os.system('systemctl stop zabbix-agent > /dev/null')
        raise NoExisteConexionServidor1

    if ping(vector[1]):
        print(bcolors.OKBLUE + "EXISTE CONEXION CON EL SERVIDOR 2" + bcolors.ENDC)
    else:
        os.system('sudo systemctl stop zabbix-agent > /dev/null')
        raise NoExisteConexionServidor2
        
# Función main
def main() -> int:
    try:
       vectorIPs = encontrarIPsServidores()
       comprobarConexion(vectorIPs)

    except NoExisteConexionServidor1:
        print(bcolors.FAIL + bcolors.BOLD + "NO EXISTE CONEXION CON EL SERVIDOR 1, FINALIZANDO EJECUCION DEL CLIENTE" + bcolors.ENDC)
    except NoExisteConexionServidor2:
        print(bcolors.FAIL + bcolors.BOLD + "NO EXISTE CONEXION CON EL SERVIDOR 2, FINALIZANDO EJECUCION DEL CLIENTE" + bcolors.ENDC)

    return 0


# Comienzo de la ejecución
if __name__ == '__main__':
    main()
