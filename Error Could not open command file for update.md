```
Error: Could not open command file '/usr/local/nagios/var/rw/nagios.cmd' for update!
The permissions on the external command file and/or directory may be incorrect. Read the FAQs on how to setup proper permissions.
An error occurred while attempting to commit your command for processing.

Return from whence you came
```

## Change file permissions as show below
```
chown nagios:nagcmd /usr/local/nagios/var/rw
chmod g+rwx /usr/local/nagios/var/rw
chmod g+s /usr/local/nagios/var/rw
```
