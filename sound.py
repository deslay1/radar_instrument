import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation
from itertools import count
import pyaudio


fs = 44100  						# Sample frequency of sound wave
freq = 0                            # Sound frequency in Hz
duration = 0.1	                    # Duration in s of audio output
samples = np.arange(duration*fs) 	# Sampling numbers
n = 4410                         	# number of samples to plot
timev = np.linspace(0, n/fs, n)		# X values array for plotwave = 0
wave = 0.1*np.sin(2*np.pi*samples*freq/fs)

pya = pyaudio.PyAudio()

stream = pya.open(format=pyaudio.paInt16,channels=1, rate=fs, input=False, output=True)
f0=0
phaseshift=0
ampold=0
fig = plt.figure() 
ax = fig.add_subplot(111)
plt.style.use('fivethirtyeight')

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
        
down = True
up = False

def sound_generator(control_variable, amp):
    global freq
    global freq_wave
    global f0
    global wave
    global phaseshift
    global ampold
    
    freq_wave = control_variable
    
    skillnad = amp - ampold
    
    '''if amp < 30:
        amp = 0.5*ampold
    elif amp > 400:
        amp = 0.5*ampold
    else:
        amp = 10*amp + 0.8*ampold'''
    
    global down
    global up
    #print(amp)
    
    if (amp > 20 and amp < 500) and down:
        down = False
    elif (amp < -20 and amp > -500) and not down:
        down = True
        amp = 1000 + 0.8*ampold
        freq =f0 + samples*(control_variable- f0)/(duration*fs)
        freq = control_variable
        
        harm1 = amp*np.sin((2*np.pi*samples*2*freq/fs)+phaseshift)
        harm2 = amp*np.sin((2*np.pi*samples*4*freq/fs)+phaseshift)
        harm3 = amp*np.sin((2*np.pi*samples*8*freq/fs)+phaseshift)
        harm4 = amp*np.sin((2*np.pi*samples*16*freq/fs)+phaseshift)
        
        wave_samples_minus_last = (2*np.pi*samples*freq/fs)
        wave = ((2*amp*np.sin(wave_samples_minus_last[0:wave_samples_minus_last.size-2]+phaseshift))+harm1[0:wave_samples_minus_last.size-2]+harm2[0:wave_samples_minus_last.size-2]+harm3[0:wave_samples_minus_last.size-2]+harm4[0:wave_samples_minus_last.size-2]).astype("int16")
        
        phaseshift = 2*np.pi*(control_variable/fs)*(duration*fs) + phaseshift
        f0=control_variable
        
        bytestream = wave.tobytes()
        stream.write(bytestream)
        ampold=amp
    else:
        amp = 0
         
        
    #print(amp)
    
    #amp = 2500
    

def wave_plotter(freq_p):
    print("wave plotter")

    #print(freq_p)
    
    #ani = FuncAnimation(plt.gcf(), animate, repeat=False,fargs=(freq_p,), interval=500)
    
    wave = 0.1*np.sin(2*np.pi*samples*freq_p/fs)
    
    x = timev
    y = wave
    
    
    plt.cla()

    plt.title('Sine wave')
    plt.xlabel('Time')
    plt.ylabel('Amplitude = sin(time)')
    ax.set_facecolor("lightgrey")
    
    '''
    if freq_p == 1740.0:
        t = plt.text(0.0015, 0.05, 'Far Away', fontsize=15)
        t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red', boxstyle='square,pad=0.5'))
        
    elif freq_p == 880.0:
        t = plt.text(0.0015, 0.05, 'Medium range', fontsize=15)
        t.set_bbox(dict(facecolor='green', alpha=0.5, edgecolor='red', boxstyle='square,pad=0.5'))
        
    elif freq_p == 440.0:
        t = plt.text(0.0015, 0.05, 'Nothing detected', fontsize=15)
        t.set_bbox(dict(facecolor='yellow', alpha=0.5, edgecolor='red', boxstyle='square,pad=0.5'))
    '''

    plt.plot(x, y, label='Sensor 1')

    #plt.show(block=False)
    plt.draw()
    plt.pause(0.01)
    #plt.close()


