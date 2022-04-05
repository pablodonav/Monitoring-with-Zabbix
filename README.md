# Zabbix

Direcciones IP:

- 155.210.71.183 -> CLIENTE 1 ZABBIX
-  alumno - cliente1admin2

- 155.210.71.95 -> CLIENTE 2 ZABBIX
-  alumno - cliente2admin2

- 155.210.71.173  -> SERVIDOR 1 ZABBIX
-  alumno - server1admin2

- 155.210.71.186  -> SERVIDOR 2 ZABBIX
-  alumno - server2admin2


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
  > 2. El siguiente paso nos preguntará si queremos asignar una contraseña para el usuario “root”. Es recomendable usar contraseña. (Servidor 1 sin contraseña y            Servidor 2 con contraseña root). </br>
  > 3. El siguiente paso nos preguntará si queremos eliminar usuario anónimo, aquí indicaremos que Sí queremos borrar los datos. </br>
  > 4. El siguiente paso nos preguntará si queremos desactivar que el usuario “root” se conecte remotamente, aquí indicaremos que Sí queremos desactivar acceso remoto para usuario “root”. </br>
  > 5. El siguiente paso nos preguntará si queremos eliminar la base de datos “test”, aquí indicaremos que Sí queremos borrar las base de datos “test”. </br>
  > 6. El siguiente paso nos preguntará si queremos recargar privilegios, aquí indicaremos que Sí. </br>

Finalmente, se ha procedido a instalar PHP:

`sudo apt install php php-cli php-mysql libapache2-mod-php` </br>
`sudo service apache2 restart` </br>

### INSTALACIÓN DEL SERVIDOR DE ZABBIX

Una vez instalado LAMP, se ha procedido a instalar el servidor de Zabbix:

`sudo dpkg -r zabbix-release` </br>
`sudo wget https://repo.zabbix.com/zabbix/3.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.4-1+bionic_all.deb` </br>
`sudo dpkg -i zabbix-release_3.4-1+bionic_all.deb` </br>
`sudo apt update` </br>
`apt install zabbix-server-mysql zabbix-frontend-php` </br>
A continuación, se ha procedido a crear e importar la base de datos. El usuario creado tiene como nombre: "zabbix" y contraseña: "TestZabbix".

`sudo mysql -u root` </br>
` > MariaDB [(none)]> create database zabbix character set utf8 collate utf8_bin;` </br>
` > MariaDB [(none)]> grant all privileges on zabbix.* to zabbix@localhost identified by 'TestZabbix';` </br>
` > MariaDB [(none)]> quit;` </br>

Se importa la base de datos:

`sudo zcat /usr/share/doc/zabbix-server-mysql/create.sql.gz | mysql -uzabbix -p zabbix` </br>

Una vez importada, se ha procedido a configurar la Base de Datos de Zabbix. Para ello, se va a editar el siguiente fichero:

`sudo vim /etc/zabbix/zabbix_server.conf`</br>

Donde se añadirán los siguientes datos:

`DBHost=localhost`</br>
`DBName=zabbix`</br>
`DBUser=zabbix`</br>
`DBPassword=TestZabbix`</br>

Y se arrancará el servidor Zabbix:

`sudo service zabbix-server start` </br>
`sudo update-rc.d zabbix-server enable` </br>

A continuación, se ha configurado PHP. Para ello, se va a proceder a modificar el siguiente fichero: </br>
 - Servidor 1: `sudo vim /etc/php/7.0/apache2/php.ini` </br>
 - Servidor 2: `sudo vim /etc/php/7.2/apache2/php.ini` </br>

Donde, se han añadido los siguientes campos:

`post_max_size = 16M` </br>
`max_execution_time = 300` </br>
`max_input_time = 300` </br>
`date.timezone = Europe/Madrid` </br>

Y finalmente, se ha reiniciado el Apache:

`sudo service apache2 restart` </br>

Una vez está funcionando todo correctamente, se ha procedido a configurar Zabbix accediendo a la dirección http://155.210.71.173/zabbix/setup.php, donde habrá que especificar los datos de acceso a la Base de Datos y la IP privada del servidor Zabbix.

