from acconeer.exptool import configs, utils
from acconeer.exptool.clients import SocketClient, SPIClient, UARTClient
#from playsound import playsound
import time
import os
import statistics
import concurrent.futures
import multiprocessing
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from sound import *
from time import sleep, time
import gui
import guiprocess
#from scipy.io.wavfile import write
#file = "/home/pi/Downloads/acconeer-python-exploration-master/audio/sound7.mp3"
# os.system("omxplayer " + file)

def main():
    args = utils.ExampleArgumentParser().parse_args()
    utils.config_logging(args)

    if args.socket_addr:
        client = SocketClient(args.socket_addr)
    elif args.spi:
        client = SPIClient()
    else:
        port = args.serial_port or utils.autodetect_serial_port()
        client = UARTClient(port)

    # Normally when using a single sensor, get_next will return
    # (info, data). When using mulitple sensors, get_next will return
    # lists of info and data for each sensor, i.e. ([info], [data]).
    # This is commonly called squeezing. To disable squeezing, making
    # get_next _always_ return lists, set:
    # client.squeeze = False

    config = configs.EnvelopeServiceConfig()
    config.sensor = args.sensors
    config.range_interval = [0.2, 0.7]
    config.update_rate = 50

    session_info = client.setup_session(config)
    print("Session info:\n", session_info, "\n")

    # Now would be the time to set up plotting, signal processing, etc.

    client.start_session()

    # Normally, hitting Ctrl-C will raise a KeyboardInterrupt which in
    # most cases immediately terminates the script. This often becomes
    # an issue when plotting and also doesn't allow us to disconnect
    # gracefully. Setting up an ExampleInterruptHandler will capture the
    # keyboard interrupt signal so that a KeyboardInterrupt isn't raised
    # and we can take care of the signal ourselves. In case you get
    # impatient, hitting Ctrl-C a couple of more times will raise a
    # KeyboardInterrupt which hopefully terminates the script.
    interrupt_handler = utils.ExampleInterruptHandler()
    print("Press Ctrl-C to end session\n")

    '''while not interrupt_handler.got_signal:
    with concurrent.futures.ProcessPoolExecutor() as executor:
            print("HI 1")
            f1 = executor.submit(runner, client)
            f2 = executor.submit(tune_player)'''

    '''  
    with concurrent.futures.ThreadPoolExecutor() as executor:
        t1 = executor.submit(data_handler, client, interrupt_handler)
        t2 = executor.submit(tune_player, interrupt_handler)
            
        print(t1.result(), t2.result())
    
    # Threads close after script terminates.
    t1.join()
    t2.join()'''
    # Here we make use of multiprocessing to run the data collection and
    # sound generation separately. the intrerrupt_handler is passed in
    # so that the threads are both stopped when a user hits Ctrl-C.
    with multiprocessing.Manager() as manager:
        shared_value = manager.Value('d', 0)   # Shared value between processes
        shared_amp = manager.Value('d', 0)
        #shared_wave = manager.Array('d', np.arange(4408))
        shared_wave = manager.list(range(100))
        p1 = multiprocessing.Process(target=data_handler, args=(
            client, interrupt_handler, shared_value, shared_amp))
        p2 = multiprocessing.Process(target=tune_player, args=(
            interrupt_handler, shared_value, shared_amp, shared_wave))
        #p3 = multiprocessing.Process(target=plotter, args=(interrupt_handler, shared_wave))
        p1.start()
        p2.start()
        #p3.start()
        
        '''
        pg_updater = guiprocess.ExamplePGUpdater() # The updater to pass to process
        pg_process = guiprocess.PGProcess(pg_updater)
        pg_process.start() # start process

        # keep below for now
        #x = np.linspace(0, 10, 100)
        x = np.arange(4408)
        t0 = time()
        t = 0
        while not interrupt_handler.got_signal:
            #print(shared_wave[:])
            t = time() - t0
            y = shared_wave[:]

            try:
                pg_process.put_data([x, y])
            except guiprocess.PGProccessDiedException:
                exit()

            sleep(0.01) # why?...

        pg_process.close() # close process...'''

        # Wait for processes to terminate before moving on
        p1.join()
        p2.join()
        #p3.join()

    print("Disconnecting...")
    client.disconnect()


# Function for data processing. The shared value is currently set to the
# mean of the data feedback from the radar sensor.
peak_prev = 0


