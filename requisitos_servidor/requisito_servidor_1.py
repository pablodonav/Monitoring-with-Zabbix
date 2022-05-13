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

PORT = 1234
MSG_SIZE = 1024

# Clase Excepcion creada para notificar que el agente zabbix no ha podido ser arrancado
class ZabbixAgentError(Exception):
    """Excepcion que se lanza cuando se detecta un error que impide el arranque del agente Zabbix"""
    pass

def instalacionLamp():
    sudo_password = 'cliente2admin2'

    commandUpdate = 'apt update'.split()
    commandPurge = 'apt-get purge apache2 mariadb-server mariadb-client php zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent'.split()
    commandAutoRemove = 'apt autoremove'.split()
    commandRemove1 = 'sudo rm -rf /var/log/zabbix/'.split()
    commandRemove2 = 'sudo rm -rf /usr/share/doc/zabbix-server-mysql'.split()

    commandInstallAp2 = 'apt-get install apache2'.split()
    commandInstallMar = 'apt-get install mariadb-server mariadb-client'.split()
    commandAlterUs = 'mysql -e "ALTER USER \'root\'@\'localhost\' IDENTIFIED BY \'root\';"'.split()
    commandDel1 = 'mysql -e "DELETE FROM mysql.user WHERE User=\'\';"'.split()
    commandDel2 = 'mysql -e "DELETE FROM mysql.user WHERE User=\'root\' AND Host NOT IN (\'localhost\', \'127.0.0.1\', \'::1\');"'.split()
    commandDrop = 'mysql -e "DROP DATABASE IF EXISTS test;"'.split()
    commandDel3 = 'mysql -e "DELETE FROM mysql.db WHERE Db=\'test\' OR Db=\'test\\_%\';"'.split()
    commandFlush = 'mysql -e "FLUSH PRIVILEGES;"'.split()
    commandInsPHP = 'apt install php php-cli php-mysql libapache2-mod-php'.split()
    commandRestAp = 'service apache2 restart'.split()

    with contextlib.redirect_stdout(None):
        p = subprocess.Popen(['sudo', '-l'], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        p.communicate(sudo_password + '\n')[1]

        purg = subprocess.Popen(['sudo', '-S'] + commandPurge, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        purg.communicate('S' + '\n')[1]
        purg.wait()

        auto = subprocess.Popen(['sudo', '-S'] + commandAutoRemove, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        auto.communicate('S' + '\n')[1]
        auto.wait()

        rem1 = subprocess.Popen(['sudo', '-S'] + commandRemove1, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        rem1.wait()

        rem2 = subprocess.Popen(['sudo', '-S'] + commandRemove2, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        rem2.wait()


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
    command2 = 'wget https://repo.zabbix.com/zabbix/5.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_5.4-1+ubuntu20.04_all.deb'.split()
    command3 = 'dpkg -i zabbix-release_5.4-1+ubuntu20.04_all.deb'.split()
    command4 = 'apt update'.split()
    commandIns = 'apt install zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent'.split()

    commandDB1 = 'mysql -u root -proot -e "create database zabbix character set utf8 collate utf8_bin;"'.split()
    commandDB2 = 'mysql -u root -proot -e "grant all privileges on zabbix.* to zabbix@localhost identified by \'TestZabbix\';"'.split()

    commandStart = 'service zabbix-server start'.split()
    commandEnab = 'update-rc.d zabbix-server enable'.split()
        
    commandRestAp = 'service apache2 restart'.split()

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


    comDB1 = subprocess.Popen(['sudo', '-S'] + commandDB1, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
    comDB1.wait()

    comDB2 = subprocess.Popen(['sudo', '-S'] + commandDB2, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
    comDB2.wait()


    os.system('zcat /usr/share/doc/zabbix-sql-scripts/mysql/create.sql.gz | mysql -uzabbix -pTestZabbix zabbix')


    replace_in_file("/etc/zabbix/zabbix_server.conf", "# DBHost=localhost", "DBHost=localhost")
    replace_in_file("/etc/zabbix/zabbix_server.conf", "# DBPassword=", "DBPassword=TestZabbix")


    start = subprocess.Popen(['sudo', '-S'] + commandStart, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
    start.wait()

    enab = subprocess.Popen(['sudo', '-S'] + commandEnab, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
    enab.wait()

    replace_in_file("/etc/php/7.4/apache2/php.ini", "post_max_size = 8M", "post_max_size = 16M")
    replace_in_file("/etc/php/7.4/apache2/php.ini", "max_execution_time = 30", "max_execution_time = 300")
    replace_in_file("/etc/php/7.4/apache2/php.ini", "max_input_time = 60", "max_input_time = 300")
    replace_in_file("/etc/php/7.4/apache2/php.ini", ";date.timezone =", "date.timezone = Europe/Madrid")

    rest = subprocess.Popen(['sudo', '-S'] + commandRestAp, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
    rest.wait()

def instalacionAgenteZabbix():
    sudo_password = 'cliente2admin2'

    commandUninstall = 'apt-get purge zabbix-agent'.split()
    commandInstall = 'apt-get install zabbix-agent'.split()

    commandDis = 'a2dismod mpm_event'.split()
    commandEn = 'a2enmod php7.4'.split()
    
    commandRest = 'systemctl restart apache2'.split()

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

        comDis = subprocess.Popen(['sudo', '-S'] + commandDis, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        comDis.wait()

        comEn = subprocess.Popen(['sudo', '-S'] + commandEn, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        comEn.wait()


        commRes = subprocess.Popen(['sudo', '-S'] + commandRest, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            universal_newlines=True)
        commRes.wait()

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
