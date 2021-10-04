#### SCAPY

##### 构建IP报文

```python
import scapy.all as sca
a = sca.IP(dst = "www.google.com/30")
print(a)        
#<IP  dst=Net('www.google.com/30') |>
print([i for i in a])      
#[<IP  dst=199.59.148.96 |>, <IP  dst=199.59.148.97 |>, <IP  dst=199.59.148.98 |>, <IP  dst=199.59.148.99 |>]
```

------

使用”/”堆加层次，基于OSI模型：

构建以太网/IP/TCP报文

```python
>>>sca.Ether(dst="ff:ff:ff:ff:ff:ff")/sca.IP(dst=["ketchup.com", "mayo.com"], ttl=(1,9))/sca.UDP()

<Ether  dst=ff:ff:ff:ff:ff:ff type=0x800 |<IP  frag=0 ttl=(1, 9) proto=udp dst=[Net('ketchup.com'), Net('mayo.com')] |<UDP  |>>>
```

##### 堆叠报文

```python
>>> sca.IP()
<IP |>

>>> sca.IP()/sca.TCP()
<IP frag=0 proto=TCP |<TCP |>>

>>> sca.Ether()/sca.IP()/sca.TCP()
<Ether type=0x800 |<IP frag=0 proto=TCP |<TCP |>>>

>>> sca.IP()/sca.TCP()/"GET / HTTP/1.0\r\n\r\n"
<IP frag=0 proto=TCP |<TCP |<Raw load='GET / HTTP/1.0\r\n\r\n' |>>>

>>> sca.Ether()/sca.IP()/sca.IP()/sca.UDP()
<Ether type=0x800 |<IP frag=0 proto=IP |<IP frag=0 proto=UDP |<UDP |>>>>

>>> sca.IP(proto=55)/sca.TCP()
<IP frag=0 proto=55 |<TCP |>>
```

IP对象都可以通过点操作符访问对象

查询是否包含指定的协议层次或获取指定层次 getlayer(sca.TCP) haslayer(sca.TCP)

------

##### 操作报文

- Hexdump

```python
a = sca.IP()/sca.TCP()/"GET / HTTP/1.0\r\n\r\n"
sca.hexdump(a)
>>> sca.hexdump(a)
0000   45 00 00 3A 00 01 00 00  40 06 7C BB 7F 00 00 01   E..:....@.|.....
0010   7F 00 00 01 00 14 00 50  00 00 00 00 00 00 00 00   .......P........
0020   50 02 20 00 B2 CA 00 00  47 45 54 20 2F 20 48 54   P. .....GET / HT
0030   54 50 2F 31 2E 30 0D 0A  0D 0A                     TP/1.0....
```

- str()

```TEXT
b = str(a)
c = sca.Ether(b.encode())

#<Ether  dst=62:27:45:5c:78:30 src=30:5c:78:30:30:3a type=0x5c78 |<Raw  load="00\\x01\\x00\\x00@\\x06|\\xbb\\x7f\\x00\\x00\\x01\\x7f\\x00\\x00\\x01\\x00\\x14\\x00P\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00P\\x02 \\x00\\xb2\\xca\\x00\\x00GET / HTTP/1.0\\r\\n\\r\\n'" |>>
```

Scapy还是应该用Python2写，Python3默认字节流不是很兼容

------

##### 读取Pcap文件

Pcap是一些工具如Wireshark，Aircrack-ng抓到的数据包

```python
a = rdpcap("test.cap")
print(a)
#<test.cap: UDP:518 TCP:231 ICMP:0 Other:0>
```

------

创建一组数据包

```python
a = sca.IP(ttl = [1,2,(3,5)])
print([i for i in a])
#[<IP  ttl=1 |>, <IP  ttl=2 |>, <IP  ttl=3 |>, <IP  ttl=4 |>, <IP  ttl=5 |>]
```

##### 堆叠数据包

```python
a = sca.IP(dst = "www.google.com/30")
b = sca.TCP(dport = [80,443])
print([i for i in a/b])
#[<IP  frag=0 proto=tcp dst=31.13.66.20 |<TCP  dport=http |>>, <IP  frag=0 proto=tcp dst=31.13.66.20 |<TCP  dport=https |>>, <IP  frag=0 proto=tcp dst=31.13.66.21 |<TCP  dport=http |>>, <IP  frag=0 proto=tcp dst=31.13.66.21 |<TCP  dport=https |>>, <IP  frag=0 proto=tcp dst=31.13.66.22 |<TCP  dport=http |>>, <IP  frag=0 proto=tcp dst=31.13.66.22 |<TCP  dport=https |>>, <IP  frag=0 proto=tcp dst=31.13.66.23 |<TCP  dport=http |>>, <IP  frag=0 proto=tcp dst=31.13.66.23 |<TCP  dport=https |>>]
```

| 方法            | 用途                                  |
| --------------- | ------------------------------------- |
| summary()       | 显示一个关于每个数据包的摘要列表      |
| nsummary()      | 同上，但规定了数据包数量              |
| conversations() | 显示一个会话图表                      |
| show()          | 显示首选表示（通常用nsummary()）      |
| filter()        | 返回一个lambda过滤后的数据包列表      |
| hexdump()       | 返回所有数据包的一个hexdump           |
| hexraw()        | 返回所以数据包Raw layer的hexdump      |
| padding()       | 返回一个带填充的数据包的hexdump       |
| nzpadding()     | 返回一个具有非零填充的数据包的hexdump |
| plot()          | 规划一个应用到数据包列表的lambda函数  |
| make table()    | 根据lambda函数来显示表格              |

------

##### 发送数据包

send()函数会在第三层发送数据包，sendp()会在第二层

