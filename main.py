import requests
import requests.exceptions

import loguru

from ProxyFactory import getProxy

# 用於保存上一次連線請求成功時用的代理資訊
proxy = None

def testRequest():
    global proxy
    # 持續更換代理直到連線請求成功為止
    while True:
        # 若無上一次連線請求成功的代理資訊，則重新取出一組代理資訊
        if proxy is None:
            proxy = getProxy()
        try:
            url = f'https://www.google.com/'
            loguru.logger.info(f'testRequest: url is {url}')
            loguru.logger.warning(f'testRequest: downloading...')
            response = requests.get(
                url,
                # 指定 HTTPS 代理資訊
                proxies={
                    'https': f'https://{proxy}'
                },
                # 指定連限逾時限制
                timeout=5
            )
            if response.status_code != 200:
                loguru.logger.debug(f'testRequest: status code is not 200.')
                # 請求發生錯誤，清除代理資訊，繼續下個迴圈
                proxy = None
                continue
            loguru.logger.success(f'testRequest: downloaded.')
        # 發生以下各種例外時，清除代理資訊，繼續下個迴圈
        except requests.exceptions.ConnectionError:
            loguru.logger.error(f'testRequest: proxy({proxy}) is not working (connection error).')
            proxy = None
            continue
        except requests.exceptions.ConnectTimeout:
            loguru.logger.error(f'testRequest: proxy({proxy}) is not working (connect timeout).')
            proxy = None
            continue
        except requests.exceptions.ProxyError:
            loguru.logger.error(f'testRequest: proxy({proxy}) is not working (proxy error).')
            proxy = None
            continue
        except requests.exceptions.SSLError:
            loguru.logger.error(f'testRequest: proxy({proxy}) is not working (ssl error).')
            proxy = None
            continue
        except Exception as e:
            loguru.logger.error(f'testRequest: proxy({proxy}) is not working.')
            loguru.logger.error(e)
            proxy = None
            continue
        # 成功完成請求，離開迴圈
        break

if __name__ == '__main__':
    testRequest()