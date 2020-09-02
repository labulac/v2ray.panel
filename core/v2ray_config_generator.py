# encoding: utf-8
"""
File:       v2ray_config_generator
Author:     twotrees.us@gmail.com
Date:       2020年7月30日  31周星期四 15:52
Desc:
"""
import json
from .node import Node
from .v2ray_user_config import V2RayUserConfig

def gen_config(user_config:V2RayUserConfig) -> str:
    config = gen_basic()
    detail = None
    if user_config.proxy_mode == V2RayUserConfig.ProxyMode.Direct.value:
        detail = gen_direct(user_config.node)
    elif user_config.proxy_mode == V2RayUserConfig.ProxyMode.ProxyAuto.value:
        detail = gen_proxy_auto(user_config.node, user_config.advance_config)
    elif user_config.proxy_mode == V2RayUserConfig.ProxyMode.ProxyGlobal.value:
        detail = gen_proxy_global(user_config.node, user_config.advance_config)

    config.update(detail)
    return json.dumps(config, indent=4)

def gen_basic() -> dict:
    basic_raw_config = '''
{
    "log": {
        "access": "/var/log/v2ray/access.log",
        "error": "/var/log/v2ray/error.log",
        "loglevel": "warning"
    },
    "inbounds": [
        {
            "port": 12345,
            "protocol": "dokodemo-door",
            "settings": {
                "followRedirect": true,
                "network": "tcp,udp"
            },
            "sniffing": {
                "destOverride": [
                    "http",
                    "tls"
                ],
                "enabled": true
            },
            "streamSettings": {
                "sockopt": {
                    "tproxy": "tproxy"
                }
            },
            "tag": "transparent"
        },
        {
            "port": 1080,
            "protocol": "socks",
            "settings": {
                "auth": "noauth"
            },
            "sniffing": {
                "destOverride": [
                    "http",
                    "tls"
                ],
                "enabled": true
            }
        }
    ]
}
'''
    config = json.loads(basic_raw_config)
    return config

def gen_direct(node: Node) -> dict:
    direct_raw_config = '''
{
	"outbounds": [
		{
			"protocol": "freedom",
			"settings": {},
			"streamSettings": {
				"sockopt": {
					"mark": 255
				}
			}
		}
	]
}'''
    config = json.loads(direct_raw_config)
    return config

def gen_proxy_outbands(node: Node) -> dict:
    proxy_global_raw_config = '''
{
    "outbounds": [
        {
            "mux": {
                "enabled": true
            },
            "protocol": "vmess",
            "settings": {
                "vnext": [
                    {
                        "address": "<str:add>",
                        "port": "<int:port>",
                        "users": [
                            {
                                "alterId": "<int:aid>",
                                "id": "<str:id>",
                                "level": 0,
                                "security": "aes-128-gcm"
                            }
                        ]
                    }
                ]
            },
            "streamSettings": {
                "network": "<str:net>",
                "security": "<str:tls>",
                "sockopt": {
                    "mark": 255
                },
                "wsSettings": {
                    "headers": {
                        "host": "<str:host>"
                    },
                    "path": "<str:path>"
                },
                "tlsSettings": {
                    "allowInsecure": true,
                    "serverName": "<str:host>"
                }
            },
            "tag": "proxy"
        },
        {
            "protocol": "freedom",
            "settings": {
                "domainStrategy": "UseIP"
            },
            "streamSettings": {
                "sockopt": {
                    "mark": 255
                }
            },
            "tag": "direct"
        },
        {
            "protocol": "blackhole",
            "settings": {
                "response": {
                    "type": "http"
                }
            },
            "tag": "block"
        },
        {
            "protocol": "dns",
            "streamSettings": {
                "sockopt": {
                    "mark": 255
                }
            },
            "tag": "dns-out"
        }
    ]
}'''

    config = json.loads(proxy_global_raw_config)
    server = config['outbounds'][0]['settings']['vnext'][0]
    server['address'] = node.add
    server['port'] = int(node.port)
    user = server['users'][0]
    user['id'] = node.id
    user['alterId'] = int(node.aid)

    stream_settings = config['outbounds'][0]['streamSettings']
    if (len(node.tls)):
        stream_settings['security'] = node.tls
        stream_settings['tlsSettings']['serverName'] = node.host
    else:
        stream_settings['security'] = 'none'
        stream_settings['tlsSettings']['serverName'] = ''

    stream_settings['network'] = node.net
    if node.net == 'ws':
        stream_settings['wsSettings']['headers']['host'] = node.host
        stream_settings['wsSettings']['path'] = node.path

    return config

