import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation
from itertools import count
import pyaudio


fs = 44100							# Sample frequency of sound wave
freq = 0							# Sound frequency in Hz
duration = 0.01		# Duration in s of audio output
samples = np.arange(duration*fs) 	# Sampling numbers
n = 100                         	# number of samples to plot
timev = np.linspace(0, n/fs, n)		# X values array for plotwave = 0
wave = 0.1*np.sin(2*np.pi*samples*freq/fs)
fig = plt.figure() 
ax = fig.add_subplot(111)
plt.style.use('fivethirtyeight')
pya = pyaudio.PyAudio()
stream = pya.open(format=pyaudio.paCustomFormat, channels=1, rate=fs, output=True)

index = count()

x = []
y = []

plt.grid(True, which='both')
plt.axhline(y=0, color='k')
plt.legend(loc='upper left')

plt.tight_layout()

'''	
def animate(i, freq_p):
        it = next(index)

        global wave
        wave = 0.1*np.sin(2*np.pi*samples*freq_p/fs)
        
        x = timev
        y = wave[0:n]
        
        plt.cla()

        plt.title('Sine wave')
        plt.xlabel('Time')
        plt.ylabel('Amplitude = sin(time)')
        ax.set_facecolor("lightgrey")
        if it % 2 == 0:
            t = plt.text(0.0015, 0.05, 'PERFECT', fontsize=15)
        else:
            t = plt.text(0.0015, 0.05, 'Very Close', fontsize=15)
        t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red', boxstyle='square,pad=0.5'))
     
        plt.plot(x, y, label='Sensor 1')'''

def sound_generator(control_variable, freq_p):
    global freq
	
    if control_variable > 500:
        freq_p.value = 1740.0
        freq = freq_p.value
		
    elif control_variable > 150 and control_variable <= 500:
        freq_p.value = 880.0
        freq = freq_p.value
		
    else:
        freq_p.value = 440.0
        freq = freq_p.value

    
    #print(freq_p.value)
    
    #print(freq)
    
    global wave
    #wave = 0.1*np.sin(2*np.pi*samples*freq_p.value/fs)
    wave = 0.1*np.sin(2*np.pi*samples*control_variable/fs)+0.1*np.sin(2*np.pi*samples*(control_variable+1)/fs)+0.1*np.sin(2*np.pi*samples*(control_variable-1)/fs)
    #generate_sample(wave)
    
    bytestream = wave.tobytes()
    stream.write(bytestream)
    #time.sleep(duration)
   
    #ska försöka implementera callback mode, misstänker att jag kan döda bruset så. Återstårosé
   
    
    
    
    
    #sd.play(wave,fs)				# Audio production from sinusoid
	
    #time.sleep(duration)			# Wait out the audio output

def wave_plotter(freq_p):
    print("wave plotter")

    print(freq_p)
    
    #ani = FuncAnimation(plt.gcf(), animate, repeat=False,fargs=(freq_p,), interval=500)
    
    wave = 0.1*np.sin(2*np.pi*samples*freq_p/fs)
    
    x = timev
    y = wave[0:n]
    
    plt.cla()

    plt.title('Sine wave')
    plt.xlabel('Time')
    plt.ylabel('Amplitude = sin(time)')
    ax.set_facecolor("lightgrey")
    
    if freq_p == 1740.0:
        t = plt.text(0.0015, 0.05, 'Far Away', fontsize=15)
        t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red', boxstyle='square,pad=0.5'))
        
    elif freq_p == 880.0:
        t = plt.text(0.0015, 0.05, 'Medium range', fontsize=15)
        t.set_bbox(dict(facecolor='green', alpha=0.5, edgecolor='red', boxstyle='square,pad=0.5'))
        
    elif freq_p == 440.0:
        t = plt.text(0.0015, 0.05, 'Nothing detected', fontsize=15)
        t.set_bbox(dict(facecolor='yellow', alpha=0.5, edgecolor='red', boxstyle='square,pad=0.5'))

 
    plt.plot(x, y, label='Sensor 1')

    #plt.show(block=False)
    plt.draw()
    plt.pause(0.01)
    #plt.close()

#### NÅGONTING JAG VILL LEKA MED SENARE!!!
def generate_sample(ob):
    print("* Generating sample...")
    tone_out = array(ob, dtype=int16)

    
    print("* Previewing audio file...")

    
    
    
    stream.write(bytestream)
    stream.stop_stream()
    stream.close()

    pya.terminate()
    print("* Preview completed!")
