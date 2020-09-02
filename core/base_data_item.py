# encoding: utf-8
"""
File:       base_data_item
Author:     twotrees.us@gmail.com
Date:       2020年7月29日  31周星期三 21:45
Desc:
"""
import json
import os.path
import jsonpickle

class BaseDataItem:
    def filename(self):
        return ''

    def dump(self, pure=True):
        data = json.loads(jsonpickle.encode(self, unpicklable=not pure))
        return data

    def load(self):
        if os.path.exists(self.filename()):
            with open(self.filename()) as f:
                return jsonpickle.decode(f.read())
        return self

    def load_data(self, data: dict):
        pickle_data: dict = self.dump(pure=False)
        pickle_data.update(data)
        return jsonpickle.decode(json.dumps(pickle_data))

    def save(self):
        raw = jsonpickle.encode(self, indent=4)
        with open(self.filename(), 'w+') as f:
            f.write(raw)