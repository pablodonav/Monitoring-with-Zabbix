#!/usr/bin/python
# requisito_servidor_9.py

# Pablo Donate, Adnana Dragut y Diego Hernandez
# Requisito de Servidor 9
# Designación: Reasignación cliente-servidor. 
# Objetivo: Reasignación cliente-servidor en función de la carga. 
# Descripción: El cliente será reasignado a otro servidor en el caso de que el servidor
#              que lo está monitorizando tenga mayor carga. 

from pyzabbix import ZabbixAPI

# CONSTANTES
PORT = 1234
HOST = ""
MSG_SIZE = 1024
ZABBIX_SERVER_1 = "http://155.210.71.164/zabbix"
ZABBIX_SERVER_2 = "http://155.210.71.186/zabbix"
ZABBIX_SERVER_LOGIN = "Admin"
ZABBIX_SERVER_PWD = "zabbix"
ZABBIX_SERVER_1_NAME = "Zabbix server 1"
ZABBIX_SERVER_2_NAME = "Zabbix server 2"

# Establece conexión con ambos servidores
zapi1 = ZabbixAPI(ZABBIX_SERVER_1) # Dirección ip del servidor Zabbix 1
zapi1.login(ZABBIX_SERVER_LOGIN, ZABBIX_SERVER_PWD)

zapi2 = ZabbixAPI(ZABBIX_SERVER_2) # Dirección ip del servidor Zabbix 2
zapi2.login(ZABBIX_SERVER_LOGIN, ZABBIX_SERVER_PWD)

print("Connected to Server1 Zabbix API Version %s" % zapi1.api_version())
print("Connected to Server2 Zabbix API Version %s" % zapi2.api_version())

# Obtiene los ids de todos los hosts monitorizados por el servidor actual
def getHostsId(zapi):
    hostsId = zapi.host.get(
        output= ["hostid"]
    )
    return hostsId

# Obtiene el id del servidor que posee el nombre pasado por parámetro
def getServerId(_hostName, zapi):
    serverId = zapi.host.get(
        output= ["hostid"],
        filter= {
            "host": [_hostName]
        }
    )
    return serverId

# Obtiene todos los items monitorizados por el servidor actual
def getItems(_hostId, zapi):
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

# Programa principal
def main():
    serverLoad1 = getServerLoad(ZABBIX_SERVER_1_NAME, zapi1)
    serverLoad2 = getServerLoad(ZABBIX_SERVER_2_NAME, zapi2)

    print("\nEl tiempo total que le cuesta al servidor " + ZABBIX_SERVER_1_NAME + 
        " monitorizar todos los hosts es de " + str(serverLoad1[0]) + " horas")

    print("El tiempo total que le cuesta al servidor " + ZABBIX_SERVER_2_NAME + 
        " monitorizar todos los hosts es de " + str(serverLoad2[0]) + " horas \n")

    recursos1 = serverLoad1[1]
    recursos2 = serverLoad2[1]

    print("Los recursos HW disponibles del servidor " + ZABBIX_SERVER_1_NAME + " son los siguientes:\n" + 
       "    " + str(recursos1[0][0]) + " --> " + str(recursos1[0][1]) + "\n" +
       "    " + str(recursos1[1][0]) + " --> " + str(recursos1[1][1]) + "\n" +
       "    " + str(recursos1[2][0]) + " --> " + str(recursos1[2][1]) + "\n")

    print("Los recursos HW disponibles del servidor " + ZABBIX_SERVER_2_NAME + " son los siguientes:\n" + 
       "    " + str(recursos2[0][0]) + " --> " + str(recursos2[0][1]) + "\n" +
       "    " + str(recursos2[1][0]) + " --> " + str(recursos2[1][1]) + "\n" +
       "    " + str(recursos2[2][0]) + " --> " + str(recursos2[2][1]) + "\n")

if __name__ == "__main__":
    main()