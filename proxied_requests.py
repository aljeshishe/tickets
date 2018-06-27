import logging
import time
import requests
from proxies import Proxies

log = logging.getLogger(__name__)


class Requests:
    def __init__(self):
        self.proxies = Proxies()

    def request(self, method, url, **kwargs):
        for i in range(5):
            proxy = self.proxies.get()
            try:
                start = time.time()
                kwargs['proxies'] = dict(http='socks5://%s:%s' % (proxy.host, proxy.port),
                                         https='socks5://%s:%s' % (proxy.host, proxy.port))
                kwargs['timeout'] = (5, 10)
                response = requests.request(method=method, url=url, **kwargs)
                seconds = time.time() - start
                log.info('Using %s %s %s %3.3f' % (proxy, response.status_code, len(response.content), seconds))
                self.proxies.put_back(proxy, seconds)
                return response
            except Exception as e:
                self.proxies.put_back(proxy, 100)
                log.error('Got exception %s try(%s/%s)' % (e, i + 1, 5))
                if i == 4:
                    raise

    def get(self, url, params=None, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self.request('get', url, params=params, **kwargs)

    def options(self, url, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self.request('options', url, **kwargs)

    def head(self, url, **kwargs):
        kwargs.setdefault('allow_redirects', False)
        return self.request('head', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request('post', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request('put', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request('patch', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('delete', url, **kwargs)

if __name__=='__main__':
    response = Requests().get('https://ya.ru')
    print(response, response.content)
