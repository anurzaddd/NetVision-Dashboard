# 🌐 NetVision-Dashboard

> **Real-time Network Monitoring Dashboard for Cisco Switches**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Flask](https://img.shields.io/badge/Flask-2.2+-green)](https://flask.palletsprojects.com/)
[![SNMP](https://img.shields.io/badge/SNMP-Cisco-red)](https://www.cisco.com/)

---

## 🚀 What is NetVision-Dashboard?

**NetVision-Dashboard** is a web-based network monitoring tool that:

- 📊 **Real-time speed monitoring** (in/out Mbps) with live charts
- 🔌 **Cisco switch port status** (up/down) with VLAN information
- 🔗 **Uplink port status** for each switch (ports 47-50)
- 🎨 **Beautiful, user-friendly interface** with modern colors
- ⚡ **Auto-refresh every 3 seconds**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🖥️ **Web Dashboard** | Accessible via any browser (Chrome recommended) |
| 📈 **Live Speed Graph** | Shows incoming/outgoing traffic in real-time |
| 🔍 **Switch Discovery** | Monitor multiple Cisco switches |
| 📋 **Port Status** | Each port (1-48) shows active/inactive with VLAN tag |
| 🔗 **Uplink Monitoring** | Check status of 4 uplink ports per switch |
| 🎯 **VLAN Mapping** | Automatically displays VLAN per port |
| 🌐 **SNMP Polling** | Fetches data via SNMP v2c |

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/anurzaddd/NetVision-Dashboard.git
cd NetVision-Dashboard
