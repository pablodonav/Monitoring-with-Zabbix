#!/usr/bin/python
# requisito_servidor_1.py

# Pablo Donate, Adnana Dragut y Diego Hernandez
#   Requisito de Servidor 1
#   Designacion: Alta de nuevo servidor sin argumentos 
#   Objetivo: Dar de alta a un nuevo servidor sin el paso de ningun tipo de argumentos. 
#   Descripcion: El alta de un servidor al sistema se realizara de forma automatica y
#                transparente una vez ejecutados los scripts correspondientes sin el paso
#                de ningun argumento.  

from email.policy import compat32
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
    commandAlterUs = 'mysql -e "ALTER USER \'root\'@\'localhost\' IDENTIFIED BY \'root\';"'.split()
    commandDel1 = 'mysql -e "DELETE FROM mysql.user WHERE User=\'\';"'.split()
    commandDel2 = 'mysql -e "DELETE FROM mysql.user WHERE User=\'root\' AND Host NOT IN (\'localhost\', \'127.0.0.1\', \'::1\');"'.split()
    commandDrop = 'mysql -e "DROP DATABASE IF EXISTS test;"'.split()
    commandDel3 = 'mysql -e "DELETE FROM mysql.db WHERE Db=\'test\' OR Db=\'test\\_%\';"'.split()
    commandFlush = 'mysql -e "FLUSH PRIVILEGES;"'.split()
    commandInsPHP = 'apt install php php-cli php-mysql libapache2-mod-php'
    commandRestAp = 'service apache2 restart'.split()

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
        insAp2.communicate('S' + '\n')[1]
        insAp2.wait()
        
        insMar = subprocess.Popen(['sudo', '-S'] + commandInstallMar, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        insMar.communicate('S' + '\n')[1]
        insMar.wait()

        altUs = subprocess.Popen(['sudo', '-S'] + commandAlterUs, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        altUs.wait()

        del1 = subprocess.Popen(['sudo', '-S'] + commandDel1, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        del1.wait()

        del2 = subprocess.Popen(['sudo', '-S'] + commandDel2, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        del2.wait()

        drop = subprocess.Popen(['sudo', '-S'] + commandDrop, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        drop.wait()

        del3 = subprocess.Popen(['sudo', '-S'] + commandDel3, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        del3.wait()

        flush = subprocess.Popen(['sudo', '-S'] + commandFlush, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        flush.wait()

        insPhp = subprocess.Popen(['sudo', '-S'] + commandInsPHP, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        insPhp.communicate('S' + '\n')[1]
        insPhp.wait()

        rest = subprocess.Popen(['sudo', '-S'] + commandRestAp, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        rest.wait()

def instalacionServidorZabbix():
    command1 = 'dpkg -r zabbix-release'.split()
    command2 = 'wget https://repo.zabbix.com/zabbix/3.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.4-1+bionic_all.deb'.split()
    command3 = 'dpkg -i zabbix-release_3.4-1+bionic_all.deb'.split()

    command4 = 'apt update'.split()
    commandIns = 'apt install zabbix-server-mysql zabbix-frontend-php'.split()
        
    com1 = subprocess.Popen(['sudo', '-S'] + command1, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
    com1.wait()

    com2 = subprocess.Popen(['sudo', '-S'] + command2, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
    com2.wait()

    com3 = subprocess.Popen(['sudo', '-S'] + command3, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
    com3.wait()

    com4 = subprocess.Popen(['sudo', '-S'] + command4, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
    com4.wait()

    com5 = subprocess.Popen(['sudo', '-S'] + commandIns, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
    com5.communicate('S' + '\n')[1]
    com5.wait()

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
    instalacionServidorZabbix()
    instalacionAgenteZabbix()
    modificacionFicheroLocalIPs()

# Comienzo de la ejecución
if __name__ == "__main__":
    main()