```python
>>> sca.send(sca.IP(dst="1.2.3.4")/sca.ICMP())
.
Sent 1 packets.
>>> sca.sendp(sca.Ether()/sca.IP(dst="1.2.3.4",ttl=(1,4)), iface="eth1")
....
Sent 4 packets.
```

------

Fuzz()函数，软件测试，漏洞挖掘经常用到

```python
>>> sca.send(sca.IP(dst="www.baidu.com")/sca.fuzz(sca.UDP()))
.
Sent 1 packets.
```

------

##### 发送和接收数据包

sr()函数用来发送数据包和接收应答。该函数返回一对数据包及其应答，还有无应答的数据包。sr1()函数用来返回一个应答数据包，以上发送的数据包必须是第3层报文（IP，ARP等）。

srp()则是使用第2层报文（以太网，802.3等）。

```TEXT
>>> r = sca.sr(sca.IP(dst="www.baidu.com")/sca.ICMP())
Begin emission:
Finished to send 1 packets.
...*
Received 4 packets, got 1 answers, remaining 0 packets
>>> r
(<Results: TCP:0 UDP:0 ICMP:1 Other:0>, <Unanswered: TCP:0 UDP:0 ICMP:0 Other:0>)
>>> r[0].show()
0000 IP / ICMP 192.168.1.101 > 111.13.100.92 echo-request 0 ==> IP / ICMP 111.13.100.92 > 192.168.1.101 echo-reply 0 / Padding
```

##### 发送SYN握手包

```python
>>>sr1(IP(dst="72.14.207.99")/TCP(dport=80,flags="S"))
Begin emission:
.Finished to send 1 packets.
*
Received 2 packets, got 1 answers, remaining 0 packets
<IP  version=4L ihl=5L tos=0x20 len=44 id=33529 flags= frag=0L ttl=244
proto=TCP chksum=0x6a34 src=72.14.207.99 dst=192.168.1.100 options=// |
<TCP  sport=www dport=ftp-data seq=2487238601L ack=1 dataofs=6L reserved=0L
flags=SA window=8190 chksum=0xcdc7 urgptr=0 options=[('MSS', 536)] |
<Padding  load='V\xf7' |>>>
```

##### TCP Tracert 实现Dos下Tracert指令功能

```python
>>>ans,unans=sca.sr(sca.IP(dst="www.baidu.com", ttl=(4,25),id=sca.RandShort())/sca.TCP(flags=0x2))
for snd,rcv in ans:
    print(snd.ttl, rcv.src, isinstance(rcv.payload, sca.TCP))
'''
4 111.13.100.92 True
5 111.13.100.92 True
6 111.13.100.92 True
7 111.13.100.92 True
8 111.13.100.92 True
9 111.13.100.92 True
10 111.13.100.92 True
11 111.13.100.92 True
12 111.13.100.92 True
13 111.13.100.92 True
14 111.13.100.92 True
15 111.13.100.92 True
'''
```

------

##### 嗅探

```python
sca.sniff(filter:str,count:int,iface:str,prn:func)
```

**sniff的prn为回调函数，每抓到一个符合过滤器规则的包就以其为参数传入执行一次prn函数，通常用lambda写prn**

```python
#demo
a = sca.sniff(filter="host 127.0.0.1 and icmp",iface="wlan0",count = 10,prn=lambda x:x.show())
a.summary()
```

控制输出信息，使用sprintf()方法：

```python
a = sniff(prn=lambda x:x.sprintf("{IP:%IP.src% -> %IP.dst%\n}{Raw:%Raw.load%\n}"))
```

嗅探的filter，类似于wireshark的filter规则：

```python
a=sniff(filter="tcp and ( port 25 or port 110 )",prn=lambda x: x.sprintf("%IP.src%:%TCP.sport% -> %IP.dst%:%TCP.dport%  %2s,TCP.flags% : %TCP.payload%"))
```

##### 循环发送数据包

```python
srloop(IP(dst="www.google.com/30")/TCP())
```

------

##### 数据包的读写

```python
使用wrpcap()和rdpcap()函数 `wrpcap("a.cap",a)`
```

------

##### 更快的traceroute

```python
sca.traceroute(["www.google.com"],maxttl=20)
```

------

##### TCP扫描

```python
ans,unans = sca.sr(sca.IP(dst="www.baidu.org")/sca.TCP(dport=[80,666],flags="A"))
for s,r in ans:
    if s[TCP].dport == r[TCP].sport:
        print(str(s[TCP].dport) + " is unfiltered")
```

##### Xmax Scan

```python
ans,unans = sca.sr(sca.IP(dst="192.168.1.1")/sca.TCP(dport=666,flags="FPU") )
```

Arp数据包，通过广播arp包发现内网主机

```python
ans,unans=sca.srp(sca.Ether(dst="ff:ff:ff:ff:ff:ff")/sca.ARP(pdst="192.168.1.0/24"),timeout=2)
ans.summary(lambda (s,r): r.sprintf("%Ether.src% %ARP.psrc%") )

#功能相同的Built-in函数
sca.arping("192.168.1.*")
```

##### ICMP Ping

```python
ans,unans=sca.sr(sca.IP(dst="192.168.1.1-254")/sca.ICMP())
ans.summary(lambda (s,r): r.sprintf("%IP.src% is alive") )
```

##### TCP Ping

```python
ans,unans=sca.sr(sca.IP(dst="192.168.1.*")/sca.TCP(dport=80,flags="S"))
ans.summary(lambda(s,r) : r.sprintf("%IP.src% is alive"))
```

##### UDP Ping

```python
#选极可能关闭的端口，让存活主机产生ICMP Port unreachable error
ans,unans=sca.sr(sca.IP(dst="192.168.*.1-10")/sca.UDP(dport=0))
ans.summary( lambda(s,r) : r.sprintf("%IP.src% is alive") )
```

------

