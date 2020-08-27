![logo.png](pic/logo.png)

## 简介

一个基于 Web 的 V2ray 控制面板，已改造为将树莓派作为旁路由使用，只需要设置好网关，支持直连\智能分流\全局代理 三种模式，并能自动管理订阅，原理参考 [透明代理(TPROXY)
](https://guide.v2fly.org/app/tproxy.html)，TG:[https://t.me/v2ray_funpi](https://t.me/v2ray_funpi)

![1.png](pic/1.png)  

![2.png](pic/2.png)  

![3.png](pic/3.png)  

![4.png](pic/4.png)  

## 硬件支持
Raspberry Pi 4B  
[ZeroPi](http://wiki.friendlyarm.com/wiki/index.php/ZeroPi)  

![zeropi_1.jpg](pic/zeropi_1.jpg)  

![zeropi_2.jpg](pic/zeropi_2.jpg)  

## 系统支持
Raspberry Pi OS (based on Debian Buster)  
Armbian (based on Debian Buster)

## 安装方式
```
sudo su - root
cd /usr/local
git clone https://github.com/twotreesus/V2ray.FunPi.git V2ray.Fun
cd V2ray.Fun/script
./install.sh
```

## 配置方式
修改配置文件

```
sudo nano /usr/local/V2ray.Fun/config/app_config.json
{
    "user": "admin",
    "password": "admin",
    "port": 1099,
    "proxy_mode": 1
}
```
重启服务

```
sudo supervisorctl restart v2ray.fun
```

树莓派修改为静态地址192.168.66.200，这里路由器是192.168.66.1
```
sudo nano /etc/dhcpcd.conf

# Example static IP configuration:
interface eth0
static ip_address=192.168.66.200/24
static routers=192.168.66.1
static domain_name_servers=192.168.66.1
```

然后设置路由器的DHCP网关为 192.168.66.200
![router.png](pic/router.png)
