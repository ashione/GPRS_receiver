import threading
import Queue

class GPRS_thread(threading.Thread):
    def __init__(self,threadID,func,queue):
        assert isinstance(queue,Queue.Queue)
        threading.Thread.__init__(self)
        self.threadID=threadID
        self._queue = queue
        self.func = func
    def run(self):
        self.func(self._queue)
    def stop(self):
        #threading.Thread.__stop()
        self._Thread__stop()
