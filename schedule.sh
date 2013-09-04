#!/bin/bash
rm /tmp/.X99-lock
killall Xvfb
Xvfb :99 -screen 0 800x600x16 &
export DISPLAY=:99

python manage.py sche_finds
python manage.py sche_alerts
python manage.py sche_update

rm /tmp/.X99-lock
killall Xvfb
