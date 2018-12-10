#!/usr/bin/python3
import cherrypy
from app import Root

app = cherrypy.tree.mount(Root(), '/')

if __name__ == '__main__': 
        cherrypy.config.update({'server.socket_host': '0.0.0.0'})
        cherrypy.quickstart(Root())
