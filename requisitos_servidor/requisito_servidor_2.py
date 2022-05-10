#!/usr/bin/python
# requisito_servidor_2.py

# Pablo Donate, Adnana Dragut y Diego Hernandez
# Requisito de Servidor 2
# Designación: Alta de nuevo servidor con la dirección IP de un servidor
# Objetivo: Dar de alta a un nuevo servidor con el paso de la dirección IP de un
# servidor del sistema.
# Descripción: El servidor se unirá al sistema automáticamente una vez ejecutados los
# scripts correspondientes pasándole como argumento la dirección IP de
# algún servidor del sistema que esté en ejecución.



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

# Clase Excepcion creada para notificar que el agente zabbix no ha podido ser arrancado
class ZabbixAgentError(Exception):
    """Excepcion que se lanza cuando se detecta un error que impide el arranque del agente Zabbix"""
    pass
class NumberOfParametersError(Exception):
    """Excepción que se lanza cuando se detecta un error en los parámetros introducidos"""
    pass

class ParameterFormatError(Exception):
    """Excepción que se lanza cuando se detecta un error en la sintaxis del parámetro introducido"""
    pass



def instalacionLamp():
    sudo_password = 'cliente2admin2'

    commandUpdate = 'apt update'.split()
    commandPurge = 'apt-get purge apache2 zabbix-server-mysql zabbix-frontend-php mariadb-server mariadb-client'.split()
    commandInstall = 'apt-get install apache2 mariadb-server mariadb-client zabbix-server-mysql zabbix-frontend-php'.split()
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

        ins = subprocess.Popen(['sudo', '-S'] + commandInstall, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        ins.wait()

        dis = subprocess.Popen(['sudo', '-S'] + commandDisable, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        dis.wait()

        en = subprocess.Popen(['sudo', '-S'] + commandEnable, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        en.wait()

        rest = subprocess.Popen(['sudo', '-S'] + commandRestAp, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        rest.wait()

def replace_in_file(file_path, search_text, new_text):
    with fileinput.input(file_path, inplace=True) as file:
        for line in file:
            new_line = line.replace(search_text, new_text)
            print(new_line, end='')

def modificacionFicheroLocalIPs():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()

    replace_in_file("/etc/zabbix/zabbix_agentd.conf", "Server=127.0.0.1", "Server=127.0.0.1, " + IP)
    replace_in_file("/etc/zabbix/zabbix_agentd.conf", "ServerActive=127.0.0.1", "ServerActive=127.0.0.1, " + IP)
    replace_in_file("/etc/zabbix/zabbix_agentd.conf", "Hostname=Zabbix server", "Hostname=Cliente")

    # Arranca el agente Zabbix
    cmd = "sudo update-rc.d zabbix-agent enable"
    codeExit1 = os.system(cmd)

    cmd = "sudo service zabbix-agent restart"
    codeExit2 = os.system(cmd)

    if codeExit1 != 0 or codeExit2 != 0:
        raise ZabbixAgentError


# Función main
def main():
    instalacionLamp()
    instalacionAgenteZabbix()
    modificacionFicheroLocalIPs()

# Comienzo de la ejecución
if __name__ == "__main__":
    main()