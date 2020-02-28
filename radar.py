from acconeer.exptool import configs, utils
from acconeer.exptool.clients import SocketClient, SPIClient, UARTClient
#from playsound import playsound
import time
import os
import statistics
import concurrent.futures
import threading
import numpy as np
import sounddevice as sd
#from scipy.io.wavfile import write
file = "/home/pi/Downloads/acconeer-python-exploration-master/audio/sound7.mp3"
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
    config.update_rate = 10

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
        info, data = client.get_next()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            f1 = executor.submit(data_handler, info, data)
            f2 = executor.submit(tune_player)
            #print(f1.result(), f2.result())'''
    '''t1 = threading.Thread(target=runner, args=[client])
    t2 = threading.Thread(target=tune_player)
    t1.start()
    t2.start()'''
        
    while not interrupt_handler.got_signal:
        '''with concurrent.futures.ProcessPoolExecutor() as executor:
            print("HI 1")
            f1 = executor.submit(runner, client)
            f2 = executor.submit(tune_player)'''
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            t1 = executor.submit(runner, client)
            t2 = executor.submit(tune_player)
        
        #t1.join()
        #t2.join()
    
    #t1.join()
    #t2.join()

    print("Disconnecting...")
    client.disconnect()

mean_data = 0
more = True

def runner(client):
    print("HI 2")
    info, data = client.get_next()
    global mean_data 
    mean_data = statistics.mean(data)
    print(info, "\n", data, "\n", mean_data)
    # tänk över vad mean är...
    

def data_handler(info,data):
    more = True
    mean_data = statistics.mean(data)
    print(info, "\n", data, "\n", mean_data, "\n", more)
        
def tune_player():
    print("HI tune")
    sps = 44100.0
    if mean_data > 100:
        freq_hz = 640.0
    else:
        freq_hz = 440.0
    duration_s = 1.0
    
    each_sample_number = np.arange(duration_s*sps)
    waveform = 0.1 * np.sin(2*np.pi*each_sample_number*freq_hz/sps)
    print("HI tune")
    sd.play(waveform,sps)
    time.sleep(duration_s)
    print("DONEEEEE \n", mean_data)


if __name__ == "__main__":
    main()
#Interpolerar hastighet från två avståndsvärden, föregående(x1)(t2) och senaste(x1)(t1) 
def fastV(x1,x2,t1,t2):
	return (x2-x1)/(t2-t1)
#returnerar det faktiska avståndet till detekterat föremål (förutsätter numpy)
def getX(minRange, rangeInterval,data):
	return np.argmax(data)*rangeInterval + minRange


