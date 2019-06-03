import cherrypy
import time
import math
import sqlite3
from os import path
import contextlib
root_dir = path.dirname(path.dirname(path.abspath(__file__)))

from datetime import datetime, timezone

class Root(object):
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        with contextlib.closing(sqlite3.connect(root_dir + '/db/weather.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)) as conn:
            cur = conn.cursor()
            cur.execute('SELECT temperature, humidity, pressure, created_at "[timestamp]" FROM weather ORDER BY id DESC limit 1')
            record = cur.fetchone()
            
            local_time = record[3].replace(tzinfo=timezone.utc).astimezone(tz=None)
                
            return {
                "temperature": record[0],
                "pressure": record[2],
                "humidity": record[1],
                "dt": local_time.strftime("%Y-%m-%d %H:%M:%S%z")
            }
            