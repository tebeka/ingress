"""A 'backdoor' shell for running servers (very much like Twisted manhole).

Once installed, you can 'telnet <host> <port>' and run Python commands on your
server environment. This is very helpful in debugging servers.

This one uses only modules found in the standard library.
"""

__author__ = 'Miki Tebeka <miki.tebeka@gmail.com>'
__version__ = '0.4.0'

from contextlib import redirect_stdout, redirect_stderr
import socketserver
from threading import Thread
from traceback import format_exc
import socket

EOF = chr(4)
DEFAULT_ADDRESS = ('localhost', 9998)
QUIT = 'quit()'


class PyHandler(socketserver.StreamRequestHandler):
    password = None
    env = {}
    prompt = '>>> '

    def handle(self):
        env = self.env.copy()
        welcome = 'Welcome to ingress (type "{}" to exit)\n'.format(QUIT)
        self.write(welcome)

        if not self.login():
            return

        while True:
            try:
                self.write(self.prompt)
                expr = self.rfile.readline().rstrip()
                if expr == EOF:
                    return

                expr = expr.decode('utf-8')

                if expr == QUIT:
                    self.request.close()
                    return

                with redirect_stdout(self), redirect_stderr(self):
                    try:
                        value = eval(expr, globals(), env)  # nosec
                        out = format(value) + '\n'
                        self.write(out)
                    except Exception:
                        exec(expr, env)  # nosec
            except (EOFError, SystemExit, socket.error):
                return
            except Exception:
                error = format_exc()
                import sys
                print(error, file=sys.stderr)
                self.write(error)

    def finish(self):
        try:
            super().finish()
        except socket.error:
            pass

    def login(self):
        if not self.password:
            return True

        for i in range(3):
            self.write('Password: ')
            password = self.rfile.readline().strip().decode('utf-8')
            if password == self.password:
                return True
            self.write('Bad password\n')

        return False

    def write(self, obj):
        if isinstance(obj, str):
            obj = obj.encode('utf-8')
        self.wfile.write(obj)


class ThreadedServer(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


def install(address=DEFAULT_ADDRESS, env=None, password=None):
    """Install TCP handler on address

    Parameters
    ----------
    address : tuple
        Address to listen on (host, port)
    env : dict
        Environment to use when evaulation expression (default to globals)
    password : str
        Login password
    """

    class Handler(PyHandler):
        pass

    Handler.env = {} if env is None else env
    Handler.password = password

    server = ThreadedServer(address, Handler)
    thr = Thread(target=server.serve_forever, daemon=True)
    thr.start()

    return thr
