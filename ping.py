#!/usr/bin/python3
#encode=utf-8

import socket
import struct

import time


def gen_data(size):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    res = ''
    for i in range(size):
        res += alphabet[i % len(alphabet)]

    return bytes(res, 'utf-8')


def ping(size, q, dest_ip, src_port, dest_port):    
    sock_out = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_RAW, proto=socket.IPPROTO_UDP)
    sock_in = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_RAW, proto=socket.IPPROTO_ICMP)

    ip_hdr_size = 20
    udp_hdr_size = 8
    icmp_hdr_size = 8

    payload_size = size - udp_hdr_size

    for i in range(a):
        payload = gen_data(payload_size)
        length = 8 + payload_size
        checksum = 0  # 3 is not the right checksum
        header_bad_checksum = struct.pack('!4H', src_port, dest_port, length, checksum)
        s = time.time()
        sock_out.sendto(header_bad_checksum + payload, (dest_ip, 4567))
        rec_pkg = sock_in.recv(ip_hdr_size + icmp_hdr_size)
        print(f'{size} bytes sent to {dest_ip}, recieved reply in {round((time.time() - s)*1000, 2)}ms, \
            code {rec_pkg[ip_hdr_size]}, type {rec_pkg[ip_hdr_size + 1]}')
        print('-'*25)


if __name__ == '__main__':
    from argparse import ArgumentParser

    p = ArgumentParser()
    p.add_argument('--ip', type=str, default='108.177.14.138')
    p.add_argument('--dest-port', type=int, default=4566)
    p.add_argument('--port', type=int, default=33434)
    p.add_argument('-s', type=int, default=8)
    p.add_argument('-a', type=int, default=3)

    a = p.parse_args()

    # ip.addr==192.168.30.71 and (udp or icmp) and not (quic or snmp or dns or ntp or mdns) and not ip.addr==192.168.1.54

    ping(a.s, a.q, a.ip, a.dest_port, a.port)
