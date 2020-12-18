#!/bin/sh

cd /usr/local/V2ray.Fun/

export V2RAY_LOCATION_ASSET=/usr/local/share/v2ray/
nohup /usr/local/bin/v2ray -config /etc/v2ray/config.json &

python3 app.py
