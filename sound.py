import sounddevice as sd
import numpy as np
import time
import pyaudio


fs = 44100  						# Sample frequency of sound wave
freq = 0                            # Sound frequency in Hz
duration = 0.1                      # Duration in s of audio output
samples = np.arange(duration*fs) 	# Sampling numbers

mem=np.ones(10)

pya = pyaudio.PyAudio()

stream = pya.open(format=pyaudio.paInt16, channels=1, rate=fs, input=False, output=True)

attack = np.arange(fs*duration*0.1)/(fs*duration*0.1)
decay = np.linspace(1, 0.95, int((fs*duration*0.1)))
sustain = np.linspace(0.95, 0.6, int((fs*duration*0.6)))
release = np.linspace(0.6, 0, int((fs*duration*0.2)))
amp_vec = 3000 * np.concatenate([attack, decay, sustain, release])

f0 = 0
phaseshift = 0

down = True

wave = np.zeros(len(samples))
old = wave

def sound_generator(control_variable, dis):
    global freq
    global f0
    global wave
    global phaseshift
    global ampold
    global mem
    global old
    global retwave
   
    freq = control_variable
   
    mem= mem[1:mem.size]
    mem=np.append(mem,dis)
    
    amp=0
    for i in range(0,mem.size-2):
        amp=amp+mem[i+1]-mem[i]
    amp=0.1*amp
  
    #print(amp)
    global down
        
    if (amp > 3 and amp < 60) and down:
        down = False

    elif (amp < -2 and amp > -20) and not down:
        down = True
        
        #freq = f0 + samples*(control_variable - f0)/(duration*fs)
        freq = control_variable

        wave_samples_minus_last = (2*np.pi*samples*freq/fs)
        
        harm1 = amp_vec*np.sin((2*np.pi*samples*4*freq/fs) +phaseshift)
        harm2 = amp_vec*np.sin((2*np.pi*samples*8*freq/fs) +phaseshift)
        harm3 = amp_vec*np.sin((2*np.pi*samples*0.2*freq/fs) +phaseshift)
        harm4 = amp_vec*np.sin((2*np.pi*samples*0.6*freq/fs) +phaseshift)
        
        main = (
            2*amp_vec*np.sin(wave_samples_minus_last+phaseshift)) + harm1 + harm2
        
        
        wave = main + 0.1*old
        old= wave
        
        phaseshift = 2*np.pi*(control_variable/fs)*(duration*fs) + phaseshift
        f0 = control_variable
        
        #return main[:]
        
        #wave = amp_vec*np.sin(2*np.pi*samples*freq/fs)   
    
        #return wave
    else:
        if(max(wave) > 500):
            wave=old
            old=0.9*wave    
            
        else:
            wave=np.ones(samples.size)
            
    #test = 3000*np.sin(2*np.pi*samples*440/fs)
    return wave
    
        
def play_sound(output):
        
        if output is None:
            print("none")
        else:
            #print(output[:])
          
            '''y=np.arange(len(output))
            for i in range (0,len(output)):
                
                y[i]=output[i]
        y = output'''
        bytestream = np.frombuffer(output.get_obj()).astype("int16").tobytes()
        stream.write(bytestream)

'''
def wave_plotter(freq_p):
    print("wave plotter")

    # print(freq_p)

    #ani = FuncAnimation(plt.gcf(), animate, repeat=False,fargs=(freq_p,), interval=500)

    wave = 0.1*np.sin(2*np.pi*samples*freq_p/fs)

    x = timev
    y = wave

    plt.cla()

    plt.title('Sine wave')
    plt.xlabel('Time')
    plt.ylabel('Amplitude = sin(time)')
    ax.set_facecolor("lightgrey")

    ##############################
    if freq_p == 1740.0:
        t = plt.text(0.0015, 0.05, 'Far Away', fontsize=15)
        t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red', boxstyle='square,pad=0.5'))
        
    elif freq_p == 880.0:
        t = plt.text(0.0015, 0.05, 'Medium range', fontsize=15)
        t.set_bbox(dict(facecolor='green', alpha=0.5, edgecolor='red', boxstyle='square,pad=0.5'))
        
    elif freq_p == 440.0:
        t = plt.text(0.0015, 0.05, 'Nothing detected', fontsize=15)
        t.set_bbox(dict(facecolor='yellow', alpha=0.5, edgecolor='red', boxstyle='square,pad=0.5'))
    ##############################

    plt.plot(x, y, label='Sensor 1')

    # plt.show(block=False)
    plt.draw()
    plt.pause(0.01)
    # plt.close()
'''
