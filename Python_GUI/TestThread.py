import threading

class SerialThread(threading.Thread):

    def __init__(self, name='SerialThread'):
        """ constructor, setting initial variables """
        self._stopevent = threading.Event()
        self._sleepperiod = 0.1

        threading.Thread.__init__(self, name=name)

    def run(self):
        """ main control loop """
        print "%s starts" % (self.getName(),)

        count = 0
        while not self._stopevent.isSet():
            count += 1
            print "loop %d" % (count,)

            item = serialq.get()
            #do_work(item)
            print(item)
            serialq.task_done()

            self._stopevent.wait(self._sleepperiod)

        print "%s ends" % (self.getName(),)

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)



if __name__ == "__main__":
    testthread = SerialThread()
    testthread.start()

    import time
    time.sleep(20.0)

    testthread.join()
