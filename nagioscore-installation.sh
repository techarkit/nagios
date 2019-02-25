#!/bin/bash
#################################
# Author: Ankam Ravi Kumar
# Purpose: Nagios Core Installation
# Date: 21st Feb 2019
# NO WARRANTY
#################################
LOGFILE=/tmp/nagios-installation.log
echo "DATE: `date`" > $LOGFILE
echo "Nagios Core 4.x Installation Start" >> $LOGFILE
echo "Stopping firewalld" >> $LOGFILE
systemctl stop firewalld >> $LOGFILE
echo "Disable firewalld service" >> $LOGFILE
systemctl disable firewalld >> $LOGFILE

echo "Disable SELinux" >> $LOGFILE
cat /etc/selinux/config |grep SELINUX=e >> $LOGFILE
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
cat /etc/selinux/config |grep SELINUX=d >> $LOGFILE

echo "Installing prerequisites" >> $LOGFILE
yum install -y wget httpd php gcc glibc glibc-common gd gd-devel make net-snmp perl perl-devel openssl >> $LOGFILE

echo "Downloading Nagios Core Package..." >> $LOGFILE
cd
wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.4.3.tar.gz

echo "Creating Nagios User" >> $LOGFILE
useradd nagios
echo "Creating Group" >> $LOGFILE
groupadd nagcmd
echo "Adding nagios to group" >> $LOGFILE
usermod -a -G nagcmd nagios

echo "Nagios package compeling" >> $LOGFILE
tar -xvf nagios-4.4.3.tar.gz
cd nagios-4.4.3 >> $LOGFILE
./configure --with-command-group=nagcmd >> $LOGFILE
sleep 30
make all >> $LOGFILE
make install >> $LOGFILE
make install-init >> $LOGFILE
make install-config >> $LOGFILE
make install-commandmode >> $LOGFILE 
make install-webconf >> $LOGFILE

echo "Copying Evenhandler Files" >> $LOGFILE
cp -rvf contrib/eventhandlers/ /usr/local/nagios/libexec/
echo "chaning permissions of eventhandlers" >> $LOGFILE
chown -R nagios:nagcmd /usr/local/nagios/libexec/eventhandlers

echo "Generating Nagiosadmin password" >> $LOGFILE
htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin

echo "Starting Web Service" >> $LOGFILE
systemctl start httpd.service  >> $LOGFILE
systemctl enable httpd.service  >> $LOGFILE
systemctl status httpd.service >> $LOGFILE
echo "Starting Nagios Service" >> $LOGFILE
systemctl start nagios.service >> $LOGFILE
systemctl enable nagios.service >> $LOGFILE
systemctl status nagios.service >> $LOGFILE

echo "Downloading Nagios Plugins" >> $LOGFILE
cd
wget https://nagios-plugins.org/download/nagios-plugins-2.2.1.tar.gz >> $LOGFILE

echo "Extracting Nagios Plugins" >> $LOGFILE
tar -xvf nagios-plugins-2.2.1.tar.gz >> $LOGFILE

echo "Installing Nagios Plugins" >> $LOGFILE
cd nagios-plugins-2.2.1 >> $LOGFILE 
./configure --with-nagios-user=nagios --with-nagios-group=nagcmd  >> $LOGFILE
make  >> $LOGFILE
make install >> $LOGFILE

echo "Nagios core and Nagios Plugins installed successfully" >> $LOGFILE
echo "DATE: `date`" >> $LOGFILE

echo "Check Installation log for more details on installation process $LOGFILE"
echo "Reach aravi@server-computer.com for more details"
