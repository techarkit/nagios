```vim /etc/yum.repos.d/pagerduty.repo
[pdagent]
name=PDAgent
baseurl=https://packages.pagerduty.com/pdagent/rpm
enabled=1
gpgcheck=1
gpgkey=https://packages.pagerduty.com/GPG-KEY-RPM-pagerduty

:wq (Save and Exit)


sudo yum install pdagent pdagent-integrations
cp /var/lib/pdagent/scripts/pdagent.service  /etc/systemd/system/pdagent.service
systemctl daemon-reload
systemctl enable pdagent.service
systemctl start pdagent.service
systemctl status pdagent.service.


## Integration with Nagios ##
yum install perl-JSON perl-CGI perl-libwww-perl
wget https://raw.githubusercontent.com/PagerDuty/pdagent-integrations/master/pagerduty_nagios.cfg
mv pagerduty_nagios.cfg /usr/local/nagios/etc/servers/

vim /usr/local/nagios/etc/objects/contacts.cfg
define contactgroup{
contactgroup_name admins 
alias Nagios Administrators
members root,pagerduty ; Add pagerduty here
}

service nagios restart


wget https://raw.githubusercontent.com/mdcollins05/pd-nag-connector/master/pagerduty.cgi
mv pagerduty.cgi /usr/local/nagios/sbin/
chmod +x /usr/local/nagios/sbin/pagerduty.cgi```
