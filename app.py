#!/usr/bin/env python3
"""
NetVision-Dashboard - Flask Backend
"""

from flask import Flask, render_template, jsonify
import yaml
import threading
import time
from snmp_utils import (
    get_system_name, get_system_description, get_switch_ports_info,
    get_uplink_ports, get_interface_octets
)
from network_speed import SpeedMonitor

app = Flask(__name__)

# بارگذاری تنظیمات
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

switches = config['switches']
poll_interval = config.get('poll_interval', 3)
vlan_mapping = config.get('vlan_mapping', {})

# دیکشنری برای نگهداری آخرین اطلاعات
switch_data = {}
speed_monitors = {}

def poll_switches():
    """تابع poll در یک نخ جداگانه برای به‌روزرسانی داده‌ها"""
    global switch_data, speed_monitors
    while True:
        for switch in switches:
            ip = switch['ip']
            community = switch['community']
            name = switch.get('name', ip)

            try:
                # دریافت اطلاعات پایه
                sys_name = get_system_name(ip, community)
                sys_desc = get_system_description(ip, community)
                ports = get_switch_ports_info(ip, community, num_ports=48)
                uplinks = get_uplink_ports(ip, community, uplink_indices=[47,48,49,50])

                # محاسبه سرعت از اینترفیس اول (مثلاً پورت 1)
                if ip not in speed_monitors:
                    speed_monitors[ip] = SpeedMonitor(ip, community, interface_index=1)
                in_speed, out_speed = speed_monitors[ip].get_current_speed()

                switch_data[ip] = {
                    'name': name,
                    'sys_name': sys_name,
                    'sys_desc': sys_desc,
                    'ports': ports,
                    'uplinks': uplinks,
                    'in_speed': in_speed,
                    'out_speed': out_speed,
                    'last_update': time.time()
                }
            except Exception as e:
                print(f"Error polling {ip}: {e}")
                # در صورت خطا، داده‌های قبلی را نگه داریم
                pass
        time.sleep(poll_interval)

# راه‌اندازی نخ poll
threading.Thread(target=poll_switches, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html', switches=switches)

@app.route('/api/data')
def get_data():
    """API برای دریافت داده‌های به‌روز"""
    return jsonify(switch_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
