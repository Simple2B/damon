# Deploy instruction
This instruction for deploy Flask application.

**Prerequisites:**
* OS: Ubuntu 18.*
* Web Server: Nginx
* Python3
* [uWSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface)

## Configure WSGI
We use uWSGI service from python virtual environment.
Activate virtual environment and setup actual packages:
```
sudo apt-get install python3-dev build-essential
cd ~/site
source .venv/bin/activate
pip install uwsgi
```
Verify **uwsgi.ini** file (WSGI configuration) in project folder:
```ini
[uwsgi]
# path to project foled
base = /home/<user>/site
# module name
module = flask_app:app
# virtual env
chdir = %(base)
home = %(base)/.venv

master = true
# number of processes uWSGI
processes = 5
# user name for process
uid = <user>
gid = www-data
socket = /tmp/site-uwsgi.sock
chmod-socket = 660

# remove temporary files on service stop
vacuum = true
# path to log file
logto = /tmp/uwsgi.log

die-on-term = true
wsgi-disable-file-wrapper = true

```
Line `base = /home/<user>/site` must contain correct path to project folder.
Line `uid = <user>` must contain correct user name.

## Create Linux Service

Create file `/etc/systemd/system/site-uwsgi.service` with follow content:
```ini
[Unit]
Description=uWSGI instance to serve flask-uwsgi project
After=network.target

[Service]
User=<user>
Group=www-data
WorkingDirectory=/home/<user>/site
Environment="PATH=/home/<user>/site/.venv/bin"
ExecStart=/home/<user>/site/.venv/bin/uwsgi --ini /home/<user>/site/uwsgi.ini

[Install]
WantedBy=multi-user.target
```

#### Attention! This file content for:
* User: `<user>`
* Project folder `/home/<user>/site`
You need fix it if you have another user name or/and project folder

Run service:
```
sudo systemctl start site-uwsgi
```
Activate service
```
sudo systemctl enable site-uwsgi
```

## Nginx configuration

Create file `/etc/nginx/sites-available/site.conf` with following content:
```
upstream uwsgi_site_upstream {
    server unix:/tmp/site-uwsgi.sock;
}

server {
    listen 80;
    server_tokens off;
    server_name <host>.<domain-name>;

     location / {
         include uwsgi_params;
         uwsgi_pass uwsgi_site_upstream;
     }
}
```

Activate this Nginx configuration:
```
sudo ln -s /etc/nginx/sites-available/site.conf
```
Check if our configuration file is OK:
```
sudo nginx -t
```
Reload Nginx configuration:
```
sudo systemctl reload nginx
```