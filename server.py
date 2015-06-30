# import os
import socket
import subprocess

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 3141))
server_socket.listen(0)

connection = server_socket.accept()[0].makefile('rb')
try:
    cmdline = [
        'vlc',
        # '-I', 'http',
        # '--http-host', '0.0.0.0',
        # '--http-port', '8888',
        # '--http-password', os.environ['VLC_HTTP_PASSWORD'],
        '--sout', 'http/ts://0.0.0.0:31415',
        '--demux', 'h264',
        '-',
    ]
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    while True:
        data = connection.read(1024)
        if not data:
            break
        player.stdin.write(data)
finally:
    connection.close()
    server_socket.close()
    player.terminate()

