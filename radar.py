from acconeer.exptool import configs, utils
from acconeer.exptool.clients import SocketClient, SPIClient, UARTClient
#from playsound import playsound
import time
import os
import statistics
import concurrent.futures
import threading
import numpy as np
from sound import sound_generate
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
    config.range_interval = [0.3, 0.7]
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
    # Here we make use of multithreading to run the data collection and
    # sound generation separately. the intrerrupt_handler is passed in
    # so that the threads are both stopped when a user hits Ctrl-C.   
    with concurrent.futures.ThreadPoolExecutor() as executor:
        t1 = executor.submit(data_handler, client, interrupt_handler)
        t2 = executor.submit(tune_player, interrupt_handler)
            
        print(t1.result(), t2.result())
    
    # Threads close after script terminates.
    t1.join()
    t2.join()

    print("Disconnecting...")
    client.disconnect()

mean_data = 0

# data handler 
def data_handler(client, interrupt_handler2):
    while not interrupt_handler2.got_signal:
        info, data = client.get_next()
        global mean_data 
        #mean_data = getX(0.3,0.0004843111091759056,data)
        mean_data = statistics.mean(data)
        
        #print(info, "\n", data, "\n", mean_data)
        print(mean_data)

        
def tune_player(interrupt_handler2):
    while not interrupt_handler2.got_signal:
        sound_generate(mean_data)
        print(mean_data)


if __name__ == "__main__":
    main()
