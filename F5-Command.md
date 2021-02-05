## BIG-IP F5 CLI Commands Cheatsheet


### [+] Show arp table

```tmsh show /net arp all```  

```
-------------------------------------------------------------------------------------------------
Net::Arp
Name           Address        HWaddress          Vlan                     Expire-in-sec  Status
-------------------------------------------------------------------------------------------------
10.10.220.200  10.10.220.200  00:0c:29:67:f5:aa  /Common/waftest          244            resolved
172.16.34.254  172.16.34.254  90:6c:ac:50:fe:cf  /Common/Vlan10_untagged  123            resolved

-------------------------------------------------------------------------------------------------
```


### [+] Create External data-group from http into iRules > Data Group List 
```tmsh create ltm data-group external new-ext-dg source-path http://10.212.134.3:8080/ext_string_data-group.txt type string```

### [+] Create External data-group from http into File Management > Data Group File List
```tmsh create sys file data-group ext-dg-test separator ":=" source-path http://10.212.134.3:8080/ext_string_data-group.txt type string```

### [+] Modify External data-group from http server. Auto it with cron
```modify ltm data-group external new-ext-dg source-path http://10.212.134.3:8080/ext_string_data-group.txt```

### [+] Grep connections from /sys
```tmsh show /sys connection | grep 10.212.134.3```
 
### [+] Delete connection
```delete /sys connection ss-server-addr node-ip ss-server-port node-port```

### [+] List deamons
```list /sys daemon-ha all-properties```

### [+] Show db variables
```show running-config /sys db all-properties```

### [+] Save SCF file from config
```save /sys config file my.config.scf tar-file my.config.tar```

### [+] Load SCF file 
```load /sys config file my.config.scf tar-file my.config.tar```

### [+] Show Fail-Over
```show /sys failover```

### [+] Force unit offline
```run /sys failover offline```

### [+] Release offline to go either standby or active
```run /sys failover online	 ```

### [+] Standby
```run /sys failover standby```

### [+] Show all ha-status
```show /sys ha-status all-properties```

### [+] Show ha-group details
```show /sys ha-group detail```

### [+] Show all interfaces
```show /net interface all-properties```

### [+] Create management route
```tmsh create /sys management-route default gateway 192.168.0.1```  


### [+] List all node monitors
```list ltm node monitor```  

### [+] List all node with statistics
```show /ltm node```  


### [+] Modify ntp server 
```modify sys ntp servers add { 10.10.10.10 }```  

### [+] List Persistences
```
tmsh show ltm persistence persist-records ?
Options:
  all-properties  Display all properties for the specified items
  save-to-file    Output from the command is saved to the specified file. This file is placed in
                  /shared. This allows to write a file larger than 2GB.
  |               Route command output to a filter
Properties:
  "{"             Optional delimiter
  client-addr     Specifies the client address for the persistence record.
  key             Specifies the key to look up in the persist table. It is based on the persist mode.
  mode            Specifies the type of persistence.
  node-addr       Specifies the address of the node with which the client session remains persistent.
  node-port       Specifies the port of the node with which the client session remains persistent.
  pool            Specifies the name of the pool with which the client session remains persistent.
  virtual         Specifies the name of the virtual with which the client session remains persistent. 
```  



### [+] Show hardware info
```tmsh show /sys hardware```
```
Sys::Hardware
Chassis Information
  Maximum MAC Count  1
  Registration Key   -

Hardware Version Information
  Name        HD1
  Type        physical-disk
  Model       Virtual disk
  Parameters  --                --
              SerialNumber      VMware-sda
              Size              142.00G
              Firmware Version  1.0
              Media Type        HDD

  Name        HD2
  Type        physical-disk
  Model       Virtual disk
  Parameters  --                --
              SerialNumber      VMware-sdb
              Size              20.00G
              Firmware Version  1.0
              Media Type        HDD


Hardware Version Information
  Name        cpus
  Type        base-board
  Model       Intel(R) Xeon(R) CPU           E5504  @ 2.00GHz
  Parameters  --            --
              cache size    4096 KB
              cores         2  (physical:2)
              cpu MHz       1995.000
              cpu sockets   2
              cpu stepping  5


Platform
  Name  BIG-IP Virtual Edition
  BIOS Revision
  Base MAC       00:0c:29:0a:1b:64
  Hypervisor     VMware Virtual Platform
  Cloud

System Information
  Type                       Z100
  Chassis Serial             564da3e7-7b6f-e947-53c7fb0a1b64
  Level 200/400 Part
  Switchboard Serial
  Switchboard Part Revision
  Host Board Serial
  Host Board Part Revision
```






