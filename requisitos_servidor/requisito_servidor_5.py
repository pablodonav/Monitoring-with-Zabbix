#!/usr/bin/python
# requisito_de_servidor5.py
#
# Pablo Doñate, Adnana Dragut y Diego Hernández
#   Requisito de Servidor 5
#   Designación: Información de Monitorización.
#   Objetivo: Monitorización de un conjunto de aspectos relevantes de cada uno de los
#             clientes asignados al servidor.
#   Descripción: El servidor monitorizará la siguiente información de cada uno de los
#                clientes:
#                   1. Ancho de banda usado en la subida.
#                   2. Sistema Operativo en el cliente e información del nodo.
#                   3. Usuarios dados de alta en el sistema.
#                   4. Información de la CPU.
#                   5. Información de la memoria.
#                   6. Información sobre los dispositivos de almacenamiento.
#                   7. Información de la tarjeta de red.

from pyzabbix import ZabbixAPI
from colorama import Fore

# CONSTANTES
PORT = 1234
HOST = ""
MSG_SIZE = 1024
ZABBIX_SERVER_2 = "http://155.210.71.186/zabbix"
ZABBIX_SERVER_2_LOGIN = "Admin"
ZABBIX_SERVER_2_PWD = "zabbix"

# Establece conexión con el servidor 2
zapi = ZabbixAPI(ZABBIX_SERVER_2) # Dirección ip del servidor Zabbix
zapi.login(ZABBIX_SERVER_2_LOGIN, ZABBIX_SERVER_2_PWD)
print("Connected to Zabbix API Version %s" % zapi.api_version())

# Clase Excepción creada para notificar que no se ha podido crear el item BandwithMonitoring
class ErrorBandwidthMonitoring(Exception):
    """Excepción que se lanza cuando no se ha podido crear el item para monitorizar el ancho de banda"""
    pass

# Clase Excepción creada para notificar que no se ha podido crear el item OSInformation
class ErrorOSInformationMonitoring(Exception):
    """Excepción que se lanza cuando no se ha podido crear el item para monitorizar la información del SO"""
    pass

# Clase Excepción creada para notificar que no se ha podido crear el item UsersInformation
class ErrorUsersInformationMonitoring(Exception):
    """Excepción que se lanza cuando no se ha podido crear el item para monitorizar los usuarios dados de alta en el sistema"""
    pass

# Clase Excepción creada para notificar que no se ha podido crear el item CPUMonitoring
class ErrorCPUMonitoring(Exception):
    """Excepción que se lanza cuando no se ha podido crear el item para monitorizar la cpu"""
    pass

# Clase Excepción creada para notificar que no se ha podido crear el item MemoryMonitoring
class ErrorMemoryMonitoring(Exception):
    """Excepción que se lanza cuando no se ha podido crear el item para monitorizar la información de la memoria"""
    pass

# Clase Excepción creada para notificar que no se ha podido crear el item DiskSpaceMonitoring
class ErrorDiskSpaceMonitoring(Exception):
    """Excepción que se lanza cuando no se ha podido crear el item para monitorizar la información de almacenamiento"""
    pass

# Clase Excepción creada para notificar que no se ha podido crear el item NetworkCardMonitoring
class ErrorNetworkCardMonitoring(Exception):
    """Excepción que se lanza cuando no se ha podido crear el item para monitorizar la información de las tarjetas de red"""
    pass

# Subrutina que se encarga de obtener los hosts clientes que son monitorizados por este servidor
def getServerMonitorizedHosts():
    hosts = zapi.host.get(
        output="hostId"
    )
    return hosts

# Subrutina que se encarga de obtener el id de la interfaz de un host
def getHostInterfaceId(_hostId):
    interfaceId = zapi.hostinterface.get(
        output="interfaceId",
        hostids=[_hostId]
    )
    return interfaceId[0]["interfaceid"]

# Subrutina que se encarga de obtener el id de la aplicación "Network interfaces"
def getNetworkApplicationId(_hostId):
    networkAppId = zapi.application.get(
        output="applicationId",
        hostids=[_hostId],
        search= {
            "name": ["Network interfaces"]
        },
        startSearch="true"
    )
    return networkAppId[0]["applicationid"]

