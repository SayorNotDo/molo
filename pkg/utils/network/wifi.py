import datetime
import socket
import subprocess
import re
import sys

import speedtest
import threading


def get_cur_system():
    if sys.platform.startswith('win'):
        return 'Windows'
    elif sys.platform.startswith('darwin'):
        return 'macOS'
    elif sys.platform.startswith('linux'):
        return 'Linux'
    elif sys.platform.startswith('freebsd'):
        return 'FreeBSD'
    else:
        return 'Unknown'


def get_wifi_name(os_name=None):
    # 使用操作系统的网络管理工具获取当前连接的wifi名称
    if os_name == 'Linux':
        return subprocess.run(['iwgetid', '-r'], capture_output=True, text=True).stdout.strip()
    elif os_name == 'macOS':
        result = subprocess.run(['networksetup', '-getairportnetwork', 'en0'], capture_output=True, text=True).stdout
        ssid_match = re.search(r'Current Wi-Fi Network:\s(.+)', result)
        if ssid_match:
            return ssid_match.group(1).strip()
        return None
    elif os_name == 'Windows':
        result = subprocess.run(['netsh', 'wlan', 'show', 'interface'], capture_output=True, text=True).stdout
        ssid_match = re.search(r'SSID\s+:\s(.+)', result)
        if ssid_match:
            return ssid_match.group(1).strip()
        return None


def get_ip_addr(os_name=None, wifi_name=None):
    ip_address = ''
    if os_name == 'Linux':
        result = subprocess.run(["ip", "addr", "show", wifi_name], capture_output=True, text=True)
        ip_address = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/\d+', result.stdout).group(1)
    elif os_name == 'macOS':
        result = subprocess.run(["networksetup", "-getinfo", "Wi-Fi"], capture_output=True, text=True).stdout
        ip_address = re.search(r'IP address: (\d+\.\d+\.\d+\.\d+)', result).group(1)
    elif os_name == 'Windows':
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
    return ip_address


def get_wifi_info(call_func: callable, **kwargs):
    # 初始化Speedtest对象
    server = None
    speed_test = speedtest.Speedtest()

    # 获取当前操作系统
    os_name = get_cur_system()

    # 获取当前wifi名称
    wifi_name = get_wifi_name(os_name)

    # 获取指定WIFI的IP地址
    ip_address = get_ip_addr(wifi_name=wifi_name, os_name=os_name)

    # 获取服务器列表
    speed_test.get_servers(server)
    speed_test.get_best_server()

    # 执行网络测试，通过回调返回
    def perform_speed_test(callback):
        ret = dict()
        speed_test.get_best_server()

        speed_test.download()
        speed_test.upload()

        result = speed_test.results.dict()
        ret['sampling_time'] = '%sZ' % datetime.datetime.utcnow().isoformat()
        ret['init_time'] = result['timestamp']
        ret['wifi_name'] = wifi_name
        ret['ip_address'] = ip_address
        ret['download'] = result['download'] / 1024 / 1024  # Mbps
        ret['upload'] = result['upload'] / 1024 / 1024  # Mbps
        ret['ping'] = result['ping']
        ret['server'] = result['server']
        ret['client'] = result['client']
        ret['bytes_sent'] = result['bytes_sent']
        ret['bytes_received'] = result['bytes_received']

        callback(ret, **kwargs)

        timer = threading.Timer(1, perform_speed_test, [callback])
        timer.start()

    perform_speed_test(call_func)
