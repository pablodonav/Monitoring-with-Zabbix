#!/usr/bin/python
# caso_de_uso_4.py
#
# Pablo Doñate, Adnana Dragut y Diego Hernández
#   Caso de Uso 4
#   Designación: Caída de un nodo Cliente
#   Objetivo: Detección de la caída de un nodo cliente para volver a adaptarse el
#             sistema a un estado estable. 
#   Precondiciones: El nodo cliente se encontrará en ejecución y monitorizado por un
#                   servidor del sistema.
#   Post-condiciones: Sistema en correcto funcionamiento sin errores.
#   Operaciones: 1. El servidor detecta la caída del cliente.
#                2. El servidor lleva a cabo las correspondientes acciones para que el
#                   sistema se encuentre en un estado estable.

from pyzabbix import ZabbixAPI
from colorama import Fore
import os

# CONSTANTES
PORT = 1234
HOST = ""
MSG_SIZE = 1024
ZABBIX_SERVER_2 = "http://155.210.71.186/zabbix"
ZABBIX_SERVER_2_LOGIN = "Admin"
ZABBIX_SERVER_2_PWD = "zabbix"
IP_LOOPBACK = "127.0.0.1"

# Clase Excepción creada para notificar que no se ha podido eliminar un host caído
class ErrorOnDeleteHost(Exception):
    """Excepción que se lanza cuando se detecta un error que impide borrar un host caído"""
    pass

# Establece conexión con el servidor 2
zapi = ZabbixAPI(ZABBIX_SERVER_2) # Dirección ip del servidor Zabbix
zapi.login(ZABBIX_SERVER_2_LOGIN, ZABBIX_SERVER_2_PWD)
print("Connected to Zabbix API Version %s" % zapi.api_version())

# Subrutina que se encarga de enviar un ping al host con la ip pasada por parámetro
def ping(ip):
    response = os.system("ping -c 1 " + ip + " 2>&1 >/dev/null")

    if response == 0:
        return True

    return False

# Subrutina que se encarga de obtener todos los hosts monitorizados por el servidor
def getMonitoredHosts():
    hosts = zapi.hostinterface.get(
        output="extend"
    )
    return hosts

# Subrutina que se encarga de obtener los identificadores de los hosts que están caídos
def getUnreachableHosts():
    unreachableHosts = []
    monitoredHosts = getMonitoredHosts()

    for host in monitoredHosts:
        if (host["ip"] != IP_LOOPBACK):
            if(not ping(host["ip"])):
                unreachableHosts.append(host)
    
    return unreachableHosts

# Subrutina que elimina un host que estaba monitorizando.
def removeHost(_hostid):
    removedHost = zapi.host.delete(
        _hostid
    );

    if removedHost:
        return True
    else:
        return False

# Subrutina que obtiene los hosts caídos y los elimina.
def removeUnreachableHosts():
    unreachableHosts = getUnreachableHosts()

    for host in unreachableHosts:
        if(removeHost(host["hostid"])):
            print(Fore.GREEN, "The host has been deleted successfully")
        else:
            raise ErrorOnDeleteHost

# Programa principal
def main():
    try:
        removeUnreachableHosts()
    except ErrorOnDeleteHost:
        print(Fore.RED, "Error: The host could not be removed")

if __name__ == "__main__":
    main()