# Subrutina que se encarga de crear el item para monitorizar el ancho de banda
#   usado en la subida
def createItemForBandwidthMonitoring(_hostId, _interfaceId):
    networkAppId = getNetworkApplicationId(_hostId)
    
    bandwidthItemId = zapi.item.create(
        name= "Bandwidth used on the upload",
        key_= "net.if.total[eth0]",
        hostid= _hostId,
        type= 0,
        value_type= 3,
        interfaceid= _interfaceId,
        tags=[{
            "tag": "Bandwith usage"
        }],
        applications=[
            networkAppId
        ],
        delay= "5m"
    );
    return bandwidthItemId

# Subrutina que se encarga de obtener el id de la aplicación "OS"
def getOSApplicationId(_hostId):
    OSAppId = zapi.application.get(
        output="applicationId",
        hostids=[_hostId],
        search= {
            "name": ["OS"]
        },
        startSearch="true"
    )
    return OSAppId[0]["applicationid"]

# Subrutina que se encarga de crear el item para monitorizar la información
#   completa del sistema operativo de un host monitorizado
def createItemForClientHostOSInformationMonitoring(_hostId, _interfaceId):
    OSAppId = getOSApplicationId(_hostId)

    itemId = zapi.item.create(
        name= "Host OS information",
        key_= "system.sw.os[full]",
        hostid= _hostId,
        type= 0,
        value_type= 4,
        interfaceid= _interfaceId,
        tags=[{
            "tag": "SO full information"
        }],
        applications=[
            OSAppId
        ],
        delay= "1d"
    );
    return itemId

# Subrutina que se encarga de obtener el id de la aplicación "General"
def getGeneralApplicationId(_hostId):
    generalAppId = zapi.application.get(
        output="applicationId",
        hostids=[_hostId],
        search= {
            "name": ["General"]
        },
        startSearch="true"
    )
    return generalAppId[0]["applicationid"]

# Subrutina que se encarga de crear el item para monitorizar los 
#   usuarios dados de alta en el sistema
def createItemForUsersInformationMonitoring(_hostId, _interfaceId):
    generalAppId = getGeneralApplicationId(_hostId)

    itemId = zapi.item.create(
        name= "Host users",
        key_= "system.run[cat /etc/passwd | awk -F ':' '{print $1}']",
        hostid= _hostId,
        type= 0,
        value_type= 4,
        interfaceid= _interfaceId,
        tags=[{
            "tag": "Name of all client users"
        }],
        applications=[
            generalAppId
        ],
        delay= "1d"
    );
    return itemId

# Subrutina que se encarga de obtener el id de la aplicación "CPU"
def getCPUApplicationId(_hostId):
    CPUAppId = zapi.application.get(
        output="applicationId",
        hostids=[_hostId],
        search= {
            "name": ["CPU"]
        },
        startSearch="true"
    )
    return CPUAppId[0]["applicationid"]

# Subrutina que se encarga de crear el item para monitorizar la
#   información de la CPU
def createItemForCPUMonitoring(_hostId, _interfaceId):
    CPUAppId = getCPUApplicationId(_hostId)

    itemId = zapi.item.create(
        name= "Host cpu utilization percentage",
        key_= "system.cpu.util[all,user,avg5]",
        hostid= _hostId,
        type= 0,
        value_type= 0,
        interfaceid= _interfaceId,
        tags=[{
            "tag": "Client host total cpu utilization"
        }],
        applications=[
            CPUAppId
        ],
        delay= "1m"
    );
    return itemId

# Subrutina que se encarga de obtener el id de la aplicación "Memory"
def getMemoryApplicationId(_hostId):
    memoryAppId = zapi.application.get(
        output="applicationId",
        hostids=[_hostId],
        search= {
            "name": ["Memory"]
        },
        startSearch="true"
    )
    return memoryAppId[0]["applicationid"]

# Subrutina que se encarga de crear el item para monitorizar la
#   información de la memoria
def createItemForMemoryMonitoring(_hostId, _interfaceId):
    memoryAppId = getMemoryApplicationId(_hostId)

    itemId = zapi.item.create(
        name= "Host memory utilization",
        key_= "vm.memory.size[free]",
        hostid= _hostId,
        type= 0,
        value_type= 3,
        interfaceid= _interfaceId,
        tags=[{
            "tag": "Client host total free memory"
        }],
        applications=[
            memoryAppId
        ],
        delay= "2m"
    );
    return itemId

