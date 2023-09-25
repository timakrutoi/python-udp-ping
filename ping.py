#!/usr/bin/python3
#encode=utf-8

import socket
import struct
import time


def gen_data(size):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    res = [alphabet[i % len(alphabet)] for i in range(size)]

    return bytes(''.join(res), 'utf-8')


def dns_lookup(hostname):

    return socket.gethostbyname(hostname)


def ping(
        hostname,
        dest_port, port, packet_size, number_of_pings,
        sleep_time, timeout):

    sock_out = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_RAW,
            proto=socket.IPPROTO_UDP)
    sock_in = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_RAW,
            proto=socket.IPPROTO_ICMP)

    sock_in.settimeout(timeout)

    ip = dns_lookup(hostname)

    ip_hdr_size = 20
    udp_hdr_size = 8
    icmp_hdr_size = 8

    payload_size = packet_size - udp_hdr_size
    times = []

    payload = gen_data(payload_size)
    length = 8 + payload_size
    checksum = 0

    header = struct.pack('!4H', dest_port, port, length, checksum)

    print(f'Ping {hostname} ({ip}) with {packet_size} bytes.')

    for i in range(number_of_pings):
        try:

            s = time.time()
            sock_out.sendto(header + payload, (ip, port))

            try:
                rec_pkg = sock_in.recv(ip_hdr_size + icmp_hdr_size)
            except socket.timeout:
                print(f'No reply recieved in {timeout}s.')
                sock_in.settimeout(timeout)
                continue

            times.append(round((time.time() - s)*1000, 2))
            print(f'recieved reply in {times[-1]}ms, '
                  f'(ICMP code {rec_pkg[ip_hdr_size]}, '
                  f'type {rec_pkg[ip_hdr_size + 1]})')

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
                   help='Time to wait for reply in s. Default = %(default)f.')

    a = p.parse_args()

    ping(**vars(a))
