## host_nagios_send_email.pl
yum install perl-Mail-Sendmail rrdtool-perl perl-Digest-MD5 -y
perl -MRRDs -le 'print q(ok!)'

## Nagios SNMP Trap installation and configuration guide
http://askaralikhan.blogspot.com/2010/12/receiving-snmp-traps-in-nagios.html


### Check_nt Commands Examples ###
./check_nt -H 10.144.132.169 -p 12489 -v CLIENTVERSION -s password


snmpwalk -v 2c -c public 192.168.2.250

/usr/local/nagios/libexec/check_nrpe -H 10.0.0.124

## Disable All hosts notifications under host group
echo "[`date +%s`] DISABLE_HOSTGROUP_HOST_NOTIFICATIONS;linux-servers" > /usr/local/nagios/var/rw/nagios.cmd

## Disable all the service notifications under hostgroup
echo "[`date +%s`] DISABLE_HOSTGROUP_SVC_NOTIFICATIONS;linux-servers" > /usr/local/nagios/var/rw/nagios.cmd

## Test HTML email from Nagios 4x ##
./nagios_send_host_mail.pl -v -t -r aravikumar48@gmail.com -f graph -u -l en
./nagios_send_host_mail.pl -v -t -r aravikumar48@gmail.com -f graph -u -l en

## Download Packges
yumdownloader --downloadonly --downloaddir=/tmp perl-Mail-Sendmail rrdtool-perl perl-Digest-MD5
