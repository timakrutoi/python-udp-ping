#!/usr/bin/python3
#encode=utf-8

import time
import socket
import struct

from udpchecksum import calc_checksum


def bytes2ip(x):
    return '.'.join([str(i) for i in x])


def server(port):
    serverSocket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_RAW,
            proto=socket.IPPROTO_UDP)
    serverSocket.bind(('', port))

    while True:
        message = serverSocket.recv(1024)

        ip_start = 12
        src_ip = message[ip_start:ip_start+4]
        dest_ip = message[ip_start+4:ip_start+8]

        s_port = int.from_bytes(message[20:22], 'big')
        d_port = int.from_bytes(message[22:24], 'big')
        if d_port != port:
            # print('got wrong port ', d_port)
            continue

        checksum = calc_checksum(src_ip, dest_ip, message[20:])
        if int.from_bytes(message[26:28], 'big') == 0:
            print(f'got zero checksum from {bytes2ip(src_ip)}')
        elif int.from_bytes(checksum, 'big') == 0:
            print(f'got correct checksum from {bytes2ip(src_ip)}')
        else:
            print(f'got wrong checksum {checksum} '
                  f'from {bytes2ip(src_ip)}')

            msg = (struct.pack('!4H', d_port, s_port, 8 + 12, 0)
                   + bytes('Bad checksum', 'utf-8'))
            serverSocket.sendto(msg, (bytes2ip(src_ip), s_port))

        time.sleep(0.1)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('-p', '--port', type=int, default=55555)

    a = p.parse_args()

    server(**vars(a))
