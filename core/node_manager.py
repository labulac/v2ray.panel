# encoding: utf-8
"""
File:       node_manager
Author:     twotrees.us@gmail.com
Date:       2020年7月29日  31周星期三 21:57
Desc:
"""

from typing import List
from typing import Dict
from datetime import datetime
import time
import json
import requests
import base64
import os
from tcp_latency import measure_latency
from concurrent import futures
from .keys import Keyword as K
from .node_item import NodeItem
from .base_data_item import BaseDataItem

class NodeGroup:
    def __init__(self):
        self.subscribe: str = ''
        self.nodes: List[NodeItem] = []

class NodeManager(BaseDataItem):
    def __init__(self):
        self.last_subscribe = ''
        self.groups: Dict= {}

    def filename(self):
        return 'config/nodes.json'

    def update_group(self, group: NodeGroup):
        url = group.subscribe
        r = requests.get(url)
        list = r.text
        list = base64.b64decode(list).decode('utf8')

        group.nodes.clear()
        for line in list.splitlines():
            if line.startswith(K.vmess_scheme):
                line = line[len(K.vmess_scheme):]
                line = base64.b64decode(line).decode('utf8')
                data = json.loads(line)
                node = NodeItem().load_data(data)
                group.nodes.append(node)

    def update(self, url):
        group = self.groups[url]
        self.update_group(group)

    def update_all(self):
        for url in self.groups.keys():
            group = self.groups[url]
            self.update_group(group)

        self.refresh_update_time()
        self.save()

    def add_subscribe(self, url):
        group = NodeGroup()
        group.subscribe = url
        self.update_group(group)
        self.groups[url] = group

        self.refresh_update_time()
        self.save()

    def remove_subscribe(self, url):
        self.groups.pop(url)
        self.save()

    def delete_node(self, url, index):
        group = self.groups[url]
        group.nodes.pop(index)
        self.save()

    def all_nodes(self) ->list :
        nodes = []
        for url in self.groups.keys():
            group = self.groups[url]
            nodes.extend(group.nodes)
        return nodes

    def refresh_update_time(self):
        self.last_subscribe = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def ping_test_all(self) -> list :
        results = []

        def ping(host, port):
            delay = measure_latency(host, port, 1)[0]
            return delay

        for url in self.groups.keys():
            group: NodeGroup = self.groups[url]
            with futures.ThreadPoolExecutor(max_workers=len(group.nodes)) as executor:
                futures_to_hosts = {}
                for node in group.nodes:
                    future = executor.submit(ping, node.add, node.port)
                    futures_to_hosts[future] = node.ps
                futures.wait(futures_to_hosts.keys())

                group_result = {}
                group_result[K.subscribe] = url
                nodes = {}
                for future in futures_to_hosts.keys():
                    delay = future.result()
                    if delay == None:
                        delay = -1
                    nodes[futures_to_hosts[future]] = int(delay)

                group_result[K.nodes] = nodes
                results.append(group_result)

        return results