import socket
from django.http import HttpResponse
import sys
import time
import struct

# from general import *
sys.path.append ( "./webapp/" )
from networking.ethernet import Ethernet
from networking.ipv4 import IPv4
from networking.icmp import ICMP
from networking.tcp import TCP
from networking.udp import UDP
from networking.pcap import Pcap
from networking.http import HTTP

pcap = Pcap ( 'Test.pcap' )
s = socket.socket ( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs ( 3 ) )


def index(request):
    answer = ''

    answer.append ( str (
        '<head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}</style></head><body><table><tr><th>Time Stamp</th><th>Destination MAC</th><th>Source MAC</th><th>Protocol</th><th>IP Version</th><th>IP Header Length</th><th>TTL</th><th>Protocol</th><th>Source IP</th><th>Target IP</th><th>Source Port</th><th>Destination Port</th><th>Length</th></tr>' ) )
    for raw_data in range ( 5 ):
        raw_data , addr = s.recvfrom ( 65565 )
        pcap.write ( raw_data )
        unpacked = struct.unpack ( '@ I H H i I I I I I I I' , raw_data[:40] )
        timestamp = time.strftime ( '%Y-%m-%d %H:%M:%S' , time.localtime ( unpacked ) )
        eth = Ethernet ( raw_data )
        ipv4 = IPv4 ( eth.data )
        icmp = ICMP ( ipv4.data )
        tcp = TCP ( ipv4.data )
        udp = UDP ( ipv4.data )

        answer.append ( str (
            '<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>'.format (
                timestamp , eth.dest_mac , eth.src_mac , eth.proto , ipv4.version , ipv4.header_length , ipv4.ttl ,
                ipv4.proto , ipv4.src , ipv4.target , tcp.src_port , tcp.dest_port , udp.src_port , udp.dest_port ,
                udp.size ) ) )

    answer.append ( str ( '</table></body>' ) )

    return HttpResponse ( answer )
