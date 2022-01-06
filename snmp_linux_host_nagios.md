Adding Linux server into Nagios monitoring using SNMP step by step procedure

- https://exchange.nagios.org/components/com_mtree/attachment.php?link_id=1608&cf_id=35

- tar -xvf check_snmp-1.4.tar.bz2
- cd check_snmp-1.4
- ./configure
- make all
- make install


```
./check_snmp_load.pl -H localhost -C techarkit -T netsc -w 90 -c 95
Output: CPU used 2.0% (<90) : OK

./check_snmp_storage.pl -H localhost -C techarkit -m /boot -r -w 90 -c 95
Output: /boot: 7%used(131MB/1952MB) (<90%) : OK

./check_snmp_mem.pl -H localhost -C techarkit -w 90,20 -c 95,30 -f
Output: Ram : 11%, Swap : 0% : ; OK | ram_used=405796;3463924;3656364;0;3848804 swap_used=0;1677721;2516581;0;8388604

check_snmp_storage.pl -C <community> -H <hostIP> -m "^Virtual Memory$"  -w <warn %> -c <crit %>

./check_snmp_process.pl -H localhost -C techarkit -n http -f -w 3,7 -c 0,8 -m 15,25 -u 10,20
Output: 5 processes matching http (> 3) (<= 7):OK, Mem : 13.5MB OK, CPU : 0% OK

./check_snmp_int.pl -H localhost -C techarkit -n ens33
Output: ens33:UP:1 UP: OK

./check_snmp_int.pl -H localhost -C techarkit -n ens33 -k -w 200,400 -c 500,600
Output:ens33:UP (0.1KBps/0.0KBps):1 UP: OK
```
