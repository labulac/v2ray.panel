FROM python:3.8-slim-buster

expose 1080
expose 1086

ADD install.sh /root/
ADD run.sh /root/

RUN chmod +x /root/install.sh && /root/install.sh
CMD chmod +x /root/run.sh && /root/run.sh