import cherrypy
import time
import os
from app import Root

cherrypy.config.update({'engine.autoreload.on': False})
cherrypy.server.unsubscribe()
cherrypy.engine.start()

conf={
    "/css": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": os.path.abspath("./css")
    },
    "/javascript": {
        'tools.staticdir.on':True,
        "tools.staticdir.dir": os.path.abspath("./javascript")
    }
}

wsgiapp = cherrypy.tree.mount(Root(),config=conf)
