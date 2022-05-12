#!/usr/bin/python
# requisito_de_usuario1.py
#
# Pablo Doñate, Adnana Dragut y Diego Hernández
#   Requisito de Usuario 1
#   Designación: Alta de nuevo cliente sin argumentos
#   Objetivo: Dar de alta a un nuevo usuario sin el paso de ningún tipo de argumentos. 
#   Descripción: El alta de un cliente al sistema se realizará de forma automática y
#       transparente una vez ejecutados los scripts correspondientes sin el paso
#       de ningún argumento.

import os
import subprocess
import fileinput
import socket
from colorama import Fore
import contextlib

# CONSTANTES
PORT = 1234
MSG_SIZE = 1024
IP_SERVER = "155.210.71.186"

# Clase Excepción creada para notificar que el agente zabbix no ha podido ser arrancado
class ZabbixAgentError(Exception):
    """Excepción que se lanza cuando se detecta un error que impide el arranque del agente Zabbix"""
    pass

def instalacionAgenteZabbix() -> None:
    sudo_password = 'cliente2admin2'

    commandUninstall = 'apt-get purge zabbix-agent'.split()
    commandInstall = 'apt-get install zabbix-agent'.split()

    with contextlib.redirect_stdout(None):
        p = subprocess.Popen(['sudo', '-l'], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)

        p.communicate(sudo_password + '\n')[1]

        rem = subprocess.Popen(['sudo', '-S'] + commandUninstall, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)

        rem.communicate('S' + '\n')[1]
        rem.wait()

        ins = subprocess.Popen(['sudo', '-S'] + commandInstall, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        ins.wait()

def replace_in_file(file_path, search_text, new_text):
    with fileinput.input(file_path, inplace=True) as file:
        for line in file:
            new_line = line.replace(search_text, new_text)
            print(new_line, end='')

def modificacionFicheroLocalIPs() -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        hostName = socket.gethostname()
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()

    replace_in_file("/etc/zabbix/zabbix_agentd.conf", "Server=127.0.0.1", "Server=127.0.0.1, " + IP + ", " + IP_SERVER)
    replace_in_file("/etc/zabbix/zabbix_agentd.conf", "ServerActive=127.0.0.1", "ServerActive=127.0.0.1, " + IP + ", " + IP_SERVER)
    replace_in_file("/etc/zabbix/zabbix_agentd.conf", "Hostname=Zabbix server", "Hostname=Client " + hostName)

    # Arranca el agente Zabbix con los cambios del fichero de configuración
    cmd = "sudo update-rc.d zabbix-agent enable"
    codeExit1 = os.system(cmd)

    cmd = "sudo service zabbix-agent restart"
    codeExit2 = os.system(cmd)

    if codeExit1 != 0 or codeExit2 != 0:
        raise ZabbixAgentError

# Subrutina para añadir cliente al nuevo servidor que le va a monitorizar.
def add_client():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((IP_SERVER, PORT))
    s.send(bytes("ADD_CLIENT| " + socket.gethostname(), encoding='utf8'))
    mensaje_recibido = s.recv(MSG_SIZE)
    s.close()

    print(Fore.GREEN, "\nMsg received: " + str(mensaje_recibido))

def main():
    try:
        instalacionAgenteZabbix()
        modificacionFicheroLocalIPs()
        add_client()

    except ZabbixAgentError:
        print(Fore.RED, "Error: Failed to start Zabbix agent.")
    except Exception as  e:
        print(Fore.RED, "Error: The connection to the server could not be made.")

if __name__ == "__main__":
    main()