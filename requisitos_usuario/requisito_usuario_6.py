#!/usr/bin/python
# requisito_de_usuario6.py
#
# Pablo Doñate, Adnana Dragut y Diego Hernández
#   Requisito de Usuario 6
#   Designación: Detección de caída del servidor
#   Objetivo: Dar de alta a un nuevo usuario sin el paso de ningún tipo de argumentos. 
#   Descripción: Tras la caída de un servidor, el cliente que está siendo monitorizado por
#                dicho servidor deberá ser capaz de adaptarse al sistema para que de
#                forma transparente dicho cliente comience a ser monitorizado por otro
#                servidor en el caso de la existencia de algún servidor en ejecución.

import os
import fileinput
import socket
import re
from colorama import Fore

# CONSTANTES
PORT = 1234
MSG_SIZE = 1024
IP_SERVER1 = "155.210.71.186"
IP_SERVER2 = "155.210.71.164"
IP_LOOPBACK = "127.0.0.1"
ZABBIX_FILE = "/etc/zabbix/zabbix_agentd.conf"
SERVER_FILE = "/etc/zabbix/servers.txt"

# Clase Excepción creada para notificar que el agente zabbix no ha podido ser arrancado
class ZabbixAgentError(Exception):
    """Excepción que se lanza cuando se detecta un error que impide el arranque del agente Zabbix"""
    pass

# Subrutina que se encarga de crear el fichero servers.txt con las ips de los servidores disponibles
def crearDirectorioConFicheroServers():
    with open(SERVER_FILE, 'w') as f:
        f.write("Server=")
        f.write(IP_SERVER1 + ", ")
        f.write(IP_SERVER2 + "\n")

# Subrutina que se encarga de enviar un ping al host con la ip pasada por parámetro
def ping(ip):
    response = os.system("ping -c 1 " + ip + " 2>&1 >/dev/null")

    if response == 0:
        return True

    return False

# Subrutina que se encarga de obtener las ips de todos los servidores existentes en el path pasado por parámetro
def getIpsServers(path):
    config = open(path, "r")

    for line in config:
        line_found = re.search("^Server=.+", line)

        if (line_found):
            return line.replace(' ', '').rstrip()[7:].split(',')
    
    config.close()
    return[]

# Subrutina que se encarga de obtener el primer servidor que está en ejecución del fichero servers.txt
def getRunningServer():
    servers = getIpsServers(SERVER_FILE)

    for server in servers:
        if (ping(server)):
            return server
        return None  

# Subrutina que se encarga de obtener la ip del host que ejecuta este script
def getActualHostIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('10.255.255.255', 1))

    return s.getsockname()[0]

# Subrutina que se encarga de obtener la ip del servidor que monitoriza al cliente actual
def getMonitoringServer():
    servers = getIpsServers(ZABBIX_FILE)
    hostIp = getActualHostIp()

    # Obtiene la ip del servidor que monitoriza a este cliente
    for server in servers:
        if (server != IP_LOOPBACK and server != hostIp):
            return server
    
    return None

# Subrutina que se encarga de verificar si el servidor que monitoriza al host cliente está caído
def isMonitoringServerDown():
    monitoringServer = getMonitoringServer()

    if (not ping(monitoringServer)):
        return True

    return False

# Subrutina que se encarga de sustituir la ip del servidor caído por la ip de un servidor que está en ejecución
def replace_in_file(file_path, search_pattern, new_text):
    with fileinput.input(file_path, inplace=True) as file:
        for line in file:
            new_line = re.sub(rf"{search_pattern}", new_text, line)
            print(new_line, end='')

# Subrutina que se encarga de asignar un nuevo servidor a un host cliente en el caso en el que su servidor inicial está caído
def assignAnotherMonitoringServer():
    if (isMonitoringServerDown()):
        hostIP = getActualHostIp()
        runningServer = getRunningServer()

        if (runningServer):
            # Asigna un servidor en ejecución para que monitorice a este cliente
            replace_in_file(ZABBIX_FILE, "^Server=.+", "Server=127.0.0.1, " + hostIP + ", " + runningServer)
            replace_in_file(ZABBIX_FILE, "^ServerActive=.+", "ServerActive=127.0.0.1, " + hostIP + ", " + runningServer)

            # Arranca el agente Zabbix con los cambios del fichero de configuración
            cmd = "sudo update-rc.d zabbix-agent enable"
            codeExit1 = os.system(cmd)

            cmd = "sudo service zabbix-agent restart"
            codeExit2 = os.system(cmd)

            if codeExit1 != 0 or codeExit2 != 0:
                raise ZabbixAgentError
            else:
                print(Fore.GREEN, "It has been detected that the first monitoring server is down. Another server was configured to monitor this client.")
        else:
            # Finaliza la ejecución del agente en el cliente
            os.system("service zabbix-agent stop")
            
# Programa principal
def main():
    try:
        crearDirectorioConFicheroServers()
        assignAnotherMonitoringServer()
    except ZabbixAgentError:
        print(Fore.RED, "Error: Failed to start Zabbix agent.")

if __name__ == "__main__":
    main()