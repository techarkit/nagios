### NagVis Installation Steps ###
```
yum install php php-pdo php-pdo_mysql php-fpm php-json rsync gcc g++ php-mbstring php-mysqlnd php-gd php-xml graphviz
wget http://www.nagvis.org/share/nagvis-1.9.18.tar.gz
tar -xvf nagvis-1.9.18.tar.gz
cd nagvis-1.9.18
./install.sh
```

```
Welcome	to NagVis Installer 1.9.18
This script is built to facilitate the NagVis installation and update
procedure for you. The installer has been tested on the following systems:
- Debian, since Etch (4.0)
- Ubuntu, since Hardy (8.04)
- SuSE Linux Enterprise Server 10 and 11

Similar distributions to the ones mentioned above should work as well.
That (hopefully) includes RedHat, Fedora, CentOS, OpenSuSE

If you experience any problems using these or other distributions, please
report that to the NagVis team.

Do you want to proceed? [y]: y
Starting installation of NagVis 1.9.18

Checking for tools 	
Using packet manager /usr/bin/rpm found 

Checking paths
Please enter the path to the nagios base directory [/usr/local/nagios]: 
nagios path /usr/local/nagios	found
Please enter the path to NagVis base [/usr/local/nagvis]: 

	 Checking prerequisites 	
 PHP 7.2
	PHP Module : gd                     found
	PHP	Module:	mbstring                found
	PHP	Module :	gettext compiled_in   found
	PHP	Module:	session compiled_in     found
	PHP Module : xml	php               found
	PHP Module : pdo                    found
 Apache mod_php I Graphviz 2.40
	Graphviz Module	dot 2.40.1          found
	Graphviz Module	neato 2.40.1        found
	Graphviz Module	twopi 2.40.1        found
	Graphviz Module	circo 2.40.1        found
	Graphviz Module	fdp 2.40.1          found
 WARNING: The SQLite package was not found	
      This may not be a problem if you installed it from source

	 Trying to detect Apache settings
 Please enter the web path to NagVis [/nagvis]:
```

```
Please enter the name of the web-server user [apache]: 
Please enter the name of the web-server group [apache] 
create Apache config file [y]:
NagVis home will be : /usr/local/nagvis
Owner of NagVis files will be: apache
Group of NagVis files will be: apache
```

```
Path to Apache config dir is : /etc/httpd/conf.d
Apache config will be created: yes
Installation mode: install
Do you really want to continue? [y]: y
```
- Username: admin
- Password: admin

```
systemctl restart httpd
systemctl restart nagios
```
http://server-ip/nagvis
