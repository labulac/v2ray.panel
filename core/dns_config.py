# encoding: utf-8

class DnsConfig:
    default_local_dns = '223.5.5.5'
    default_remote_dns = '8.8.8.8'

    def __init__(self):
        self.local_dns = ''
        self.remote_dns = ''