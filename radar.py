from acconeer.exptool import configs, utils
from acconeer.exptool.clients import SocketClient, SPIClient, UARTClient

import os
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
from sound import *

def main():
    
    duration=0.1
    fs=44100
    n=int(fs*duration)
    
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
    config.range_interval = [0.2, 1] # Range configuration
    config.update_rate = 50 # Data collection frequency

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


    # Here we make use of multiprocessing to run the data collection, sound wave computation, and 
    # audio output separately. the intrerrupt_handler is passed in
    # so that the processes are stopped when a user hits Ctrl-C.
    
    with multiprocessing.Manager() as manager:
        
        shared_value = manager.Value('d', 0)   # Shared value between processes
        shared_amp = manager.Value('d', 0)
        shared_wave = multiprocessing.Array('d',n)
        
        p1 = multiprocessing.Process(target=data_handler, args=(
            client, interrupt_handler, shared_value, shared_amp))
        p2 = multiprocessing.Process(target=tune_gen, args=(
            interrupt_handler, shared_value, shared_amp, shared_wave))
        p3 = multiprocessing.Process(target=tune_play, args=(interrupt_handler, shared_wave))
        
        # Start processes
        p1.start()
        p2.start()
        p3.start()

        # Wait for processes to terminate before moving on
        p1.join()
        p2.join()
        p3.join()

    print("Disconnecting...")
    client.disconnect()


# Function for data processing.
# shared_value is updated according to a frequency mapping function.
# shared_amp is updated according to the distance away from the sensor
# used to decide when a note should be played
peak_prev = 0

def data_handler(client, interrupt_handler, shared_value, shared_amp):
    
    while not interrupt_handler.got_signal:

        info, data = client.get_next()
        
        shared_value.value = freqMapper(len(data[0]), np.argmax(data[0]))
        
        global peak_prev

        if np.max(data[1])>150:
            shared_amp.value = np.argmax(data[1])


# Generates a sound wave out of a determined frequency 
# sound_generator() is called from sound.py
def tune_gen(interrupt_handler, shared_value, shared_amp, shared_wave):
        
    while not interrupt_handler.got_signal:
        control_variable = float(shared_value.value)
        y= sound_generator(control_variable, float(shared_amp.value))
        shared_wave[:] = y[:]
        
# Plays a sound wave through a connected audio outport using the
# pyaudio library
def tune_play(interrupt_handler, shared_wave):
        while not interrupt_handler.got_signal:
           
           play_sound(shared_wave)

# A mapper function that returns a frequency value depending on
# currentIndex, which is the distance from the sensor responsible for
# determining the frequency
def freqMapper(arrayLength, currentIndex):
    mini = 440
    freN = 14
    maxi = 1661.28
    #fre = (currentIndex*(maxi-mini)/arrayLength + mini)
    fre = currentIndex/arrayLength*freN

    if fre > 13:
        fre = 1567.98 # G6

    elif fre > 12:
        fre = 1396.91 # F6

    elif fre > 11:
        fre = 1318.51 # E6

    elif fre > 10:
        fre = 1174.66 # D6

    elif fre > 9:
        fre = 1046.50 # C6

    elif fre > 8:
        fre = 987.77  # B5

    elif fre > 7:
        fre = 880.00  # A5

    elif fre > 6:
        fre = 783.99  # G5

    elif fre > 5:
        fre = 698.46  # F5

    elif fre > 4:
        fre = 659.25  # E5

    elif fre > 3:
        fre = 587.33  # D5

    elif fre > 2:
        fre = 523.25  # C5

    elif fre > 1:
        fre = 493.98  # B4

    else:
        fre = 440.0   # A4
    
    
    # another set of optional note configurations
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
