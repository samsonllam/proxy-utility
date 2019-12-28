import time

import js2py
import loguru
import pyquery
import requests

def getProxiesFromProxyNova():
    proxies = []
    # 按照網站規則使用各國代碼傳入網址取得各國 IP 代理
    countries = [
        'tw',
        'jp',
        'kr',
        'id',
        'my',
        'th',
        'vn',
        'ph',
        'hk',
        'uk',
        'us'
    ]
    for country in countries:
        url = f'https://www.proxynova.com/proxy-server-list/country-{country}/'
        loguru.logger.debug(f'getProxiesFromProxyNova: {url}')
        loguru.logger.warning(f'getProxiesFromProxyNova: downloading...')
        response = requests.get(url)
        if response.status_code != 200:
            loguru.logger.debug(f'getProxiesFromProxyNova: status code is not 200')
            continue
        loguru.logger.success(f'getProxiesFromProxyNova: downloaded.')
        d = pyquery.PyQuery(response.text)
        table = d('table#tbl_proxy_list')
        rows = list(table('tbody:first > tr').items())
        loguru.logger.warning(f'getProxiesFromProxyNova: scanning...')
        for row in rows:
            tds = list(row('td').items())
            # 若為分隔行則僅有 1 格
            if len(tds) == 1:
                continue
            # 取出 IP 欄位內的 JavaScript 程式碼
            js = row('td:nth-child(1) > abbr').text()
            # 去除 JavaScript 程式碼開頭的 document.write( 字串與結尾的 ); 字串，
            # 再與可供 js2py 執行後回傳指定變數的 JavaScript 程式碼相結合
            js = 'let x = %s; x' % (js[15:-2])
            # 透過 js2py 執行取得還原後的 IP
            ip = js2py.eval_js(js).strip()
            # 取出 Port 欄位值
            port = row('td:nth-child(2)').text().strip()
            # 組合 IP 代理
            proxy = f'{ip}:{port}'
            proxies.append(proxy)
        loguru.logger.success(f'getProxiesFromProxyNova: scanned.')
        loguru.logger.debug(f'getProxiesFromProxyNova: {len(proxies)} proxies is found.')
        # 每取得一個國家代理清單就休息一秒，避免頻繁存取導致代理清單網站封鎖
        time.sleep(1)
    return proxies