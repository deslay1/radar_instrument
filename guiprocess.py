import multiprocessing as mp
import queue
import signal
from time import sleep, time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class PGProcess:
    def __init__(self, updater, max_freq=60):
        self._queue = mp.Queue()
        self._exit_event = mp.Event()

        args = (
            self._queue,
            self._exit_event,
            updater,
            max_freq
        )

        self._process = mp.Process(target=pg_process_program, args=args, daemon=True)

    def start(self):
        self._process.start()

    def put_data(self, data):
        print(self._process.exitcode)
        if self._exit_event.is_set() or self._process.exitcode is not None:
            self.close()
            raise PGProccessDiedException

        try:
            self._queue.put(data) # update if all good?
        except BrokenPipeError:
            self.close()
            raise PGProccessDiedException

    def close(self):
        if self._process.exitcode is None:
            self._exit_event.set()
            self._process.join(1)

        if self._process.exitcode is None:
            self._process.terminate()
            self._process.join(1)

        if self._process.exitcode is None:
            raise RuntimeError


def pg_process_program(q, exit_event, updater, max_freq):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    
    updater.setup() # setup, start animation and stuff...

    while not exit_event.is_set():
        data = None
        try:
            data = q.get(timeout=0.1)
            while True:
                #print("stuck here")
                data = q.get(timeout=0.001) # seems like we dont get locked here, but I don't see how not (while true). 
        except queue.Empty:
            pass

        data_time = time()

        if data is not None:
            #print("stuck here2")
            print(data)
            updater.update(data) # here is where we actually update?

        if max_freq and data is not None:
            sleep_time = 1 / max_freq - (time() - data_time)
            if sleep_time > 0.005:
                sleep(sleep_time)

    try:
        while True:
            q.get(timeout=0.001)
    except Exception:
        pass


class ExamplePGUpdater:
    # set class attricutes x and y data
    xc = np.linspace(0,10,100)
    yc = np.sin(xc)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.ion()
    fig.show()
    fig.canvas.draw()
    
    def __init__(self):
        pass
    
    def animate(self,i):
        plt.cla()
        plt.plot(self.xc, self.yc)

    def setup(self):
        # here setup the figures and animation, read from attributes
        # x and y
        #plt.style.use('fivethirtyeight')
        #ani = FuncAnimation(plt.gcf(), self.animate, interval=100)
        #plt.tight_layout()
        #plt.show()
        print(self.yc)

    def update(self, data):
        x, y = data
        # dont use below, here we want to set class attributes
        #self.curve.setData(x, y)
        #global xc
        #global yc
        self.xc = x
        self.yc = y
        #print(self.yc)
        self.ax1.clear()
        self.ax1.scatter(self.xc,self.yc)
        self.fig.canvas.draw()


class PGProccessDiedException(Exception):
    pass

def main(interrupt_handler, shared_wave):
    import numpy as np

    pg_updater = ExamplePGUpdater() # The updater to pass to process
    pg_process = PGProcess(pg_updater)
    pg_process.start() # start process

    # keep below for now
    x = np.linspace(0, 10, 100)
    t0 = time()
    t = 0
    while not interrupt_handler.got_signal:
        #print(shared_wave)
        t = time() - t0
        y = np.sin(x + t)

        try:
            pg_process.put_data([x, y])
        except PGProccessDiedException:
            exit()

        sleep(0.01) # why?...

    pg_process.close() # close process...
        

# ideally this part will be put in radar.py when this thing works.
#if __name__ == "__main__":
    #main(interrupt_handler, shared_wave)
    
