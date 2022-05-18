#!/usr/bin/python
# requisito_servidor_7.py

# Pablo Donate, Adnana Dragut y Diego Hernandez
# Requisito de Servidor 7
# Designación : Generación de un log de los datos monitorizados.
# Objetivo : Almacenamiento de los datos monitorizados en el sistema.
# Descripción : El servidor almacenará en un fichero log, los eventos que se van
#               produciendo referentes a la información que va monitorizando de sus
#               clientes

from pyzabbix import ZabbixAPI
from datetime import datetime

# Constantes
PORT = 1234
HOST = ""
MSG_SIZE = 1024
ZABBIX_SERVER_2 = "http://155.210.71.186/zabbix"
ZABBIX_SERVER_LOGIN = "Admin"
ZABBIX_SERVER_PWD = "zabbix"
ZABBIX_SERVER_NAME = "Zabbix server 2"
RUTA_LOG = "/var/log/zabbix/Server2.log"



# Establece conexión con el servidor

zapi = ZabbixAPI(ZABBIX_SERVER_2) # Dirección ip del servidor Zabbix 2
zapi.login(ZABBIX_SERVER_LOGIN, ZABBIX_SERVER_PWD)

print("Connected to Server 2 Zabbix API Version %s" % zapi.api_version())
    



# Convierte segundos a horas
def convertSecondsToHours(_seconds):
    return float(_seconds // 3600)

# Convierte minutos a horas
def convertMinutesToHours(_minutes):
    return float(_minutes // 60)

# Convierte días a horas
def convertDaysToHours(_days):
    return float(_days * 24)

def getHostsId(zapi):
    hostsId = zapi.host.get(
        output= ["hostid"]
    )
    return hostsId

# Obtiene Id de servidor
def getServerId(_hostName, zapi):
    serverId = zapi.host.get(
        output= ["hostid"],
        filter= {
            "host": [_hostName]
        }
    )
    return serverId
# Obtiene items de un host
def getItems(_hostId, zapi):
    items = zapi.item.get(
        output= ["delay"],
        hostids=_hostId
    )
    return items

# Subrutina que obtiene la monitorización del item de ancho de banda
def ItemForBandwidthMonitoring(_serverName, zapi):
    serverId = getServerId(_serverName, zapi)[0]["hostid"]

    BandwidthMonitoring = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_":"net.if.total[eth0]"
        }
    )

    return BandwidthMonitoring[0]["lastvalue"]

# Subrutina que se encarga de obtener la información del item que monitoriza la información
#   completa del sistema operativo de un host monitorizado.
def ItemForClientHostOSInformationMonitoring(_hostId, zapi):
    serverId = getServerId(_hostId, zapi)[0]["hostid"]

    ClientHostOSInformationMonitoring = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_":"system.sw.os[full]"
        }
    )

    return ClientHostOSInformationMonitoring[0]["lastvalue"]
# Subrutina que obtiene la información del item que monitoriza a los usuarios dados
#   de alta en el sistema
def ItemForUsersInformationMonitoring(_hostId, zapi):
    serverId = getServerId(_hostId, zapi)[0]["hostid"]

    UsersInformationMonitoring = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_":"system.run[cat /etc/passwd | awk -F ':' '{print $1}']"
        }
    )

    return UsersInformationMonitoring[0]["lastvalue"]
    

# Subrutina que obtiene la información del item que monitoriza la CPU
def getCPUMonitoring(_serverName, zapi):
    serverId = getServerId(_serverName, zapi)[0]["hostid"]

    CPUMonitoring = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_": "system.cpu.util[,,avg5]"
        }
    )

    return CPUMonitoring[0]["lastvalue"]


# Subrutina que obtiene la información del item que monitoriza la información de la memoria
def ItemForMemoryMonitorin(_hostId, zapi):
    serverId = getServerId(_hostId, zapi)[0]["hostid"]

    MemoryMonitoring = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_":"vm.memory.size[pavailable]"
        }
    )

    return MemoryMonitoring[0]["lastvalue"]

# Subrutina que obtiene la información del item que monitoriza los dispositivos de almacenamiento
def ItemForDiskSpaceMonitoring(_hostId, _interfaceId):
    serverId = getServerId(_hostId, zapi)[0]["hostid"]

    SpaceMonitoring = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_":"vfs.fs.size[/,pused]" 
        }
    )
    
    return SpaceMonitoring[0]["lastvalue"]

# Subrutina que obtiene información del item que monitoriza las tarjetas de red
def ItemForNetworkCardMonitoring(_hostId, _interfaceId):
    serverId = getServerId(_hostId, zapi)[0]["hostid"]

    NetworkMonitoring = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_" : "system.run[lshw -class network]",
        }
    )
    
    return NetworkMonitoring[0]["lastvalue"]
    



# Función main
def main():
    fichero = open(RUTA_LOG, "a")

    fichero.write("\n---------------------------------------------\n")
    fichero.write("\n"+datetime.today().strftime('%Y-%m-%d %H:%M:%S')+ "\n")   
    fichero.write("\nItemForCPUMonitoring --> " + getCPUMonitoring(ZABBIX_SERVER_NAME, zapi)+"\n")
    fichero.write("\nItemForDiskSpaceMonitoring--> " + ItemForDiskSpaceMonitoring(ZABBIX_SERVER_NAME, zapi)+"\n")
    fichero.write("\nItemForMemoryMonitoring --> " + ItemForMemoryMonitorin(ZABBIX_SERVER_NAME, zapi)+"\n")
    # fichero.write("\nItemForUsersInformationMonitoring --> " + ItemForUsersInformationMonitoring(ZABBIX_SERVER_NAME, zapi)+"\n")
    fichero.write("\nItemForClientHostOSInformationMonitoring --> " +ItemForClientHostOSInformationMonitoring(ZABBIX_SERVER_NAME, zapi)+"\n")
    fichero.write("\nItemForBandwidthMonitoring --> " + ItemForBandwidthMonitoring(ZABBIX_SERVER_NAME, zapi)+"\n")
    fichero.write("\ItemForNetworkCardMonitoring --> " + ItemForNetworkCardMonitoring(ZABBIX_SERVER_NAME, zapi)+"\n")
     
    

if __name__ == "__main__":
    main()