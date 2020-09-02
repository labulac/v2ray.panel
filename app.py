#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, jsonify, request
from flask_basicauth import BasicAuth

from core.keys import Keyword as K
from core.core_service import CoreService

CoreService.load()
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

app = Flask(__name__, static_url_path='/static')
app.config['BASIC_AUTH_USERNAME'] = CoreService.app_config.user
app.config['BASIC_AUTH_PASSWORD'] = CoreService.app_config.password
app.config['BASIC_AUTH_FORCE'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
basic_auth = BasicAuth(app)

@app.route('/')
@app.route('/index.html')
def index_page():
    return render_template("index.html")

@app.route('/status.html')
def status_page():
    return render_template("status.html")

@app.route('/subscribe.html')
def subscribe_page():
    return render_template("subscribe.html")

@app.route('/advance.html')
def advance_page():
    return render_template("advance.html")

@app.route('/log.html')
def log_page():
    return render_template("log.html")

@app.route('/start_service')
def start_service_api():
    result = K.failed
    if CoreService.v2ray.start():
        result = K.ok

    return jsonify({ K.result : result })

@app.route('/stop_service')
def stop_service_api():
    result = K.failed
    if CoreService.v2ray.stop():
        result = K.ok
    return jsonify({K.result: result})

@app.route('/restart_service')
def restart_service_api():
    result = K.failed
    if CoreService.v2ray.restart():
        result = K.ok
    return jsonify({K.result: result})

@app.route('/get_status')
def get_status_api():
    status = CoreService.status()
    status.update({K.result: K.ok})
    return jsonify(status)

@app.route('/get_performance')
def get_performance_api():
    performance = CoreService.performance()
    performance.update({K.result: K.ok})
    return jsonify(performance)

@app.route('/check_v2ray_new_ver')
def check_v2ray_new_ver_api():
    version = CoreService.v2ray.check_new_version()
    return jsonify({
        K.result : K.ok,
        K.version : version})

@app.route('/update_v2ray')
def update_v2ray_api():
    success = CoreService.v2ray.update()
    result = K.failed
    if success:
        result = K.ok
    return jsonify({K.result:result})

@app.route('/switch_proxy_mode')
def switch_proxy_mode_api():
    mode = request.args.get('mode')
    mode = int(mode)
    success = CoreService.switch_mode(mode)
    result = K.failed
    if success:
        result = K.ok
    return jsonify({K.result: result})

@app.route('/add_subscribe')
def add_subscribe_api():
    result = K.failed
    try:
        url = request.args.get(K.subscribe)
        CoreService.node_manager.add_subscribe(url)
        result = K.ok
    except:
        pass

    return jsonify({K.result : result})

@app.route('/add_manual_node')
def add_manual_node_api():
    result = K.failed
    try:
        url = request.args.get(K.url)
        CoreService.node_manager.add_manual_node(url)
        result = K.ok
    except:
        pass

    return jsonify({K.result : result})

@app.route('/remove_subscribe')
def remove_subscribe_api():
    result = K.failed
    try:
        url = request.args.get(K.subscribe)
        CoreService.node_manager.remove_subscribe(url)
        result = K.ok
    except:
        pass

    return jsonify({K.result: result})

@app.route('/update_all_subscribe')
def update_all_subscribe_api():
    result = K.failed
    try:
        CoreService.node_manager.update_all()
        result = K.ok
    except:
        pass
    return jsonify({K.result: result})

@app.route('/update_subscribe')
def update_subscribe_api():
    result = K.failed
    try:
        url = request.args.get(K.subscribe)
        CoreService.node_manager.update(url)
        result = K.ok
    except:
        pass
    return jsonify({K.result: result})

@app.route('/subscribe_list')
def subscribe_list_api():
    list = CoreService.node_manager.dump()
    status = CoreService.status()
    list.update(status)
    list.update({K.result : K.ok})
    return jsonify(list)

@app.route('/subscribe_ping_all')
def subscribe_ping_all_api():
    groups = CoreService.node_manager.ping_test_all()
    return jsonify({K.result : K.ok,
                    K.groups : groups})

@app.route('/apply_node')
def apply_node_api():
    url = request.args.get(K.subscribe)
    index = request.args.get(K.node_index)
    index = int(index)
    result = K.failed
    if CoreService.apply_node(url, index):
        result = K.ok

    return jsonify({K.result: result})

@app.route('/get_node_link')
def get_node_link_api():
    url = request.args.get(K.subscribe)
    index = request.args.get(K.node_index)
    index = int(index)
    link = CoreService.node_manager.find_node(url, index).link
    return jsonify({ K.result: K.ok,
                     K.node_link: link})

@app.route('/delete_node')
def delete_node_api():
    url = request.args.get(K.subscribe)
    index = request.args.get(K.node_index)
    index = int(index)
    CoreService.node_manager.delete_node(url, index)
    return jsonify({K.result: K.ok})

@app.route('/get_user_config')
def get_user_config_api():
    config = CoreService.user_config.dump()
    config.update({ K.result: K.ok})
    return jsonify(config)

@app.route('/advance_set_dns')
def advance_set_dns_api():
    local_dns = request.args.get('local')
    remote_dns = request.args.get('remote')

    if local_dns != None:
        if not CoreService.set_local_dns(local_dns):
            return jsonify({ K.result : K.failed })

    if remote_dns != None:
        if not CoreService.set_remote_dns(remote_dns):
            return jsonify({K.result: K.failed})

    return jsonify({ K.result : K.ok })

@app.route('/get_access_log')
def get_access_log_api():
    return CoreService.v2ray.access_log()

@app.route('/get_error_log')
def get_error_log_api():
    return CoreService.v2ray.error_log()

app.run(host='0.0.0.0', port=CoreService.app_config.port)
