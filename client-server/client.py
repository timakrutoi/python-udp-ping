#!/usr/bin/python3
#encode=utf-8

import socket
import struct
import time

from udpchecksum import calc_checksum as get_checksum


def gen_data(size):
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    res = ''
    for i in range(size):
        res += alphabet[i % len(alphabet)]

    return bytes(res, 'utf-8')


def dns_lookup(hostname):

    return socket.gethostbyname(hostname)


def ping(
        hostname,
        dest_port, port, packet_size, number_of_pings,
        sleep_time, timeout, calc_checksum):

    sock_out = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_RAW,
            proto=socket.IPPROTO_UDP)
    sock_in = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_RAW,
            proto=socket.IPPROTO_UDP)

    sock_in.settimeout(timeout)

    ip = dns_lookup(hostname)

    ip_hdr_size = 20
    udp_hdr_size = 8

    payload_size = packet_size - udp_hdr_size
    times = []

    payload = gen_data(payload_size)
    length = 8 + payload_size

    print(dest_port, port)
    header = struct.pack('!4H', dest_port, port, length, 0)
    if calc_checksum:
        checksum = get_checksum('127.0.0.1', ip, header + payload)
        header = struct.pack('!3H', dest_port, port, length) + checksum

    header += payload

    print(f'Ping {hostname} ({ip}) with {packet_size} bytes.')

    for i in range(number_of_pings):
        try:
            s = time.time()
            sock_out.sendto(header + payload, (ip, port))

            try:
                rec_pkg = sock_in.recv(1024)
            except socket.timeout:
                print(f'No reply recieved in {timeout}s.')
                sock_in.settimeout(timeout)
                continue

            times.append(round((time.time() - s)*1000, 2))
            print(f'recieved reply from {rec_pkg[12:16]} in {times[-1]}ms, '
                  f'(message {rec_pkg[ip_hdr_size + 8:]})')

            time.sleep(sleep_time / 1000)

        except KeyboardInterrupt:
            break

    print()
    if len(times) > 0:
        print(f'Total {len(times)} pings '
              f'with avg time {round(sum(times) / len(times), 2)}ms.')
    else:
        print('No successful pings.')


if __name__ == '__main__':
    from argparse import ArgumentParser

    p = ArgumentParser()
    p.add_argument('--ip', '--hostname', dest='hostname', type=str,
                   help='IP of server to ping.')
    p.add_argument('--dest-port', type=int, default=4567,
                   help='Port to get reply. Default = %(default)d.')
    p.add_argument('--port', type=int, default=33434,
                   help='Port to ping. Default = %(default)d.')
    p.add_argument('-l', '--packet-size', type=int, default=64,
                   help='Size of packet. Default = %(default)d.')
    p.add_argument('-n', '--number-of-pings', type=int, default=3,
                   help='Number of pings. Default = %(default)d.')
    p.add_argument('--sleep-time', type=int, default=500,
                   help='Time between pings in ms. Default = %(default)d.')
    p.add_argument('--timeout', type=int, default=10,
                   help='Time to wait for reply in s. Default = %(default)d.')
    p.add_argument('-c', '--calc-checksum', action='store_true', default=False,
                   help='Calculate checksum or not. Default = %(default)b.')

    a = p.parse_args()

    ping(**vars(a))
