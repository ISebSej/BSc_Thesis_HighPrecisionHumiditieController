import threading
import Queue
import time


class SerialThread(threading.Thread):

    def __init__(self, name='SerialThread'):
        """ constructor, setting initial variables """
        self._stopevent = threading.Event()
        self._sleepperiod = 0.5

        threading.Thread.__init__(self, name=name)

    def run(self):
        """ main control loop """
        print "%s starts" % (self.getName(),)

        while not self._stopevent.isSet():
            with lock:
                print("{} in serial".format(count))
                global count
                count += 1
                time.sleep(2)

            serialq.task_done()
            pass


        print "%s ends" % (self.getName(),)

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)



if __name__ == "__main__":
    lock = threading.Lock()
    serialq = Queue.Queue()

    global count
    count = 0

    testthread = SerialThread()
    testthread.start()
    for item in range(1,30):
        serialq.put(item)
        print("put {} in queue".format(item))
    import time

    time.sleep(20.0)

    testthread.join()
