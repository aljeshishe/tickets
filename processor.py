import traceback
from queue import Queue
from threading import Thread
import logging

log = logging.getLogger(__name__)


class Processor:
    POISON_PILL = 'POISON_PILL'

    def __init__(self, threads=1):
        self.results = []
        self.threads = []
        self.tasks = Queue()
        for i in range(threads):
            thread = Thread(target=self._thread_func)
            thread.start()
            self.threads.append(thread)

    def __len__(self):
        return self.tasks.qsize()

    def _thread_func(self):
        while True:
            task = self.tasks.get()
            if task == self.POISON_PILL:
                return
            try:
                task()
            except Exception:
                traceback.print_exc()
            finally:
                self.tasks.task_done()

    def add(self, task):
        self.tasks.put(task)

    def wait_done(self):
        self.tasks.join()
        print('all done')

    def stop(self):
        for thread in self.threads:
            self.add(self.POISON_PILL)

        for thread in self.threads:
            thread.join()
        print('stopped')

    def run(self, tasks):
        for task in tasks:
            self.add(task)
        print('%s tasks added' % self.tasks.qsize())
        self.wait_done()
        self.stop()