def gen_proxy_global(node: Node, advance_config: V2RayUserConfig.AdvanceConfig) -> dict:
    proxy_global_raw_config = '''
{	
    "dns": {
        "servers": [
            "<str:remote_dns>",
            {
                "address": "<str:local_dns>",
                "domains": [
                    "ntp.org",
                    "geosite:speedtest",
                    "<str:add>"
                ],
                "port": 53
            }
        ]
    },
    "routing": {
		"domainStrategy": "IPOnDemand",
		"rules": [{
				"inboundTag": [
					"transparent"
				],
				"network": "udp",
				"outboundTag": "dns-out",
				"port": 53,
				"type": "field"
			},
			{
				"inboundTag": [
					"transparent"
				],
				"network": "udp",
				"outboundTag": "direct",
				"port": 123,
				"type": "field"
			},
			{
				"domain": [
					"geosite:category-ads-all"
				],
				"outboundTag": "block",
				"type": "field"
			},
			{
				"outboundTag": "direct",
				"protocol": [
					"bittorrent"
				],
				"type": "field"
			},
			{
				"ip": [
					"geoip:private"
				],
				"outboundTag": "direct",
				"type": "field"
			}
		]
	}
}'''
    config = json.loads(proxy_global_raw_config)
    update_dns_config(config, advance_config)
    config['dns']['servers'][1]['domains'][2] = node.add

    config.update(gen_proxy_outbands(node))
    return config

def gen_proxy_auto(node: Node, advance_config: V2RayUserConfig.AdvanceConfig) -> dict:
    proxy_auto_raw_config = '''
{
	"dns": {
		"servers": [
			"<str:remote_dns>",
			{
				"address": "<str:local_dns>",
				"domains": [
					"geosite:cn",
					"ntp.org",
					"geosite:speedtest",
					"<str:add>"
				],
				"port": 53
			}
		]
	},
	"routing": {
		"domainStrategy": "IPOnDemand",
		"rules": [{
				"inboundTag": [
					"transparent"
				],
				"network": "udp",
				"outboundTag": "dns-out",
				"port": 53,
				"type": "field"
			},
			{
				"inboundTag": [
					"transparent"
				],
				"network": "udp",
				"outboundTag": "direct",
				"port": 123,
				"type": "field"
			},
			{
				"domain": [
					"geosite:category-ads-all"
				],
				"outboundTag": "block",
				"type": "field"
			},
			{
				"outboundTag": "direct",
				"protocol": [
					"bittorrent"
				],
				"type": "field"
			},
			{
				"ip": [
					"geoip:private",
					"geoip:cn"
				],
				"outboundTag": "direct",
				"type": "field"
			},
			{
				"domain": [
					"geosite:cn"
				],
				"outboundTag": "direct",
				"type": "field"
			}
		]
	}
}
'''
    config = json.loads(proxy_auto_raw_config)
    update_dns_config(config, advance_config)
    config['dns']['servers'][1]['domains'][3] = node.add

    config.update(gen_proxy_outbands(node))
    return config

def update_local_dns_config(config:dict, local_dns:str):
    config['dns']['servers'][1]['address'] = local_dns

    local_rule_raw = '''
{
    "ip": [
        "223.5.5.5"
    ],
    "outboundTag": "direct",
    "type": "field"
}'''
    local_dns_rule = json.loads(local_rule_raw)
    local_dns_rule['ip'][0] = local_dns

    rules : list = config['routing']['rules']
    rules.append(local_dns_rule)

def update_remote_dns_config(config:dict, remote_dns:str):
    config['dns']['servers'][0] = remote_dns
    remote_rule_raw = '''
{
    "ip": [
        "8.8.8.8"
    ],
    "outboundTag": "proxy",
    "type": "field"
}
'''
    remote_dns_rule = json.loads(remote_rule_raw)
    remote_dns_rule['ip'][0] = remote_dns

    rules : list = config['routing']['rules']
    rules.append(remote_dns_rule)

def update_dns_config(config:dict, advance_config:V2RayUserConfig.AdvanceConfig):
    if len(advance_config.dns.local):
        update_local_dns_config(config, advance_config.dns.local)
    else:
        update_local_dns_config(config, advance_config.dns.default_local)

    if len(advance_config.dns.remote):
        update_remote_dns_config(config, advance_config.dns.remote)
    else:
        update_remote_dns_config(config, advance_config.dns.default_remote)
