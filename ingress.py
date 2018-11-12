#!/usr/bin/env python
'''A 'backdoor' shell for running servers (very much like Twisted manhole).

Once installed, you can 'telnet <host> <port>' and run Python commands on your
server environment. This is very helpful in debugging servers.

This one uses only modules found in the standard library.
'''

__author__ = 'Miki Tebeka <miki.tebeka@gmail.com>'
__version__ = '0.3.0'

from contextlib import contextmanager
from six import b, exec_, string_types
from six.moves import socketserver as socksrv
from threading import Thread
from traceback import format_exc
import socket
import sys

EOF = chr(4)
DEFAULT_PORT = 9998


@contextmanager
def redirect_stdout(fo):
    old_stdout = sys.stdout
    sys.stdout = fo
    yield fo
    sys.stdout = old_stdout


class Writer(object):
    def __init__(self, wfile):
        self.wfile = wfile

    def write(self, obj):
        if isinstance(obj, string_types):
            obj = b(obj)
        self.wfile.write(obj)


class PyHandler(socksrv.StreamRequestHandler):
    password = None
    env = {}
    redirect = False

    def handle(self):
        env = self.env.copy()
        self.wfile.write(b('Welcome to ingress (type "exit()" to exit)\n'))

        if not self.login():
            return

        while True:
            try:
                self.wfile.write(b('>>> '))
                expr = self.rfile.readline().rstrip()
                if expr == EOF:
                    return

                out = Writer(self.wfile) if self.redirect else sys.stdout
                with redirect_stdout(out):
                    try:
                        value = eval(expr, globals(), env)
                        self.wfile.write(format(value) + '\n')
                        self.wfile.flush()
                    except:
                        exec_(expr, env)
            except (EOFError, SystemExit, socket.error):
                return
            except Exception:
                error = format_exc()
                self.wfile.write(b(error))

    def finish(self):
        try:
            socksrv.StreamRequestHandler.finish(self)
        except socket.error:
            pass

    def login(self):
        if not self.password:
            return True

        for i in range(3):
            self.wfile.write('Password: ')
            password = self.rfile.readline().strip()
            if password == self.password:
                return True
            self.wfile.write('Bad password\n')

        return False


class ThreadedServer(socksrv.ThreadingMixIn, socksrv.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


def server_thread(env, port, password=None, redirect=False, host='localhost'):
    # Create a new handler class for this with it's own env
    class Handler(PyHandler):
        pass
    Handler.env = env
    Handler.password = password
    Handler.redirect = redirect

    server = ThreadedServer((host, port), Handler)
    server.serve_forever()


def install(env=None, port=DEFAULT_PORT, password=None, redirect=False,
            host='localhost'):
    env = env or {}
    t = Thread(target=server_thread,
               args=(env, port, password, redirect, host))
    t.daemon = True
    t.start()

    return t


def main(argv=None):
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='Run demo server.')
    parser.add_argument('-p', '--port', help='port to listen',
                        default=DEFAULT_PORT)
    parser.add_argument('-l', '--login', help='login password',
                        default=None)
    parser.add_argument('-r', '--redirect', help='redirect stdout',
                        default=False, action='store_true')
    parser.add_argument('-s', '--host', help='host to bind to',
                        default='localhost')
    args = parser.parse_args(argv[1:])

    t = install(port=args.port, password=args.login, redirect=args.redirect,
                host=args.host)
    print('Serving on {0}:{1}'.format(args.host, args.port))
    t.join()


if __name__ == '__main__':
    main()
