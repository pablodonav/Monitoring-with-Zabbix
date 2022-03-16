# Zabbix

Direcciones IP:

- 155.210.71.95

- 155.210.71.183

- 155.210.71.173


# Instalación del servidor de Zabbix

En este apartado, se va a proceder a explicar como se ha instalado el servidor de Zabbix. Se va a comenzar por instalar LAMP.

### INSTALACIÓN DE LAMP

Para ello, se ha comenzado con la instalación de Apache en su versión 2.

`sudo apt update` </br>
`sudo apt-get install apache2` </br>
`sudo service apache2 status` </br>
 
 Una vez instalado Apache, se ha procedido a instalar MariaDB:
 
 `sudo apt-get install mariadb-server mariadb-client` </br>
 `sudo service mysql status` </br>
 
 Y se ha configurado MariaDB ejecutando el siguiente ssh:
 
 `sudo /usr/bin/mysql_secure_installation` </br>
 
 Del formulario que aparece, debe realizarse las siguientes operaciones: </br>
  > 1. En el primer paso nos preguntará por la contraseña de “root” para MariaDB, pulsaremos la tecla enter ya que no hay contraseña definida. </br>
  > 2. El siguiente paso nos preguntará si queremos asignar una contraseña para el usuario “root”. Es recomendable usar contraseña. </br>
  > 3. El siguiente paso nos preguntará si queremos eliminar usuario anónimo, aquí indicaremos que Sí queremos borrar los datos. </br>
  > 4. El siguiente paso nos preguntará si queremos desactivar que el usuario “root” se conecte remotamente, aquí indicaremos que Sí queremos desactivar acceso remoto para usuario “root”. </br>
  > 5. El siguiente paso nos preguntará si queremos eliminar la base de datos “test”, aquí indicaremos que Sí queremos borrar las base de datos “test”. </br>
  > 6. El siguiente paso nos preguntará si queremos recargar privilegios, aquí indicaremos que Sí. </br>

Finalmente, se ha procedido a instalar PHP:

`sudo apt install php php-cli php-mysql libapache2-mod-php` </br>
`sudo service apache2 restart` </br>

### INSTALACIÓN DEL SERVIDOR DE ZABBIX
