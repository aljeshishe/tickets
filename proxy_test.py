import asyncio
import logging
from proxybroker import Broker

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d|%(levelname)-4.4s|%(thread)-6.6s|%(funcName)-10.10s|%(message)s',
                    handlers=[logging.FileHandler("example1.log"),
                              logging.StreamHandler()])
# import warnings
# warnings.resetwarnings()

log = logging.getLogger(__name__)


async def show(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        log.info('Found proxy: %s' % proxy)


proxies = asyncio.Queue()
broker = Broker(proxies, max_conn=300)
tasks = asyncio.gather(
    # broker.find(types=['HTTP', 'HTTPS', 'SOCKS4', 'SOCKS5', 'CONNECT:80', 'CONNECT:25']),
    broker.find(types=['HTTPS'], limit=100),
    show(proxies))

loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)
