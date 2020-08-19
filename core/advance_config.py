# encoding: utf-8

from .base_data_item import BaseDataItem
from .dns_config import DnsConfig

class AdvanceConfig(BaseDataItem):
    def __init__(self):
        self.dns: DnsConfig = DnsConfig()

    def filename(self):
        return 'config/adv_config.json'