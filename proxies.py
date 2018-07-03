import sys
import asyncio
import time
import traceback
from collections import deque
from queue import Queue
from threading import Thread
import logging


log = logging.getLogger(__name__)


class Proxies:

    def __init__(self, cost_threshold=5, proxy_count_threshold=10, proxy_count=100):
        self.cost_threshold = cost_threshold
        self.proxy_count_threshold = proxy_count_threshold
        self.proxy_count = proxy_count

        self.proxies = Queue()
        self.bad_proxies = Queue()
        self.running = True
        self.thread = Thread(target=self._collect, daemon=True)
        self.thread.start()

    def _collect(self):
        self.loop = loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        import proxybroker
        from proxybroker.providers import Tools_rosinstrument_com_socks, Tools_rosinstrument_com

        judges = None  # ['https://proxyjudge.info/', 'http://proxyjudge.info/']
        providers = None  # ['http://www.proxylists.net/', 'https://www.sslproxies.org/']

        async def show(proxies):
            while True:
                try:
                    proxy = await proxies.get()
                    if proxy is None:
                        log.info('Proxy search complete found: %s' % self.proxies.qsize())
                        break
                    log.info('Found proxy: %s (%s)' % (proxy, self.proxies.qsize()))
                    self.proxies.put(proxy)
                except:
                    traceback.print_exc()

        while self.running:
            if self.proxies.qsize() < self.proxy_count_threshold:
                log.info('Got less that {} proxies, getting more'.format(self.proxy_count_threshold))
                queue = asyncio.Queue()
                broker = proxybroker.Broker(queue, judges=judges, providers=providers)
                tasks = asyncio.gather(
                    broker.find(types=['SOCKS5']),
                    show(queue))

                loop.run_until_complete(tasks)
            time.sleep(1)

    def get(self):
        log.info('Getting proxy')
        return self.proxies.get()

    def put_back(self, proxy, cost):
        if cost > self.cost_threshold:
            self.bad_proxies.put(proxy)
        else:
            self.proxies.put(proxy)
        log.info('Putting back proxy {} with cost: {:.2f} {}/{}(bad)'.format(proxy, cost, self.proxies.qsize(), self.bad_proxies.qsize()))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    proxies = Proxies()
    a = proxies.get()
    print(a)
    time.sleep(1000)
