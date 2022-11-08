# Ingress

[![Python package](https://github.com/tebeka/ingress/actions/workflows/python-package.yml/badge.svg)](https://github.com/tebeka/ingress/actions/workflows/python-package.yml)

Ingress is a pure Python, no dependencies REPL (interactive prompt) over the network to your application 
(very much like [Twisted manhole](http://www.lothar.com/tech/twisted/manhole.xhtml)).

Once installed (using `ingress.install()`), you can `telnet <host> <port>` and run Python commands on your server.
This is helpful when debugging servers.
