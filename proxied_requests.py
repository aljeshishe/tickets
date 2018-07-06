import logging
import time
import requests
from proxies import Proxies

log = logging.getLogger(__name__)


class Requests:
    def __init__(self):
        self.proxies = Proxies()

    def request(self, method, url, **kwargs):
        exception = None
        TRIES = 10
        for i in range(TRIES):
            try:
                with self.proxies.borrow() as proxy:
                    kwargs['proxies'] = dict(http='https://%s:%s' % (proxy.host, proxy.port),
                                             https='https://%s:%s' % (proxy.host, proxy.port))
                    kwargs['timeout'] = (10, 20)
                    response = requests.request(method=method, url=url, **kwargs)
                    response.json() # avoiding incorrect json even if 200
                    return response
            except Exception as e:
                log.warning('Got exception %s try(%s/%s)' % (e, i + 1, TRIES))
                exception = e
        raise exception

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