# Subrutina que se encarga de obtener el id de la aplicación "Filesystems"
def getFilesystemsApplicationId(_hostId):
    filesystemsAppId = zapi.application.get(
        output="applicationId",
        hostids=[_hostId],
        search= {
            "name": ["Filesystems"]
        },
        startSearch="true"
    )
    return filesystemsAppId[0]["applicationid"]

# Subrutina que se encarga de crear el item para monitorizar la
#   información de los dispositivos de almacenamiento
def createItemForDiskSpaceMonitoring(_hostId, _interfaceId):
    filesystemsAppId = getFilesystemsApplicationId(_hostId)

    itemId = zapi.item.create(
        name= "Host disk space utilization",
        key_= "vfs.fs.size[/,pused]",
        hostid= _hostId,
        type= 0,
        value_type= 0,
        interfaceid= _interfaceId,
        tags=[{
            "tag": "Client host total disk usage of filesystem /"
        }],
        applications=[
            filesystemsAppId
        ],
        delay= "5m"
    );
    return itemId

# Subrutina que se encarga de crear el item para monitorizar la
#   información de las tarjetas de red
def createItemForNetworkCardMonitoring(_hostId, _interfaceId):
    networkAppId = getNetworkApplicationId(_hostId)

    itemId = zapi.item.create(
        name= "Host network card information",
        key_= "system.run[lshw -class network]",
        hostid= _hostId,
        type= 0,
        value_type= 4,
        interfaceid= _interfaceId,
        tags=[{
            "tag": "Client host full network card information"
        }],
        applications=[
            networkAppId
        ],
        delay= "1h"
    );
    return itemId

def assignItemsToAllMonitoredHosts():
    monitoredHosts = getServerMonitorizedHosts()

    for host in monitoredHosts:
        hostId = host["hostid"]
        interfaceId = getHostInterfaceId(hostId)

        resultItem1 = createItemForBandwidthMonitoring(hostId, interfaceId)

        if resultItem1:
            resultItem2 = createItemForClientHostOSInformationMonitoring(hostId, interfaceId)

            if resultItem2:
                resultItem3 = createItemForUsersInformationMonitoring(hostId, interfaceId)

                if resultItem3:
                    resultItem4 = createItemForCPUMonitoring(hostId, interfaceId)

                    if resultItem4:
                        resultItem5 = createItemForMemoryMonitoring(hostId, interfaceId)

                        if resultItem5:
                            resultItem6 = createItemForDiskSpaceMonitoring(hostId, interfaceId)

                            if resultItem6:
                                resultItem7 = createItemForNetworkCardMonitoring(hostId, interfaceId)

                                if not resultItem7:
                                    raise ErrorNetworkCardMonitoring
                            else:
                                raise ErrorDiskSpaceMonitoring
                        else:
                            raise ErrorMemoryMonitoring
                    else:
                        raise ErrorCPUMonitoring   
                else:
                    raise ErrorUsersInformationMonitoring   
            else:
                raise ErrorOSInformationMonitoring    
        else:
            raise ErrorBandwidthMonitoring

# Programa principal
def main():
    try:
        assignItemsToAllMonitoredHosts()
        print(Fore.GREEN, "\nItems have been created successfully.")
    except ErrorNetworkCardMonitoring:
        print(Fore.RED, "\nError: Item for bandwidth monitoring could not be created.")
    except ErrorDiskSpaceMonitoring:
        print(Fore.RED, "\nError: Item for disk space monitoring could not be created.")
    except ErrorMemoryMonitoring:
        print(Fore.RED, "\nError: Item for memory monitoring could not be created.")
    except ErrorCPUMonitoring:
        print(Fore.RED, "\nError: Item for cpu monitoring could not be created.")
    except ErrorUsersInformationMonitoring:
        print(Fore.RED, "\nError: Item for users monitoring could not be created.")
    except ErrorOSInformationMonitoring:
        print(Fore.RED, "\nError: Item for OS monitoring could not be created.")
    except ErrorBandwidthMonitoring:
        print(Fore.RED, "\nError: Item for bandwidth monitoring could not be created.")

if __name__ == "__main__":
    main()