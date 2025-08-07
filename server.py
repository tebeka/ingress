"""Small test server"""

import ingress

from argparse import ArgumentParser

parser = ArgumentParser(description=__doc__)
parser.add_argument(
    '--port', '-p', help='port to listen on', type=int, default=8999)
parser.add_argument('--passwd', '-l', help='login password', default='')
args = parser.parse_args()

ingress.install(('localhost', args.port), password=args.passwd)
print(f'server ready on {args.port}')
try:
    input('Hit ENTER or CTRL-C to quit')
except KeyboardInterrupt:
    pass
