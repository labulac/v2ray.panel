# encoding: utf-8

from .base_data_item import BaseDataItem

class AdvanceConfig(BaseDataItem):
    def __init__(self):
        self.local_dns = ''
        self.remote_dns = ''

    def filename(self):
        return 'config/adv_config.json'