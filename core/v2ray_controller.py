# encoding: utf-8
"""
File:       v2ray_controller
Author:     twotrees.us@gmail.com
Date:       2020年7月30日  31周星期四 10:53
Desc:
"""
import textwrap
import subprocess
import requests
import sys
from .v2ray_user_config import V2RayUserConfig
from .v2ray_config import V2RayConfig

class V2rayController:
    def start(self) -> bool:
        cmd = "systemctl start v2ray.service"
        subprocess.check_output(cmd, shell=True).decode('utf-8')
        return self.running()

    def stop(self) -> bool:
        cmd = "systemctl stop v2ray.service"
        subprocess.check_output(cmd, shell=True).decode('utf-8')
        return not self.running()

    def restart(self) -> bool:
        cmd = "systemctl restart v2ray.service"
        subprocess.check_output(cmd, shell=True).decode('utf-8')
        return self.running()

    def running(self) -> bool:
        cmd = """ps -ef | grep "v2ray" | grep -v grep | awk '{print $2}'"""
        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        if output == "":
            return False
        else:
            return True

    def version(self) -> str:
        v2ray_path = 'v2ray'
        cmd_get_current_ver = """echo `{0} -version 2>/dev/null` | head -n 1 | cut -d " " -f2""".format(v2ray_path)
        current_ver = 'v' + subprocess.check_output(cmd_get_current_ver, shell=True).decode('utf-8').replace('\n', '')

        return current_ver

    def check_new_version(self) -> str:
        r = requests.get('https://api.github.com/repos/v2fly/v2ray-core/releases/latest')
        r = r.json()
        version = r['tag_name']
        return version

    def update(self) -> bool:
        update_log = subprocess.check_output("bash ./script/update_v2ray.sh", shell=True).decode('utf-8')
        ret = update_log.find('installed')
        if ret:
            ret = self.restart()

        return ret

    def access_log(self) -> str:
        with open('/var/log/v2ray/access.log') as f:
            lines = f.read().split("\n")
            return self.wrap_last_lines(lines)

    def error_log(self) -> str:
        with open('/var/log/v2ray/error.log') as f:
            lines = f.read().split("\n")
            return self.wrap_last_lines(lines)

    def wrap_last_lines(self, lines: list) -> str:
        count = min(10, len(lines))
        lines = lines[-count:]
        string = ""

        wrapper = textwrap.TextWrapper(width=100)
        for line in lines:
            wrap_list = wrapper.wrap(line)
            for wrap in wrap_list:
                string += wrap + '<br>'
        return string

    def apply_node(self, user_config:V2RayUserConfig, restart: bool) -> bool:
        config = V2RayConfig.gen_config(user_config)
        return self.apply_config(config, restart)

    def apply_config(self, config: str, restart: bool) -> bool:
        with open('/etc/v2ray/config.json', 'w+') as f:
            f.write(config)

        result = True
        if restart:
            result = self.restart()
        return  result

    def enable_iptables(self):
        subprocess.check_output("bash ./script/config_iptable.sh", shell=True)
        subprocess.check_output("systemctl enable v2ray_iptable.service", shell=True)

class MokeV2rayController(V2rayController):
    def start(self) -> bool:
        return True

    def stop(self) -> bool:
        return True

    def restart(self) -> bool:
        return True

    def running(self) -> bool:
        return True

    def version(self) -> str:
        return 'v4.27.0'

    def update(self) -> bool:
        return True

    def access_log(self) -> str:
        return ''

    def error_log(self) -> str:
        return ''

    def apply_config(self, config: str, restart: bool) -> bool:
        with open('config/moke_config.json', 'w+') as f:
            f.write(config)
        return True

    def enable_iptables(self):
        return

def make_controller():
    if sys.platform == 'darwin':
        return MokeV2rayController()
    else:
        return V2rayController()