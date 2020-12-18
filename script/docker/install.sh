#!/bin/sh

#install depend Packages
apt-get update -y
apt-get install gcc procps wget git python3-setuptools python3-dev -y

# clone project
cd /usr/local
git clone --depth=1 https://github.com/twotreesus/V2ray.FunPi.git V2ray.Fun
cd V2ray.Fun/script

# install python package
pip3 install -r requirements.txt


# install v2ray
mkdir -p /etc/v2ray/
touch /etc/v2ray/config.json
chmod 644 /etc/v2ray/config.json
mkdir -p /var/log/v2ray/
bash update_v2ray.sh

echo "install success"