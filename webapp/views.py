
import socket
from django.http import HttpResponse
import sys


#from general import *
sys.path.append("./webapp/")
from networking.ethernet import Ethernet
from networking.ipv4 import IPv4
from networking.icmp import ICMP
from networking.tcp import TCP
from networking.udp import UDP
from networking.pcap import Pcap
from networking.http import HTTP


pcap = Pcap('Test.pcap')
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))




#print('Ethernet Frame:')
#print('Destination: {}, Source: {}, Protocol: {}'.format(eth.dest_mac, eth.src_mac, eth.proto))

 #if eth.proto == 8:
           # ipv4 = IPv4(eth.data)
           # print('IPv4 Packet:')
           #   print('Version: {}, Header Length: {}, TTL: {},'.format(ipv4.version, ipv4.header_length, ipv4.ttl))
           #   print('Protocol: {}, Source: {}, Target: {}'.format(ipv4.proto, ipv4.src, ipv4.target))



def index(request):
    answer = []
    for raw_data in range(5):
        raw_data , addr = s.recvfrom(65565)
        pcap.write(raw_data)
        eth = Ethernet(raw_data)
        ipv4 = IPv4(eth.data)
        icmp = ICMP ( ipv4.data )
        tcp = TCP (ipv4.data)
        udp = UDP (ipv4.data)
       # pcap =Pcap(pcap.data)

        answer.extend ( [
                str('Time Stamp:'.format()),
                str('Destination MAC: {}, Source MAC: {}, Protocol: {}'.format ( eth.dest_mac ,eth.src_mac, eth.proto)),
                str('IP Version: {}, IP Header Length: {}, TTL: {},'.format(ipv4.version, ipv4.header_length, ipv4.ttl)),
                str('Protocol: {}, Source IP: {}, Target IP: {}'.format(ipv4.proto, ipv4.src, ipv4.target)),
                str('Source Port: {}, Destination Port: {}'.format(tcp.src_port, tcp.dest_port)),
                str('Source Port: {}, Destination Port: {}, Length: {}'.format(udp.src_port, udp.dest_port, udp.size))
        ])

        answer.append (" ")

    return HttpResponse("<br>".join(answer))


