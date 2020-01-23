from socket import error as SocketError
from socket import socket
from time import sleep, time
import re

import ingress


def free_port():
    sock = socket()
    sock.listen(0)
    port = sock.getsockname()[1]
    sock.close()
    return port


def wait_for_server(port, timeout=10):
    start = time()
    while time() - start <= timeout:
        sock = socket()
        try:
            sock.connect(('localhost', port))
            return sock
        except SocketError:
            sleep(0.1)

    return None


def start_server(passwd=None):
    port = free_port()
    env = {}
    ingress.install(('localhost', port), env, passwd)
    assert wait_for_server(port), 'server did not start'
    return Client(port)


class Client:
    def __init__(self, port):
        sock = wait_for_server(port)
        self.rfile, self.wfile = sock.makefile('r'), sock.makefile('w')

    def write(self, msg):
        self.wfile.write(f'{msg}\n')
        self.wfile.flush()

    def read(self, prefix_len=0):
        out = self.rfile.readline().strip()
        prefix_len += len(ingress.PyHandler.prompt)
        return out[prefix_len:]


def test_ingress():
    c = start_server()
    header = c.read()
    assert 'ingress' in header, 'bad header'

    c.write('1 + 1')
    out = c.read()
    assert out == '2', 'bad output'


def test_password():
    passwd = 's3cr3t'
    c = start_server(passwd)
    c.read()  # Skip header
    c.write(f'{passwd}')

    c.write('1 + 1')
    out = c.read(len('Password: '))
    assert out == '2', 'bad output'


def test_exec():
    c = start_server()
    c.read()  # skip header

    key, val = 'zaphod', 12
    c.write(f'{key} = {val}')
    c.write(key)
    # FIXME: Why the prompt?
    out = re.sub('^>* ', '', c.read())
    assert out == str(val), 'bad value'
