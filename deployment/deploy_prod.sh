#!/bin/sh


#ssh root@server ip address <<EOF
#  cd incodaq_weather
#git pull
#  source /opt/envs/incodaq_weather/bin/activate
#  pip install -r requirements.txt
#  ./manage.py migrate
#  sudo supervisorctl restart incodaq_weather
#  exit
#EOF