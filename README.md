# Pydump

> Pydump is a wrapper over tcpdump utility which is a powerful command-line packet analyzer on UNIX/Linux platforms.

> With normal tcpdump command, as a system admin, you need to collect all the public IP addresses configured on the server and set the port you want with long arguments/flags.

> Using Pydump, you only need to pass the port numbers as arguments, rest will be taken care by Pydump.

#### prerequisites:
##### tcpdump command-line utility.

#### Install tcpdump on an rpm based machine.
```
# yum install tcpdump -y
```
#### Install tcpdump on a debian based machine.
```
# apt install tcpdump -y
```



#### Download and use it locally or on your server:
```
# wget https://raw.githubusercontent.com/vjwilson1987/Pydump/master/pydump.py
# chmod +x pydump.py
# ./pydump.py 80 443
```

#### Usage:

```
# ./pydump.py 80 443
```
#### Sample output:

```
# ./pydump.py 

No arguments passed

Usage:
	./pydump.py <port> <port>

Exiting...
```

```
# ./pydump.py 80

Total number of arguments passed:  1

Command to run:

		tcpdump -nn -tttt -A -i eth0 "(dst host 192.168.1.2 or dst host 192.168.1.3) and (dst port 80)" 

Proceed? Yes|yes|Y|y / No|no|N|n: n

Chose to exit. Goodbye
```

```
# ./pydump.py 80 443

Total number of arguments passed:  2

Command to run:

		tcpdump -nn -tttt -A -i eth0 "(dst 192.168.1.2 or dst host 192.168.1.3) and (dst port 80 or dst port 443)" 

Proceed? Yes|yes|Y|y / No|no|N|n: y
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
2022-03-04 15:34:46.115903 IP 45.x.x.x.64470 > 192.168.1.2.443: Flags [.], ack 4174720456, win 501, options [nop,nop,TS val 830943008 ecr 169058905], length 0
E..4..@.1...-s[..E.}....C.i...-......v.....
1./
..Y
2022-03-04 15:34:46.115969 IP 45.x.x.x.64470 > 192.168.1.2.443: Flags [F.], seq 0, ack 2, win 501, options [nop,nop,TS val 830943009 ecr 169058905], length 0
E..4..@.1...-s[..E.}....C.i...-......s.....
1./!
..Y
2022-03-04 15:34:46.912858 IP 45.x.x.x.35323 > 192.168.1.2.443: Flags [.], ack 822209606, win 1318, options [nop,nop,TS val 830943810 ecr 169059702], length 0
E..4..@.3.2.-s[..E.}.......@1..F...&.......
1.2B
..v
```


### Quick usage of the script
```
# python3 <(curl -s https://raw.githubusercontent.com/vjwilson1987/Pydump/master/pydump.py) 80 443
```


#### Pydump log file:
> By default it logs everything to a file named **tcpdump.log** which is created on the same path you run this script.
