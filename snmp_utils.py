#!/usr/bin/env python3
"""
SNMP Utilities for Cisco Switch Monitoring
"""

from pysnmp.hlapi import *
import re

def get_snmp_data(ip, community, oid):
    """دریافت یک OID از دستگاه SNMP"""
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )
    if error_indication:
        return None
    if error_status:
        return None
    return var_binds[0][1].prettyPrint()

def get_interface_status(ip, community, if_index):
    """دریافت وضعیت یک اینترفیس (1=up, 2=down)"""
    oid = f"1.3.6.1.2.1.2.2.1.8.{if_index}"
    value = get_snmp_data(ip, community, oid)
    return value == '1'  # True if up

def get_interface_name(ip, community, if_index):
    """دریافت نام اینترفیس (مثلاً GigabitEthernet0/1)"""
    oid = f"1.3.6.1.2.1.2.2.1.2.{if_index}"
    return get_snmp_data(ip, community, oid)

def get_interface_speed(ip, community, if_index):
    """دریافت سرعت اینترفیس (bps)"""
    oid = f"1.3.6.1.2.1.2.2.1.5.{if_index}"
    return int(get_snmp_data(ip, community, oid) or 0)

def get_interface_octets(ip, community, if_index):
    """دریافت تعداد بایت‌های ورودی/خروجی"""
    oid_in = f"1.3.6.1.2.1.2.2.1.10.{if_index}"   # ifInOctets
    oid_out = f"1.3.6.1.2.1.2.2.1.16.{if_index}"  # ifOutOctets
    in_bytes = get_snmp_data(ip, community, oid_in)
    out_bytes = get_snmp_data(ip, community, oid_out)
    return int(in_bytes or 0), int(out_bytes or 0)

def get_switch_ports_info(ip, community, num_ports=48):
    """دریافت اطلاعات تمام پورت‌های سوئیچ"""
    ports = []
    for i in range(1, num_ports + 1):
        status = get_interface_status(ip, community, i)
        name = get_interface_name(ip, community, i)
        speed = get_interface_speed(ip, community, i)
        ports.append({
            'index': i,
            'name': name or f'Gig0/{i}',
            'status': status,
            'speed': speed,
            'vlan': get_vlan_for_port(ip, community, i)  # تابع بعدی
        })
    return ports

def get_vlan_for_port(ip, community, if_index):
    """دریافت VLAN یک پورت (از جدول dot1q)"""
    oid = f"1.3.6.1.2.1.17.7.1.4.2.1.3.{if_index}"
    vlan = get_snmp_data(ip, community, oid)
    return vlan or '1'

def get_uplink_ports(ip, community, uplink_indices=[47,48,49,50]):
    """دریافت وضعیت پورت‌های آپلینک"""
    uplinks = []
    for idx in uplink_indices:
        status = get_interface_status(ip, community, idx)
        name = get_interface_name(ip, community, idx)
        speed = get_interface_speed(ip, community, idx)
        uplinks.append({
            'index': idx,
            'name': name or f'Uplink{idx}',
            'status': status,
            'speed': speed
        })
    return uplinks

def get_system_name(ip, community):
    """دریافت نام دستگاه (sysName)"""
    oid = '1.3.6.1.2.1.1.5.0'
    return get_snmp_data(ip, community, oid) or 'Unknown'

def get_system_description(ip, community):
    """دریافت توضیحات دستگاه (sysDescr)"""
    oid = '1.3.6.1.2.1.1.1.0'
    return get_snmp_data(ip, community, oid) or 'Unknown'
