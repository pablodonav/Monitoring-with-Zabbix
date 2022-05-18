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
RUTA_LOG = "/var/log/zabbix/"



# Establece conexión con ambos servidores

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
        output= ["lastvalue"],
        hostids=_hostId
    )
    return items
# Obtiene el tiempo total que le cuesta al servidor monitorizar todos los ítems de un host
def getTimeOfHostMonitoring(_items):
    totalHours = 0
    minutes = 0
    seconds = 0
    days = 0
    
    for item in _items:
        itemStr = item["lastvalue"]
        
        if itemStr[-1] is "s":
            itemStr = itemStr[:-1]
            seconds = seconds + float(itemStr)
        elif itemStr[-1] is "m":
            itemStr = itemStr[:-1]
            minutes = minutes + float(itemStr)
        elif itemStr[-1] is "h":
            itemStr = itemStr[:-1]
            totalHours = totalHours + float(itemStr)
        elif itemStr[-1] is "d":
            itemStr = itemStr[:-1]
            days = days + float(itemStr)

    totalHours = totalHours + convertSecondsToHours(seconds) + convertMinutesToHours(minutes) + convertDaysToHours(days)
    return totalHours

# Obtiene el tiempo total de monitorización de todos los hosts
def getTotalTimeMonitoringHosts(zapi):
    totalTimeToMonitorHosts = 0
    hostsMonitorized = getHostsId(zapi)

    for host in hostsMonitorized:
        hoursMonitoringHost = getTimeOfHostMonitoring(getItems(host["hostid"], zapi))
        totalTimeToMonitorHosts = totalTimeToMonitorHosts + hoursMonitoringHost

    return totalTimeToMonitorHosts

# Obtiene el porcentaje de memoria disponible del servidor
def getAvailableMemoryPercentage(_serverName, zapi):
    serverId = getServerId(_serverName, zapi)[0]["hostid"]

    freeMemoryPercentage = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_": "vm.memory.size[pavailable]"
        }
    )

    return freeMemoryPercentage[0]["lastvalue"]

# Obtiene el porcentaje de tiempo durante el cual el CPU del servidor está libre
def getCPUIdlePercentage(_serverName, zapi):
    serverId = getServerId(_serverName, zapi)[0]["hostid"]

    cpuIdlePercentage = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_": "system.cpu.util[,idle]"
        }
    )

    return cpuIdlePercentage[0]["lastvalue"]

# Obtiene el porcentaje de almacenamiento secundario libre del servidor
def getFreeDiskSpacePercentage(_serverName, zapi):
    serverId = getServerId(_serverName, zapi)[0]["hostid"]

    freeDiskSpacePercentage = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_": "vfs.fs.size[/,pfree]"
        }
    )

    return freeDiskSpacePercentage[0]["lastvalue"]

# Obtiene un vector con los valores de los recursos hardware disponibles
def getHardwareResources(_serverName, zapi):
    resourcesValues = []

    resourcesValues.append(("Memory_Available (%)", getAvailableMemoryPercentage(_serverName, zapi)))
    resourcesValues.append(("CPU_Idle (%)", getCPUIdlePercentage(_serverName, zapi)))
    resourcesValues.append(("Free_DiskSpace (%)", getFreeDiskSpacePercentage(_serverName, zapi)))

    return resourcesValues

# Obtiene la carga del servidor
def getServerLoad(_serverName, zapi):
    serverLoad = []

    serverLoad.append(getTotalTimeMonitoringHosts(zapi))
    serverLoad.append(getHardwareResources(_serverName, zapi))

    return serverLoad

def removeHost(zapi):
    hostId = zapi.host.get(
        output="hostid",
        filter =  { 'host': "Client eupt-admin2-03"}
    )

    removedHost = zapi.host.delete(
        hostId[0]["hostid"]
    );

    if removedHost:
        return True
    else:
        return False
   


def main():
    fichero = open("Server2.log", "a")

    fichero.write("\n---------------------------------------------\n")

    fichero.write("\n"+datetime.today().strftime('%Y-%m-%d %H:%M:%S')+ "\n")
    serverLoad = getServerLoad(ZABBIX_SERVER_NAME, zapi)
    recursos = serverLoad[1]
    loadServer = format((100 - ((float(recursos[0][1]) + float(recursos[1][1]) + float(recursos[2][1])) / 3)),".3f")
    fichero.write
    fichero.write("\nTiempo empleado para monitorizar "+ ZABBIX_SERVER_NAME + str(serverLoad[0]) + " horas\n")
    
    fichero.write("\n"+ "Item de monitorización de recursos " + ZABBIX_SERVER_NAME +"\n"
       "    " + str(recursos[0][0]) + " --> " + str(recursos[0][1]) + "\n" +
       "    " + str(recursos[1][0]) + " --> " + str(recursos[1][1]) + "\n" +
       "    " + str(recursos[2][0]) + " --> " + str(recursos[2][1]) + "\n")

    fichero.write("\nItem de carga del servidor " + ZABBIX_SERVER_NAME + " es " + str(loadServer) + "%\n")


if __name__ == "__main__":
    main()
