from v2fly/v2fly-core

run sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN set -ex \
	&& apk add linux-headers wget gcc g++ git python3 python3-dev openssl ca-certificates supervisor

run wget https://bootstrap.pypa.io/get-pip.py \
	&& python3 get-pip.py

copy . /usr/local/
run ls /usr/local/

run pip3 install -r /usr/local/V2ray.FunPi/script/requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

run mkdir /etc/supervisor.d \
	&& cp /usr/local/V2ray.FunPi/script/docker/v2ray.ini /etc/supervisor.d/v2ray.ini \
	&& mv /usr/local/V2ray.FunPi /usr/local/V2ray.Fun

expose 1080
expose 1086

volume /etc/v2ray

cmd  supervisord -c /etc/supervisord.conf && sh /usr/local/V2ray.Fun/script/start.sh run


