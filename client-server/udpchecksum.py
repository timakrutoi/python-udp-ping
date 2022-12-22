import struct


def calc_checksum(src_ip, dest_ip, data):
    if type(src_ip) == str:
        src_ip = struct.pack('!4B', *[int(x) for x in src_ip.split('.')])
    if type(dest_ip) == str:
        dest_ip = struct.pack('!4B', *[int(x) for x in dest_ip.split('.')])
    zero_proto = struct.pack('!2B', 0, 17)
    length = struct.pack('!2B', data[4], data[5])

    pseudo_hdr = src_ip + dest_ip + zero_proto + length + data
    if len(pseudo_hdr) % 2 == 1:
        pseudo_hdr += struct.pack('!1B', 0)

    checksum = 0

    for i in range(0, len(pseudo_hdr), 2):
        w = (pseudo_hdr[i] << 8) + (pseudo_hdr[i + 1])
        checksum += w

    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = struct.pack('!1H', ~checksum & 0xFFFF)
    return checksum


if __name__ == '__main__':
    src = '127.0.0.1'
    dest = '127.0.0.1'
    payload = bytes('ab', 'utf-8')

    port = 55555
    dest_port = 4567
    length = 8 + len(payload)
    checksum = 0

    header = struct.pack('!4H', dest_port, port, length, checksum) + payload

    checksum = calc_checksum(src, dest, header)
    print('checksum ', checksum)

    header = struct.pack('!3H', dest_port, port, length) + checksum + payload

    checksum = calc_checksum(src, dest, header)
    print('checksum ', checksum)
