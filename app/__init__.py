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
            cur.execute('SELECT temperature, pressure, humidity, delta, created_at "[timestamp]" FROM weather ORDER BY id DESC limit 1')
            record = cur.fetchone()
            
            local_time = record[4].replace(tzinfo=timezone.utc).astimezone(tz=None)
                
            return {
                "temperature": record[0],
                "pressure": record[1],
                "humidity": record[2],
                "delta": record[3],
                "dt": local_time.strftime("%Y-%m-%d %H:%M:%S%z")
            }
            
    @cherrypy.expose
    def trend(self, mins = 60):
        with contextlib.closing(sqlite3.connect(root_dir + '/db/weather.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)) as conn:
            cur = conn.cursor()
            
            html = """<html>
              <head>
                  <link rel="stylesheet" href="/css/chartist.min.css">
              </head>
              <body>
                  Temperature:
                  <div class="ct-chart ct-perfect-fourth"></div>
              """
                
            sql = """SELECT temperature, pressure, humidity, delta, created_at "[timestamp]"
                     FROM weather 
                     WHERE created_at > datetime("now", "-{} minutes")""".format(mins)
                     

            max = -100
            min = 100
            dat = ""
            for record in cur.execute(sql):
                local_time = record[4].replace(tzinfo=timezone.utc).astimezone(tz=None)
                dat += "{{x: new Date({}), y: {}}},\n".format(local_time.timestamp() * 1000, ("%0.2f" % record[0]))
                if max < record[0]:
                    max = record[0]
                
                if min > record[0]:
                    min = record[0]
                
            ticks = ""
            r = 0
            while r < 50:
                ticks += "{},".format(r)
                r += 0.5
              
            return html + """
                <script src="/javascript/chartist.min.js"></script>
                <script src="/javascript/moment.js"></script>
                <script>
                      var data = {
                      // Our series array that contains series objects or in this case series data arrays
                      series: [
                        { name: 'temp',
                          data: [""" + dat + """]
                        }
                      ]
                    };
                    
                    // As options we currently only set a static size of 300x200 px. We can also omit this and use aspect ratio containers
                    // as you saw in the previous example
                    var options = {
                      height: 530,
                      axisX: {
                        type: Chartist.FixedScaleAxis,
                        divisor: 12,
                        labelInterpolationFnc: function(value) {
                          return moment(value).format('h:mm a');
                        }
                      },
                      axisY: {
                        ticks: [""" + ticks + """],
                        low: """ + ("%0.2f" % (min - 0.5)) + """,
                        high: """ + ("%0.2f" % (max + 0.5)) + """,
                    },
                    };

                    // Create a new line chart object where as first parameter we pass in a selector
                    // that is resolving to our chart container element. The Second parameter
                    // is the actual data object.
                    new Chartist.Line('.ct-chart', data, options);
                  </script>
              </body>
              </html>"""