def data_handler(client, interrupt_handler, shared_value, shared_amp):

    while not interrupt_handler.got_signal:

        info, data = client.get_next()

        shared_value.value = freqMapper(len(data[0]), np.argmax(data[0]))

        global peak_prev

        if np.max(data[1])>150:
            shared_amp.value = np.argmax(data[1])


# Function for playing different tunes according to how far away our
# obstacle is from the sensor. Sound_generate() is called from sound.py
def tune_player(interrupt_handler, shared_value, shared_amp, shared_wave):
    
    pg_updater = guiprocess.ExamplePGUpdater() # The updater to pass to process
    pg_process = guiprocess.PGProcess(pg_updater)
    pg_process.start() # start process

    # keep below for now
    #x = np.linspace(0, 10, 100)
    x = np.arange(100)
    t0 = time()
    t = 0
        
    while not interrupt_handler.got_signal:
        control_variable = float(shared_value.value)

        shared_wave = sound_generator(control_variable, float(shared_amp.value), shared_wave)[:]
        #print(shared_wave)
        
        #print(shared_wave[:])
        t = time() - t0
        y = shared_wave[:]

        try:
            pg_process.put_data([x, y])
        except guiprocess.PGProccessDiedException:
            exit()

        sleep(0.01) # why?...

    pg_process.close() # close process...

# Function not complete, but the idea is to plot the sound wave real-time

def updateWave():
    print(y_wave)
    return y_wave[:]

def plotter(interrupt_handler, shared_wave):
    #while not interrupt_handler.got_signal:
        #freq = float(shared_value.value)
        #wave_plotter(freq)
    #t1 = threading.Thread(target=gui.main(shared_wave[:]))
    #t2 = threading.Thread(target=gui.updateWave(interrupt_handler, shared_wave[:]))
    
    pg_updater = guiprocess.ExamplePGUpdater() # The updater to pass to process
    pg_process = guiprocess.PGProcess(pg_updater)
    pg_process.start() # start process

    # keep below for now
    #x = np.linspace(0, 10, 100)
    x = np.arange(4408)
    t0 = time()
    t = 0
    while not interrupt_handler.got_signal:
        print(shared_wave)
        t = time() - t0
        y = shared_wave[:]

        try:
            pg_process.put_data([x, y])
        except guiprocess.PGProccessDiedException:
            exit()

        sleep(0.01) # why?...

    pg_process.close() # close process...
    

# A frequency mapper function that returns a frequency for sound generation
def freqMapper(arrayLength, currentIndex):
    mini = 440
    freN = 10
    maxi = 1661.28
    #fre = (currentIndex*(maxi-mini)/arrayLength + mini)
    fre = currentIndex/arrayLength*freN
   
    '''if fre > 14:
        fre = 1661.28

    elif fre > 13:
        fre = 1567.98

    elif fre > 12:
        fre = 1396.91

    elif fre > 11:
        fre = 1318.51

    elif fre > 10:
        fre = 1174.66'''

    if fre > 9:
        fre = 1046.50

    elif fre > 8:
        fre = 987.77

    elif fre > 7:
        fre = 880.00

    elif fre > 6:
        fre = 783.99

    elif fre > 5:
        fre = 698.46

    elif fre > 4:
        fre = 659.25

    elif fre > 3:
        fre = 587.33

    elif fre > 2:
        fre = 523.25

    elif fre > 1:
        fre = 493.98

    else:
        fre = 440.0
    
    
    ''' if fre > 1567.98:
        fre = 1661.28

    elif fre > 1396.91:
        fre = 1567.98

    elif fre > 1318.51:
        fre = 1396.91

    elif fre > 1174.66:
        fre = 1318.51

    elif fre > 1046.50:
        fre = 1174.66

    elif fre > 987.77:
        fre = 1046.50

    elif fre > 880.00:
        fre = 987.77

    elif fre > 783.99:
        fre = 880.00

    elif fre > 698.46:
        fre = 783.99

    elif fre > 659.25:
        fre = 698.46

    elif fre > 587.33:
        fre = 659.25

    elif fre > 523.25:
        fre = 587.33

    elif fre > 493.98:
        fre = 523.25

    elif fre > 440.0:
        fre = 493.98

    else:
        fre = 440.0 '''

    return fre
    
    
    
    


if __name__ == "__main__":
    main()
