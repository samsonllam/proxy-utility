import csv
import datetime
import os
import random

import loguru

from ProxySource.proxyNova import getProxiesFromProxyNova
from ProxySource.gatherProxy import getProxiesFromGatherProxy
from ProxySource.freeProxyList import getProxiesFromFreeProxyList

now = datetime.datetime.now()
proxies = []

# 隨機取出一組代理
def getProxy():
    global proxies
    # 若代理清單內已無代理，則重新下載
    if len(proxies) == 0:
        getProxies()
    proxy = random.choice(proxies)
    loguru.logger.debug(f'getProxy: {proxy}')
    proxies.remove(proxy)
    loguru.logger.debug(f'getProxy: {len(proxies)} proxies is unused.')
    return proxy

def reqProxies(hour):
    global proxies
    proxies = proxies + getProxiesFromProxyNova()
    proxies = proxies + getProxiesFromGatherProxy()
    proxies = proxies + getProxiesFromFreeProxyList()
    proxies = list(dict.fromkeys(proxies))
    loguru.logger.debug(f'reqProxies: {len(proxies)} proxies is found.')

def getProxies():
    global proxies
    hour = f'{now:%Y%m%d%H}'
    filename = f'proxies-{hour}.csv'
    filepath = f'{filename}'
    if os.path.isfile(filepath):
        loguru.logger.info(f'getProxies: {filename} exists.')
        loguru.logger.warning(f'getProxies: {filename} is loading...')
        with open(filepath, 'r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                proxy = row['Proxy']
                proxies.append(proxy)
        loguru.logger.success(f'getProxies: {filename} is loaded.')
    else:
        loguru.logger.info(f'getProxies: {filename} does not exist.')
        reqProxies(hour)
        loguru.logger.warning(f'getProxies: {filename} is saving...')
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Proxy'
            ])
            for proxy in proxies:
                writer.writerow([
                    proxy
                ])
        loguru.logger.success(f'getProxies: {filename} is saved.')
