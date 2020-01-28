import asyncio
import random
import time
import traceback
from queue import Queue
from threading import Thread
import logging


log = logging.getLogger(__name__)


class Borrower:
    def __init__(self, proxies):
        self.proxies = proxies
        self.proxy = None
        self.start = None

    def __enter__(self):
        self.proxy = self.proxies.get()
        self.start = time.time()
        return self.proxy

    def __exit__(self, exc_type, exc_value, tb):
        if exc_value is not None:
            exc_value.errmsg = str(exc_value)
        self.proxy.log('', stime=self.start, err=exc_value)
        self.proxies.put_back(self.proxy)


class Proxies:

    def __init__(self, cost_threshold=5, proxy_count_threshold=4000, types=[('HTTP', ('Anonymous', 'High'))]):
        self.cost_threshold = cost_threshold
        self.proxy_count_threshold = proxy_count_threshold
        self.types = types
        self.proxies = Queue()
        self.bad_proxies = Queue()
        self.running = True
        self.thread = Thread(target=self._collect, daemon=True)
        self.thread.start()

    def _collect(self):
        self.loop = loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        import proxybroker

        async def show(proxies):
            while True:
                try:
                    proxy = await proxies.get()
                    if proxy is None:
                        log.info('Proxy search complete found: %s' % self.proxies.qsize())
                        break
                    # log.info('Found proxy: %s (%s)' % (proxy, self.proxies.qsize()))
                    proxy._runtimes = proxy._runtimes[:1]
                    self.proxies.put(proxy)
                except:
                    traceback.print_exc()

        while self.running:
            if self.proxies.qsize() < self.proxy_count_threshold:
                log.info('Got less that {} proxies, getting more'.format(self.proxy_count_threshold))
                queue = asyncio.Queue()
                broker = proxybroker.Broker(queue)
                random.seed()
                random.shuffle(broker._providers)
                tasks = asyncio.gather(
                    broker.find(types=self.types, limit=0),
                    show(queue))

                loop.run_until_complete(tasks)
            time.sleep(1)

    def borrow(self):
        return Borrower(self)

    def get(self):
        proxy = self.proxies.get()
        log.info('Got proxy {}'.format(proxy))
        return proxy

    def put_back(self, proxy):
        if sum(proxy.stat['errors'].values()) > 3:
            self.bad_proxies.put(proxy)
        else:
            self.proxies.put(proxy)
        log.info('Putting back proxy {} {}/{}(bad)'.format(proxy, self.proxies.qsize(), self.bad_proxies.qsize()))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    proxies = Proxies()
    a = proxies.get()
    print(a)
    time.sleep(1000)