Una vez configurado correctamente, se podrá acceder al sistema mediante las credenciales que por defecto son usuario: "Admin" y contraseña: "zabbix", aunque la contraseña ha sido modificada por seguridad a "admin2".

### INSTALACIÓN DEL AGENTE ZABBIX

A continuación, se ha procedido a instalar y configurar el agente Zabbix para llevar a cabo nuestra propia gestión del servidor. Para ello:

`sudo apt-get install zabbix-agent` </br>

Y se procederá al editar el siguiente fichero:

`sudo vim /etc/zabbix/zabbix_agentd.conf` </br>

**Para los host servidores se modificarán las siguientes variables :**

 - Servidor 1 </br>
   `Server=127.0.0.1, 155.210.71.173, 155.210.71.186 #IP Privada de nuestro servidor Zabbix` </br>
   `ServerActive=127.0.0.1, 155.210.71.173, 155.210.71.186` </br>
   `Hostname=Zabbix server 1` </br>
   
 - Servidor 2 </br>
   `Server=127.0.0.1, 155.210.71.186, 155.210.71.173  #IP Privada de nuestro servidor Zabbix` </br>
   `ServerActive=127.0.0.1, 155.210.71.186, 155.210.71.173` </br>
   `Hostname=Zabbix server 2` </br>
   
**Para los host clientes se modificarán las siguientes variables :**
   
 - Host Cliente 1 </br>
   `Server=127.0.0.1, 155.210.71.186, 155.210.71.183, 155.210.71.173 #IP Privada de nuestro servidor Zabbix` </br>
   `ServerActive=127.0.0.1, 155.210.71.186, 155.210.71.183, 155.210.71.173` </br>
   `Hostname=Host 1` </br>
   
  - Host Cliente 2 </br>
   `Server=127.0.0.1, 155.210.71.173, 155.210.71.95, 155.210.71.186 #IP Privada de nuestro servidor Zabbix` </br>
   `ServerActive=127.0.0.1, 155.210.71.173, 155.210.71.95, 155.210.71.186` </br>
   `Hostname=Host 2` </br>

Ahora, ya se puede arrancar el agente Zabbix:

`sudo update-rc.d zabbix-agent enable` </br>
`sudo service zabbix-agent start` </br>

En el caso del servidor tambien se deberá restaurar el apache:

`sudo service apache2 restart` </br>

### CAMBIO DEL IDIOMA

Para llevar a cabo el cambio de idioma, se ha procedido a instalar el paquete en castellano:

`sudo vim /usr/share/zabbix/include/locales.inc.php` </br>

y se ha modificado el campo 

`'es_ES' => ['name' => _('Spanish (es_ES)'), 'display' => false ],` </br>

por el siguiente:

`'es_ES' => ['name' => _('Spanish (es_ES)'), 'display' => true],` </br>

Finalmente, se ha reiniciado el servicio de apache y se ha comprobado su correcto funcionamiento:

`sudo service apache2 restart` </br>

---

Asignación de ejercicios:
- Caso de uso 1: Pablo
- Caso de uso 2: Adnana
- Caso de uso 3: Diego
- Caso de uso 4: Pablo
- Caso de uso 5: Adnana
- Requisito de Usuario 1: Diego
- Requisito de Usuario 2: Pablo
- Requisito de Usuario 3: Adnana
- Requisito de Usuario 4: Diego
- Requisito de Usuario 5: Pablo
- Requisito de Usuario 6: Adnana
- Requisito de Servidor 1: Diego
- Requisito de Servidor 2: Pablo
- Requisito de Servidor 3: Adnana
- Requisito de Servidor 4: Diego
- Requisito de Servidor 5: Pablo
- Requisito de Servidor 6: Adnana
- Requisito de Servidor 7: Diego
- Requisito de Servidor 8: Pablo
- Requisito de Servidor 9: Adnana
- Requisito de Servidor 10: Diego
- Requisito de Restricción 1: Pablo
- Requisito de Restricción 2: Adnana
