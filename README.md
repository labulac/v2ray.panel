![logo.png](pic/logo.png)

## 简介

一个基于 Web 的 V2ray 控制面板，已改造为将树莓派作为旁路由使用，只需要设置好网关，即可代理路由器下所有设备透明翻墙，支持直连\智能分流\全局代理 三种模式，并能自动管理订阅，原理参考 [透明代理(TPROXY)
](https://guide.v2fly.org/app/tproxy.html)，TG:[https://t.me/v2ray_funpi](https://t.me/v2ray_funpi)

![1.png](pic/1.png)  

![2.png](pic/2.png)  

![3.png](pic/3.png)  

![4.png](pic/4.png)  

![5.png](pic/5.png)  

## 硬件支持
Mac  
Raspberry Pi 4B  
[ZeroPi](http://wiki.friendlyarm.com/wiki/index.php/ZeroPi)  

![zeropi_1.jpg](pic/zeropi_1.jpg)  

![zeropi_2.jpg](pic/zeropi_2.jpg)  

## 系统支持
MacOS  
Raspberry Pi OS (based on Debian Buster)  
Armbian (based on Debian Buster)

## 安装方式
### Mac
```
# 安装 brew
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# clone 代码
cd ~/Documents/
git clone https://github.com/twotreesus/V2ray.FunPi.git V2ray.Fun

# 安装依赖
./script/install_osx.sh

# 运行
python3 app.py
# 浏览器输入127.0.0.1:1086，即可访问面板
# 浏览器设置 socks5 代理 127.0.0.1:1080，即可使用，Chrome 浏览器推荐使用 SwitchyOmega

```

### Raspberry Pi
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
