# encoding: utf-8
"""
File:       core_service
Author:     twotrees.us@gmail.com
Date:       2020年7月30日  31周星期四 10:55
Desc:
"""
import psutil
import subprocess
import os
import os.path

from .app_config import AppConfig
from .node_item import NodeItem
from .v2ray_controller import V2rayController
from .node_manager import NodeManager
from .keys import Keyword as K
from .advance_config import AdvanceConfig

class CoreService:
    app_config : AppConfig = None
    node_config : NodeItem = None
    advance_config : AdvanceConfig = None
    v2ray = V2rayController()
    node_manager = NodeManager()

    @classmethod
    def load(cls):
        config_path = 'config/'
        if not os.path.exists(config_path):
            os.mkdir(config_path)

        cls.app_config = AppConfig().load()
        cls.node_config = NodeItem().load()
        cls.advance_config = AdvanceConfig().load()
        cls.node_manager = NodeManager().load()

    @classmethod
    def status(cls) -> dict:
        running = cls.v2ray.running()
        version = cls.v2ray.version()

        result = {
            K.running: running,
            K.version: version,
            K.proxy_mode: cls.app_config.proxy_mode,
        }

        node = cls.node_config.dump()
        result.update(node)
        return result

    @classmethod
    def performance(cls) -> dict:
        result = {}
        cpu_usage = psutil.cpu_percent(interval=0.2, percpu=True)
        result_cpu = {}
        core = 0
        for u in cpu_usage:
            core += 1
            result_cpu["core {0}".format(core)] = u
        result['cpu'] = result_cpu

        memory_usage = psutil.virtual_memory()
        result['memory'] = {
            "percent" : memory_usage.percent,
            "total" : int(memory_usage.total / (1024 * 1024)),
            "used" : int((memory_usage.total - memory_usage.available) / (1024 * 1024))
        }
        return result

    @classmethod
    def add_subscribe(cls, url: str):
        cls.node_manager.add_subscribe(url)

    @classmethod
    def apply_node(cls, url:str, index: int) -> bool:
        result = False
        node = cls.node_manager.groups[url].nodes[index]
        if cls.v2ray.apply_node(node, cls.node_manager.all_nodes(), cls.app_config.proxy_mode, cls.advance_config, True):
            cls.node_config = node
            cls.node_config.save()

            if not cls.app_config.inited:
                subprocess.check_output("bash ./script/config_iptable.sh", shell=True)
                subprocess.check_output("enable v2ray_iptable.service", shell=True)
                cls.app_config.inited = True
                cls.app_config.save()

            result = True
        return result

    @classmethod
    def switch_mode(cls, proxy_mode: int) -> bool:
        result = True
        result = cls.v2ray.apply_node(cls.node_config, cls.node_manager.all_nodes(), proxy_mode, cls.advance_config, cls.v2ray.running())
        if result:
            cls.app_config.proxy_mode = proxy_mode
            cls.app_config.save()

        return result

    @classmethod
    def node_link(cls, url: str, index: int) ->bool:
        node = cls.node_manager.groups[url].nodes[index]
        return node.link

    @classmethod
    def set_local_dns(cls, local_dns: str):
        result = True
        cls.advance_config.dns.local_dns = local_dns
        result = cls.v2ray.apply_node(cls.node_config, cls.node_manager.all_nodes(), cls.app_config.proxy_mode, cls.advance_config, cls.v2ray.running())
        if result:
            cls.advance_config.save()
        return result

    @classmethod
    def set_remote_dns(cls, remote_dns: str):
        result = True
        cls.advance_config.dns.remote_dns = remote_dns
        result = cls.v2ray.apply_node(cls.node_config, cls.node_manager.all_nodes(), cls.app_config.proxy_mode, cls.advance_config, cls.v2ray.running())
        if result:
            cls.advance_config.save()
        return result



