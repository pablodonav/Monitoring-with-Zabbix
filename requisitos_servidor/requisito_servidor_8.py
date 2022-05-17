#!/usr/bin/python
# requisito_de_servidor_8.py
#
# Pablo Doñate, Adnana Dragut y Diego Hernández
#   Requisito de Servidor 8
#   Designación: Carga del servidor.
#   Objetivo: Obtención de la carga del Servidor.
#   Descripción: La carga del servidor será establecida por el tiempo que tarda en
#                monitorizar a todos sus clientes así como los recursos hardware
#                disponibles.

from pyzabbix import ZabbixAPI

# CONSTANTES
PORT = 1234
HOST = ""
MSG_SIZE = 1024
ZABBIX_SERVER_2 = "http://155.210.71.186/zabbix"
ZABBIX_SERVER_2_LOGIN = "Admin"
ZABBIX_SERVER_2_PWD = "zabbix"
ZABBIX_SERVER_2_NAME = "Zabbix server 2"

# Establece conexión con el servidor 2
zapi = ZabbixAPI(ZABBIX_SERVER_2) # Dirección ip del servidor Zabbix
zapi.login(ZABBIX_SERVER_2_LOGIN, ZABBIX_SERVER_2_PWD)
print("Connected to Zabbix API Version %s" % zapi.api_version())

# Obtiene los ids de todos los hosts monitorizados por el servidor actual
def getHostsId():
    hostsId = zapi.host.get(
        output= ["hostid"]
    )
    return hostsId

# Obtiene el id del servidor que posee el nombre pasado por parámetro
def getServerId(_hostName):
    serverId = zapi.host.get(
        output= ["hostid"],
        filter= {
            "host": [_hostName]
        }
    )
    return serverId

# Obtiene todos los items monitorizados por el servidor actual
def getItems(_hostId):
    items = zapi.item.get(
        output= ["delay"],
        hostids=_hostId
    )
    return items

# Convierte segundos a horas
def convertSecondsToHours(_seconds):
    return float(_seconds // 3600)

# Convierte minutos a horas
def convertMinutesToHours(_minutes):
    return float(_minutes // 60)

# Convierte días a horas
def convertDaysToHours(_days):
    return float(_days * 24)

# Obtiene el tiempo total que le cuesta al servidor monitorizar todos los ítems de un host
def getTimeOfHostMonitoring(_items):
    totalHours = 0
    minutes = 0
    seconds = 0
    days = 0
    
    for item in _items:
        itemStr = item["delay"]
        
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
def getTotalTimeMonitoringHosts():
    totalTimeToMonitorHosts = 0
    hostsMonitorized = getHostsId()

    for host in hostsMonitorized:
        hoursMonitoringHost = getTimeOfHostMonitoring(getItems(host["hostid"]))
        totalTimeToMonitorHosts = totalTimeToMonitorHosts + hoursMonitoringHost

    return totalTimeToMonitorHosts

# Obtiene el porcentaje de memoria disponible del servidor
def getAvailableMemoryPercentage(_serverName):
    serverId = getServerId(_serverName)[0]["hostid"]

    freeMemoryPercentage = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_": "vm.memory.size[pavailable]"
        }
    )

    return freeMemoryPercentage[0]["lastvalue"]

# Obtiene el porcentaje de tiempo durante el cual el CPU del servidor está libre
def getCPUIdlePercentage(_serverName):
    serverId = getServerId(_serverName)[0]["hostid"]

    cpuIdlePercentage = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_": "system.cpu.util[,idle]"
        }
    )

    return cpuIdlePercentage[0]["lastvalue"]

# Obtiene el porcentaje de almacenamiento secundario libre del servidor
def getFreeDiskSpacePercentage(_serverName):
    serverId = getServerId(_serverName)[0]["hostid"]

    freeDiskSpacePercentage = zapi.item.get(
        output= ["lastvalue"],
        hostids= serverId,
        search= {
            "key_": "vfs.fs.size[/,pfree]"
        }
    )

    return freeDiskSpacePercentage[0]["lastvalue"]

# Obtiene un vector con los valores de los recursos hardware disponibles
def getHardwareResources(_serverName):
    resourcesValues = []

    resourcesValues.append(("Memory_Available (%)", getAvailableMemoryPercentage(_serverName)))
    resourcesValues.append(("CPU_Idle (%)", getCPUIdlePercentage(_serverName)))
    resourcesValues.append(("Free_DiskSpace (%)", getFreeDiskSpacePercentage(_serverName)))

    return resourcesValues

# Obtiene la carga del servidor
def getServerLoad(_serverName):
    serverLoad = []

    serverLoad.append(getTotalTimeMonitoringHosts())
    serverLoad.append(getHardwareResources(_serverName))

    return serverLoad

# Programa principal
def main():
    serverLoad = getServerLoad(ZABBIX_SERVER_2_NAME)

    print("El tiempo total que le cuesta al servidor " + ZABBIX_SERVER_2_NAME + 
        " monitorizar todos los hosts es de " + str(serverLoad[0]) + " horas")

    recursos = serverLoad[1]
    print("Los recursos HW disponibles del servidor " + ZABBIX_SERVER_2_NAME + " son los siguientes:\n" + 
       "    " + str(recursos[0][0]) + " --> " + str(recursos[0][1]) + "\n" +
       "    " + str(recursos[1][0]) + " --> " + str(recursos[1][1]) + "\n" +
       "    " + str(recursos[2][0]) + " --> " + str(recursos[2][1]))

if __name__ == "__main__":
    main()
