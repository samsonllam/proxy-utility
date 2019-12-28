import re
import time
import urllib.parse

import json
import loguru
import pyquery
import requests

def getProxiesFromGatherProxy():
    proxies = []
    # 按照網站規則使用各國國名傳入網址取得各國 IP 代理
    countries = [
        'Taiwan',
        'Japan',
        'United States',
        'Thailand',
        'Vietnam',
        'Indonesia',
        'Singapore',
        'Philippines',
        'Malaysia',
        'Hong Kong'
    ]
    for country in countries:
        url = f'http://www.gatherproxy.com/proxylist/country/?c={urllib.parse.quote(country)}'
        loguru.logger.debug(f'getProxiesFromGatherProxy: {url}')
        loguru.logger.warning(f'getProxiesFromGatherProxy: downloading...')
        response = requests.get(url)
        if response.status_code != 200:
            loguru.logger.debug(f'getProxiesFromGatherProxy: status code is not 200')
            continue
        loguru.logger.success(f'getProxiesFromGatherProxy: downloaded.')
        d = pyquery.PyQuery(response.text)
        scripts = list(d('table#tblproxy > script').items())
        loguru.logger.warning(f'getProxiesFromGatherProxy: scanning...')
        for script in scripts:
            # 取出 script 標簽中的 JavaScript 原始碼
            script = script.text().strip()
            # 去除 JavaScript 程式碼開頭的 gp.insertPrx( 字串與結尾的 ); 字串
            script = re.sub(r'^gp\.insertPrx\(', '', script)
            script = re.sub(r'\);$', '', script)
            # 將參數物件以 JSON 方式解析
            script = json.loads(script)
            # 取出 IP 欄位值
            ip = script['PROXY_IP'].strip()
            # 取出 Port 欄位值，並從 16 進位表示法解析為 10 進位表示法
            port = int(script['PROXY_PORT'].strip(), 16)
            # 組合 IP 代理
            proxy = f'{ip}:{port}'
            proxies.append(proxy)
        loguru.logger.success(f'getProxiesFromGatherProxy: scanned.')
        loguru.logger.debug(f'getProxiesFromGatherProxy: {len(proxies)} proxies is found.')
        # 每取得一個國家代理清單就休息一秒，避免頻繁存取導致代理清單網站封鎖
        time.sleep(1)
    return proxies