from socket import error as SocketError
from socket import socket
from subprocess import Popen
from sys import executable
from time import sleep, time

import pytest

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
            sock.close()
            return True
        except SocketError:
            sleep(0.1)

    return False


@pytest.fixture(scope='function')
def server_port():
    port = free_port()
    pipe = Popen([executable, 'ingress.py', '-p', str(port)])
    assert wait_for_server(port), 'server did not start'
    yield port
    pipe.kill()


def test_ingress(server_port):
    sock = socket()
    sock.connect(('localhost', server_port))
    rfile, wfile = sock.makefile('r'), sock.makefile('w')
    header = rfile.readline()
    assert 'ingress' in header, 'bad header'

    wfile.write('1 + 1\n')
    wfile.flush()
    out = rfile.readline().strip()
    out = out[len(ingress.PyHandler.prompt):]
    assert out == '2', 'bad output'
