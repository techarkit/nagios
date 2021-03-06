## host_nagios_send_email.pl
- yum install perl-Mail-Sendmail rrdtool-perl perl-Digest-MD5 -y
- perl -MRRDs -le 'print q(ok!)'

## Nagios SNMP Trap installation and configuration guide
http://askaralikhan.blogspot.com/2010/12/receiving-snmp-traps-in-nagios.html


### Check_nt Commands Examples ###
- /usr/local/nagios/libexec/check_nt -H 192.168.48.200 -p 12489 -v CLIENTVERSION -s password

- snmpwalk -v 2c -c public 192.168.2.250

- /usr/local/nagios/libexec/check_nrpe -H 10.0.0.124

## Disable All hosts notifications under host group
`echo "[`date +%s`] DISABLE_HOSTGROUP_HOST_NOTIFICATIONS;linux-servers" > /usr/local/nagios/var/rw/nagios.cmd`

## Disable all the service notifications under hostgroup
`echo "[`date +%s`] DISABLE_HOSTGROUP_SVC_NOTIFICATIONS;linux-servers" > /usr/local/nagios/var/rw/nagios.cmd`

## Test HTML email from Nagios 4x ##
- ./nagios_send_host_mail.pl -v -t -r aravikumar48@gmail.com -f graph -u -l en
- ./nagios_send_host_mail.pl -v -t -r aravikumar48@gmail.com -f graph -u -l en

## Download Packges
`yumdownloader --downloadonly --downloaddir=/tmp perl-Mail-Sendmail rrdtool-perl perl-Digest-MD5`

## Dell iDrac Checks ##
```- /usr/local/nagios/libexec/check_idrac2 -H IDRACIP -c public -p -v2c -w MEM
- /usr/local/nagios/libexec/check_idrac2 -H IDRACIP -c public -p -v2c -w PS
- /usr/local/nagios/libexec/check_idrac2 -H IDRACIP -c public -p -v2c -w FAN
- /usr/local/nagios/libexec/check_idrac2 -H IDRACIP -c public -p -v2c -w FAN --fan-warn=4000,6000 --fan-crit=3000,7000
- /usr/local/nagios/libexec/check_idrac2 -H IDRACIP -c public -p -v2c -w VDISK
- /usr/local/nagios/libexec/check_idrac2 -H IDRACIP -c public -p -v2c -w DISK
- /usr/local/nagios/libexec/check_idrac2 -H IDRACIP -c public -p -v2c -w SENSOR
- /usr/local/nagios/libexec/check_idrac2 -H IDRACIP -c public -p -v2c -w PU
- /usr/local/nagios/libexec/check_idrac2 -H IDRACIP -c public -p -v2c -w BATTERY
- /usr/local/nagios/libexec/check_idrac2 -H IDRACIP -c public -p -v2c -w CPU
- /usr/local/nagios/libexec/check_idrac2 -H IDRACIP -c public -p -v2c -w SENSOR --temp-warn=29,61
- /usr/local/nagios/libexec/check_idrac2 -H IDRACIP -c public -p -v2c -w GLOBAL```
