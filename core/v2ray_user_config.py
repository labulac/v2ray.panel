# encoding: utf-8
from enum import Enum, auto
import typing
from typing import List
from .base_data_item import BaseDataItem
from .node import Node

class V2RayUserConfig(BaseDataItem):
    class ProxyMode(Enum):
        Direct = 0
        ProxyAuto = 1
        ProxyGlobal = 2

    class AdvanceConfig(BaseDataItem):
        class Policy:
            class Type(Enum):
                ip = auto()
                domain = auto()
            class Outbound(Enum):
                direct = auto()
                proxy = auto()
                block = auto()

            def __init__(self, content:str, type:Type, outbound:Outbound):
                self.content = content
                self.type = type.name
                self.outbound = outbound.name

        class DnsConfig:
            def __init__(self):
                self.default_local = '223.5.5.5'
                self.default_remote = '8.8.8.8'
                self.local = ''
                self.remote = ''

            def local_dns(self) -> str:
                if len(self.local):
                    return self.local
                else:
                    return self.default_local

            def remote_dns(self) -> str:
                if len(self.remote):
                    return self.remote
                else:
                    return self.default_remote

        def __init__(self):
            self.dns: V2RayUserConfig.AdvanceConfig.DnsConfig = V2RayUserConfig.AdvanceConfig.DnsConfig()
            self.policys:List[V2RayUserConfig.AdvanceConfig.Policy] = []

    def filename(self):
        return 'config/v2ray_user_config.json'

    def __init__(self):
        self.proxy_mode:int = self.ProxyMode.ProxyAuto.value
        self.node:Node = Node()
        self.advance_config:V2RayUserConfig.AdvanceConfig = self.AdvanceConfig()