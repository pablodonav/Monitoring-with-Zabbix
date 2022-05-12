#!/usr/bin/python
# requisito_servidor_1.py

# Pablo Donate, Adnana Dragut y Diego Hernandez
#   Requisito de Servidor 1
#   Designacion: Alta de nuevo servidor sin argumentos 
#   Objetivo: Dar de alta a un nuevo servidor sin el paso de ningun tipo de argumentos. 
#   Descripcion: El alta de un servidor al sistema se realizara de forma automatica y
#                transparente una vez ejecutados los scripts correspondientes sin el paso
#                de ningun argumento.  

import sys
import os
import subprocess
import fileinput
from cmath import e
import socket
import re
from colorama import Fore
import contextlib
import mysql.connector

PORT = 1234
MSG_SIZE = 1024

# Clase Excepcion creada para notificar que el agente zabbix no ha podido ser arrancado
class ZabbixAgentError(Exception):
    """Excepcion que se lanza cuando se detecta un error que impide el arranque del agente Zabbix"""
    pass

def instalacionLamp():
    sudo_password = 'cliente2admin2'

    commandUpdate = 'apt update'.split()
    commandPurge = 'apt-get purge apache2 zabbix-server-mysql zabbix-frontend-php mariadb-server mariadb-client php'.split()
    commandInstallAp2 = 'apt-get install apache2'.split()
    commandInstallMar = 'apt-get install mariadb-server mariadb-client'.split()

    
    
    commandRestAp = 'service apache2 restart'.split()
    commandDisable = 'a2dismod mpm_event'.split()
    commandEnable = 'a2enmod php7.2'.split()

    with contextlib.redirect_stdout(None):
        p = subprocess.Popen(['sudo', '-l'], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        p.communicate(sudo_password + '\n')[1]

        purgA = subprocess.Popen(['sudo', '-S'] + commandPurge, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        purgA.communicate('S' + '\n')[1]
        purgA.wait()

        upd = subprocess.Popen(['sudo', '-S'] + commandUpdate, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        upd.wait()

        insAp2 = subprocess.Popen(['sudo', '-S'] + commandInstallAp2, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        insAp2.wait()
        
        insMar = subprocess.Popen(['sudo', '-S'] + commandInstallMar, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        insMar.wait()
        
        

        dis = subprocess.Popen(['sudo', '-S'] + commandDisable, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        dis.wait()

        en = subprocess.Popen(['sudo', '-S'] + commandEnable, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        en.wait()

        rest = subprocess.Popen(['sudo', '-S'] + commandRestAp, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        rest.wait()

def instalacionAgenteZabbix():
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

def modificacionFicheroLocalIPs():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        hostName = socket.gethostname()
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()

    replace_in_file("/etc/zabbix/zabbix_agentd.conf", "Server=127.0.0.1", "Server=127.0.0.1, " + IP)
    replace_in_file("/etc/zabbix/zabbix_agentd.conf", "ServerActive=127.0.0.1", "ServerActive=127.0.0.1, " + IP)
    replace_in_file("/etc/zabbix/zabbix_agentd.conf", "Hostname=Zabbix server", "Hostname=Client " + hostName)

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
    instalacionLamp()
    instalacionAgenteZabbix()
    modificacionFicheroLocalIPs()

# Comienzo de la ejecución
if __name__ == "__main__":
    main()