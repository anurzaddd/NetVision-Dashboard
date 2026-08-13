#!/usr/bin/env python3
"""
Network Speed Monitoring using SNMP ifOctets
"""

import time
from snmp_utils import get_interface_octets

class SpeedMonitor:
    def __init__(self, switch_ip, community, interface_index=1):
        self.switch_ip = switch_ip
        self.community = community
        self.interface_index = interface_index
        self.prev_in = None
        self.prev_out = None
        self.prev_time = None

    def get_current_speed(self):
        """دریافت سرعت لحظه‌ای ورودی/خروجی (Mbps)"""
        in_bytes, out_bytes = get_interface_octets(
            self.switch_ip, self.community, self.interface_index
        )
        current_time = time.time()

        if self.prev_in is None:
            self.prev_in = in_bytes
            self.prev_out = out_bytes
            self.prev_time = current_time
            return 0, 0

        time_diff = current_time - self.prev_time
        if time_diff < 0.1:
            return 0, 0

        in_bps = (in_bytes - self.prev_in) * 8 / time_diff
        out_bps = (out_bytes - self.prev_out) * 8 / time_diff

        self.prev_in = in_bytes
        self.prev_out = out_bytes
        self.prev_time = current_time

        # تبدیل به Mbps
        in_mbps = in_bps / 1_000_000
        out_mbps = out_bps / 1_000_000

        return round(in_mbps, 2), round(out_mbps, 2)
