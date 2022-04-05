## Install Plugins

```yum install -y gcc glibc glibc-common gd gd-devel make net-snmp openssl-devel 

useradd nagios  
passwd nagios 

cd /tmp 
wget https://nagios-plugins.org/download/nagios-plugins-2.3.3.tar.gz 

tar -xzvf nagios-plugins-2.3.3.tar.gz 
cd nagios-plugins-2.3.3 
./configure 
make 
make install 
chown nagios.nagios /usr/local/nagios 
chown -R nagios.nagios /usr/local/nagios/libexec


## Install NRPE Client
```cd /tmp 
wget --no-check-certificate -O nrpe.tar.gz https://github.com/NagiosEnterprises/nrpe/archive/nrpe-4.0.3.tar.gz 
tar xzf nrpe-4.0.3.tar.gz 
cd nrpe-4.0.3 
./configure 
make all 
make install-groups-users 
make install-plugin 
make install-daemon 
make install-config 
make install-init 

echo >> /etc/services 
echo '# Nagios services' >> /etc/services 
echo 'nrpe    5666/tcp' >> /etc/services 

systemctl enable nrpe.service 

firewall-cmd --zone=public --add-port=5666/tcp 
firewall-cmd --zone=public --add-port=5666/tcp --permanent 

sed -i '/^allowed_hosts=/s/$/,192.168.29.200/' /usr/local/nagios/etc/nrpe.cfg 
sed -i 's/^dont_blame_nrpe=.*/dont_blame_nrpe=1/g' /usr/local/nagios/etc/nrpe.cfg 

systemctl start nrpe

## Check NRPE status 

/usr/local/nagios/libexec/check_nrpe -H 127.0.0.1 
