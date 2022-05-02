#!/usr/bin/python
# requisito_de_usuario2.py
#
# Pablo Doñate, Adnana Dragut y Diego Hernández
#   Requisito de Usuario 2
#   Designación: Alta de nuevo cliente pasando la IP de un servidor
#   Objetivo: Dar de alta a un nuevo usuario con el paso de la dirección 
#       IP de un servidor del sistema. 
#   Descripción: El cliente se unirá al sistema automáticamente una vez ejecutados los
#       scripts correspondientes pasándole como argumento la dirección IP de
#       algún servidor del sistema que esté en ejecución. 

import sys
import os
import subprocess
import fileinput
from cmath import e
import socket
import re
from colorama import Fore
import contextlib

PORT = 1234
MSG_SIZE = 1024

# Clase para definir 
class NumberOfParametersError(Exception):
    """Excepción que se lanza cuando se detecta un error en los parámetros introducidos"""
    pass

class ParameterFormatError(Exception):
    """Excepción que se lanza cuando se detecta un error en la sintaxis del parámetro introducido"""
    pass

# Clase Excepción creada para notificar que el agente zabbix no ha podido ser arrancado
class ZabbixAgentError(Exception):
    """Excepción que se lanza cuando se detecta un error que impide el arranque del agente Zabbix"""
    pass

def comprobarParametros() -> None:
    if len(sys.argv) != 2:
        raise NumberOfParametersError

    aa=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",sys.argv[1])
    if not aa:
        raise ParameterFormatError

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
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()

    replace_in_file("/etc/zabbix/zabbix_agentd.conf", "Server=127.0.0.1", "Server=127.0.0.1, " + IP + ", " + sys.argv[1])
    replace_in_file("/etc/zabbix/zabbix_agentd.conf", "ServerActive=127.0.0.1", "ServerActive=127.0.0.1, " + IP + ", " + sys.argv[1])
    replace_in_file("/etc/zabbix/zabbix_agentd.conf", "Hostname=Zabbix server", "Hostname=Cliente")

    # Arranca el agente Zabbix
    cmd = "sudo update-rc.d zabbix-agent enable"
    codeExit1 = os.system(cmd)

    cmd = "sudo service zabbix-agent restart"
    codeExit2 = os.system(cmd)

    if codeExit1 != 0 or codeExit2 != 0:
        raise ZabbixAgentError

# Subrutina para añadir cliente al nuevo servidor que le va a monitorizar.
def add_client():

    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((sys.argv[1], PORT))
    s.send(bytes("ADD_CLIENT| " + socket.gethostname(), encoding='utf8'))
    mensaje_recibido = s.recv(MSG_SIZE)
    s.close()

    print(Fore.GREEN, "\nMsg recibido: " + str(mensaje_recibido))

# Función main
def main():
    try:
        comprobarParametros()
        instalacionAgenteZabbix()
        modificacionFicheroLocalIPs()
        add_client()

    except NumberOfParametersError:
        print(Fore.RED, "Error: el número de parámetros introducidos no es correcto.")
    except ParameterFormatError:
        print(Fore.RED, "Error: el parámetro introducido debe ser una dirección IP válida.")
    except ZabbixAgentError:
        print(Fore.RED, "Error: no se ha podido arrancar el agente Zabbix.")
    except Exception as  e:
        print(Fore.RED, "Error: no se ha podido realizar la conexión con el servidor.")

if __name__ == "__main__":
    main()