#!/bin/sh
ssh root@134.209.195.117 <<EOF
    source ./incodaqweatherenv/bin/activate
    cd incodaq_weather
    git pull
    pip install -r requirements.txt
    ./manage.py migrate
    systemctl restart gunicorn
    systemctl daemon-reload
    systemctl restart gunicorn.socket gunicorn.service
    nginx -t && sudo systemctl restart nginx
    exit
EOF