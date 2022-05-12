#!/usr/bin/python
# requisito_de_servidor5.py
#
# Pablo Doñate, Adnana Dragut y Diego Hernández
#   Requisito de Servidor 5
#   Designación: Información de Monitorización.
#   Objetivo: Monitorización de un conjunto de aspectos relevantes de cada uno de los
#             clientes asignados al servidor.
#   Descripción: El servidor monitorizará la siguiente información de cada uno de los
#                clientes:
#                   1. Ancho de banda usado en la subida.
#                   2. Sistema Operativo en el cliente e información del nodo.
#                   3. Usuarios dados de alta en el sistema.
#                   4. Información de la CPU.
#                   5. Información de la memoria.
#                   6. Información sobre los dispositivos de almacenamiento.
#                   7. Información de la tarjeta de red.

import socket
import threading
from pyzabbix import ZabbixAPI
from colorama import Fore, Style

# CONSTANTES
PORT = 1234
HOST = ""
MSG_SIZE = 1024
ZABBIX_SERVER_2 = "http://155.210.71.186/zabbix"
ZABBIX_SERVER_2_LOGIN = "Admin"
ZABBIX_SERVER_2_PWD = "admin2"

# Establece conexión con el servidor 2
zapi = ZabbixAPI(ZABBIX_SERVER_2) # Dirección ip del servidor Zabbix
zapi.login(ZABBIX_SERVER_2_LOGIN, ZABBIX_SERVER_2_PWD)
print("Connected to Zabbix API Version %s" % zapi.api_version())

# Subrutina que se encarga de obtener los hosts clientes que son monitorizados por este servidor
def getServerMonitorizedHosts():
    hosts = zapi.host.get(
        output="hostid",
        search= {
            "host": ["Client"]
        },
        startSearch="true"
    )
    return hosts

# Subrutina que se encarga de obtener el id de la interfaz de un host
def getHostInterfaceId(hostid):
    interfaceId = zapi.hostinterface.get(
        output="interfaceid",
        hostids=[hostid]
    )
    return interfaceId

# Subrutina que se encarga de crear el item para monitorizar el ancho de banda
#   usado en la subida
def creacionItemAnchoBandaUsadoEnSubida(hostid, interfaceid):
    itemId = zapi.item.create(
        name= "Bandwidth used on the upload",
        key_= "net.if.total[eth0]",
        hostid= 10289,
        type= 0,
        value_type= 3,
        interfaceid= 38,
        tags=[{
            "tag": "Bandwith usage"
        }],
        delay= "5m"
    );
    return itemId

# Programa principal
def main():
    hostId = getServerMonitorizedHosts()[0]["hostid"]
    interfaceId = getHostInterfaceId(hostId)[0]["interfaceid"]

    print(hostId)
    print(interfaceId)

    print(creacionItemAnchoBandaUsadoEnSubida(hostId, interfaceId))

if __name__ == "__main__":
    main()