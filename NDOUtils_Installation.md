```yum install mariadb*
systemctl start mariadb

## Setup MySQL/MariaSB Database Server ##
mysql_secure_installation

## Create Database and User ##
mysql -u root -p

CREATE DATABASE nagios DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'ndoutils'@'localhost' IDENTIFIED BY 'password';
GRANT USAGE ON *.* TO 'ndoutils'@'localhost' IDENTIFIED BY 'password' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0 ;
GRANT ALL PRIVILEGES ON nagios.* TO 'ndoutils'@'localhost' WITH GRANT OPTION ;
FLUSH PRIVILEGES;

## Change Kernel Parameters ##
cp /etc/sysctl.conf /opt/
sed -i '/msgmnb/d' /etc/sysctl.conf
sed -i '/msgmax/d' /etc/sysctl.conf
sed -i '/shmmax/d' /etc/sysctl.conf
sed -i '/shmall/d' /etc/sysctl.conf
printf "\n\nkernel.msgmnb = 131072000\n" >> /etc/sysctl.conf
printf "kernel.msgmax = 131072000\n" >> /etc/sysctl.conf
printf "kernel.shmmax = 4294967295\n" >> /etc/sysctl.conf
printf "kernel.shmall = 268435456\n" >> /etc/sysctl.conf
sysctl -e -p /etc/sysctl.conf


## Download NDOUtils ##
wget -O ndoutils.tar.gz https://github.com/NagiosEnterprises/ndoutils/releases/download/ndoutils-2.1.3/ndoutils-2.1.3.tar.gz

## Extract Package and Install ##
tar xvf ndoutils.tar.gz
cd ndoutils-2.1.3/

./configure
make all
make install
make install-config
make install-init

## Load Database Tables ##
cd db/
./installdb -u 'ndoutils' -p 'password' -h 'localhost' -d nagios


## Change config File ##
cd /usr/local/nagios/etc/
mv ndo2db.cfg-sample ndo2db.cfg
mv ndomod.cfg-sample ndomod.cfg
ed -i 's/^db_user=.*/db_user=ndoutils/g' /usr/local/nagios/etc/ndo2db.cfg
sed -i 's/^db_user=.*/db_user=ndoutils/g' /usr/local/nagios/etc/ndo2db.cfg
sed -i 's/^db_pass=.*/db_pass=password/g' /usr/local/nagios/etc/ndo2db.cfg

## Enable and Start Services ##
systemctl enable ndo2db.service
systemctl start ndo2db.service
cd /usr/local/nagios/etc/
vi nagios.cfg

#NDOUtils Broker Module Add this Line
broker_module=/usr/local/nagios/bin/ndomod.o config_file=/usr/local/nagios/etc/ndomod.cfg

systemctl restart nagios.service
systemctl status nagios.service
clear
grep ndo /usr/local/nagios/var/nagios.log
echo 'select * from nagios.nagios_logentries;' | mysql -u ndoutils -p'password'
systemctl start ndo2db.service
systemctl stop ndo2db.service
systemctl restart ndo2db.service
systemctl status ndo2db.service
