To start web service when system starts
```
cd /etc/systemd/system/
sudo ln -sf [PATH_TO_THE_SERVICE_FILE]
sudo systemctl daemon-reload
sudo systemctl --all .  # verify myweather.service is listed
sudo systemctl start myweather
sudo systemctl status myweather
```

The myweather.service starts uwsgi server with creating socket `weather.sock` as communication channel between Nginx and the server.

Nginx configuration should be set for it. For example
```
location / {
    include uwsgi_params;
    uwsgi_pass unix:/home/astropi/workspace/myweather/weather.sock;
}
```

To start displaying temperature on 7-Segment LED, do same procedure for display-temperature.service.
