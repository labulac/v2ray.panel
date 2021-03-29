# encoding: utf-8
"""
File:       core_service
Author:     twotrees.us@gmail.com
Date:       2020年7月30日  31周星期四 10:55
Desc:
"""
import psutil
import os
import os.path
from .package import jsonpickle
from typing import List

from .app_config import AppConfig
from .v2ray_controller import V2rayController, make_controller

from .node_manager import NodeManager
from .keys import Keyword as K
from .v2ray_user_config import V2RayUserConfig

class CoreService:
    app_config : AppConfig = None
    user_config: V2RayUserConfig = V2RayUserConfig()
    v2ray:V2rayController = make_controller()
    node_manager = NodeManager()

    @classmethod
    def load(cls):
        config_path = 'config/'
        if not os.path.exists(config_path):
            os.mkdir(config_path)

        cls.app_config = AppConfig().load()
        cls.node_manager = NodeManager().load()
        cls.user_config = V2RayUserConfig().load()

    @classmethod
    def status(cls) -> dict:
        running = cls.v2ray.running()
        version = cls.v2ray.version()

        result = {
            K.running: running,
            K.version: version,
            K.proxy_mode: cls.user_config.proxy_mode,
        }

        node = cls.user_config.node.dump()
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
    def apply_node(cls, url:str, index: int) -> bool:
        result = False
        node = cls.node_manager.find_node(url, index)
        cls.user_config.node = node
        if cls.v2ray.apply_node(cls.user_config, cls.node_manager.all_nodes()):
            cls.user_config.save()

            if not cls.app_config.inited:
                cls.v2ray.enable_iptables()
                cls.app_config.inited = True
                cls.app_config.save()

            result = True
        return result

    @classmethod
    def switch_mode(cls, proxy_mode: int) -> bool:
        cls.user_config.proxy_mode = proxy_mode
        result = True
        result = cls.v2ray.apply_node(cls.user_config, cls.node_manager.all_nodes())
        if result:
            cls.user_config.save()

        return result

    @classmethod
    def apply_advance_config(cls, config:dict):
        result = True
        new_advance = cls.user_config.advance_config.load_data(config)
        cls.user_config.advance_config = new_advance
        result = cls.v2ray.apply_node(cls.user_config, cls.node_manager.all_nodes())
        if result:
            cls.user_config.save()
        return  result

    @classmethod
    def reset_advance_config(cls):
        result = True
        cls.user_config.advance_config = V2RayUserConfig.AdvanceConfig()
        result = cls.v2ray.apply_node(cls.user_config, cls.node_manager.all_nodes())
        if result:
            cls.user_config.save()
        return result

    @classmethod
    def make_policy(cls, contents:List[str], type:str, outbound:str) -> dict:
        type = V2RayUserConfig.AdvanceConfig.Policy.Type[type]
        outbound = V2RayUserConfig.AdvanceConfig.Policy.Outbound[outbound]
        policy = V2RayUserConfig.AdvanceConfig.Policy()
        policy.contents = contents
        policy.type = type.name
        policy.outbound = outbound.name
        return jsonpickle.encode(policy, indent=4)