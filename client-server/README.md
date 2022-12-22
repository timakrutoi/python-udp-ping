# client-server UDP ping

Custom ping, reply is caused by wrong UDP checksum.

# Usage: 

Start server first:

```python server.py --port 55555```

Ping your server:

```python client --ip 127.0.0.1 --port 55555 -c 333```

You will get a reply from server due to checksum being wrong.
If checksum is correct or checksum is 0 server will not send reply.
