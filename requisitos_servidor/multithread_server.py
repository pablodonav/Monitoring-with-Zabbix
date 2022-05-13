#!/usr/bin/python
# multithread_server.py
#
# Pablo Doñate, Adnana Dragut y Diego Hernández
#   Requisito de Servidor 3
#   Designación: Recepción de peticiones por TCP
#   Objetivo: Uso del protocolo TCP para la recepción de peticiones de altas
#   Descripción: El servidor recibirá peticiones de alta en el sistema gracias al protocolo TCP

import socket
import threading
from pyzabbix import ZabbixAPI
from colorama import Fore, Style

# CONSTANTES
PORT = 1234
HOST = ""
MSG_SIZE = 1024
ZABBIX_SERVER_1 = "http://155.210.71.186/zabbix"
ZABBIX_SERVER_1_LOGIN = "Admin"
ZABBIX_SERVER_1_PWD = "admin2"
GROUP_NAME = "Zabbix servers"
TEMPLATE_NAME  = "Linux by Zabbix agent"

# Establece conexión con el servidor 2
zapi = ZabbixAPI(ZABBIX_SERVER_1) # Dirección ip del servidor Zabbix
zapi.login(ZABBIX_SERVER_1_LOGIN, ZABBIX_SERVER_1_PWD)
print("Connected to Zabbix API Version %s" % zapi.api_version())

# Clase Excepción creada para notificar que el host está desconectado
class HostDisconnected(Exception):
    """Excepción que se lanza cuando el host está desconectado"""
    pass

# Clase Excepción creada para notificar fallos al ejecutar una operación solicitada 
class OperationError(Exception):
    """Excepción que se lanza cuando la operación solicitada tiene éxito"""
    pass

# Clase que contiene los métodos de los threads que atienden a los hosts clientes
class ClientThread(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    # Acepta conexiones de los clientes
    def listen(self):
        self.sock.listen(5)
        while True:
            print("Waiting for client connection...\n")
            conn, address = self.sock.accept()
            conn.settimeout(60)
            threading.Thread(target = self.run,args = (conn,address)).start()

    # Recibe peticiones del host cliente
    def run(self, conn, address):
        try:
            connRequest = (conn.recv(MSG_SIZE).decode()).split("|")

            operation = connRequest[0]
            parameters = connRequest[1]
            
            if operation:
                operationStatus = ClientThread.doRequest(operation, parameters, conn, address)

                if operationStatus:
                    print(Fore.GREEN, "Operation executed successfully.")
                else:
                    raise OperationError
            else:
                raise HostDisconnected
        except HostDisconnected:
            print(Fore.RED, "\nError: Connection with client has failed.")
        except OperationError:
            print(Fore.RED, "\nError: Operation execution has failed.")
        finally:
            print(Fore.YELLOW, "Connection with client has been closed.")
            print(Style.RESET_ALL)
            conn.close()
            return False

    # Obtiene el identificador del grupo cuyo nombre se pasa por parámetro
    def getGroupId(_groupName): 
        groupId = zapi.hostgroup.get(
            output="groupid",
            filter= {
                "name": [_groupName]
            }
        )
        return groupId

    # Obtiene el identificador de la plantilla cuyo nombre se pasa por parámetro
    def getTemplateId(_templateName):
        templateId = zapi.template.get(
            output= "templateid", 
            filter= { 
                "host": [_templateName]
            }
        )
        return templateId

    # Da de alta un nuevo host tras recibir petición TCP.
    def addHost(conn, addr, parameters):
        groupId = ClientThread.getGroupId(GROUP_NAME)[0]["groupid"]
        templateId = ClientThread.getTemplateId(TEMPLATE_NAME)[0]["templateid"]

        createdHost = zapi.host.create(
            host="Client" + parameters,
            interfaces= [{"type": 1, "main": 1, "useip": 1, "ip": addr[0], "dns": "", "port": 10050}],
            groups= [{"groupid": groupId}],
            templates= [{"templateid": templateId}],
            inventory_mode= 1
        );

        if createdHost:
            conn.send(b"Host added successfully")
            return True
        else:
            conn.send(b"Couldn't add host")
            return False
    
    # Ejecuta las operaciones solicitadas por el host cliente
    def doRequest(operation, parameters, conn, addr):
        print(f"Operation {operation} was requested by the client {addr[0]}.")

        if operation == "ADD_CLIENT":
            return ClientThread.addHost(conn, addr, parameters)

# Programa principal
def main():
    ClientThread(HOST, PORT).listen()

if __name__ == "__main__":
    main()
