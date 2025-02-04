#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys



import socket
import cherrypy
from django.core.management import execute_from_command_line
from live_server.wsgi import application

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'live_server.settings')
    try:
        if sys.argv[1] == "runserver":
            ssl_certfile = 'cert.pem'
            ssl_keyfile = 'key.pem'

            cherrypy.config.update({
                'server.socket_host': socket.gethostbyname(socket.gethostname()),
                'server.socket_port': 8800,
                'server.ssl_module': 'builtin',
                'server.ssl_certificate': ssl_certfile,
                'server.ssl_private_key': ssl_keyfile
            })

            cherrypy.tree.graft(application, '/')
            cherrypy.engine.start()
            cherrypy.engine.block()
        else:
            from django.core.management import execute_from_command_line
            
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
