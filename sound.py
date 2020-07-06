import numpy as np
import pyaudio

# Sound wave configs
fs = 44100  						# Sample frequency of sound wave
freq = 0                            # Sound frequency in Hz
duration = 0.1                      # Duration in s of audio output
samples = np.arange(duration*fs) 	# Sampling numbers

averaging_array = np.ones(10)

# PyAudio configs
pya = pyaudio.PyAudio()
stream = pya.open(format=pyaudio.paInt16, channels=1, rate=fs, input=False, output=True)

# ADSR mechanism
attack = np.arange(fs*duration*0.1)/(fs*duration*0.1)
decay = np.linspace(1, 0.95, int((fs*duration*0.1)))
sustain = np.linspace(0.95, 0.6, int((fs*duration*0.6)))
release = np.linspace(0.6, 0, int((fs*duration*0.2)))
amp_vec = 3000 * np.concatenate([attack, decay, sustain, release])

# Variables for chirping
f0 = 0
phaseshift = 0

down = True # Current state

# Initializations
wave = np.zeros(len(samples))
old = wave

 # Returns a sine wave optimized to play a good sound
def sound_generator(control_variable, dis):
    global freq
    global f0
    global wave
    global phaseshift
    global averaging_array
    global old
    global retwave
   
    freq = control_variable
   
    averaging_array = averaging_array[1:averaging_array.size]
    averaging_array = np.append(averaging_array,dis)
    
    amp = 0
    for i in range(0, averaging_array.size - 2):
        amp = amp + averaging_array[i + 1] - averaging_array[i]
    amp=0.1*amp
  
    global down
    
    # State: Up    
    if (amp > 3 and amp < 60) and down:
        down = False

    # State: Down (generate sound wave)
    elif (amp < -2 and amp > -20) and not down:
        down = True
        
        #freq = f0 + samples*(control_variable - f0)/(duration*fs) # Chirping

        wave_samples_minus_last = (2*np.pi*samples*freq/fs)
        
        # additional sine waves to produce better sound
        harm1 = amp_vec*np.sin((2*np.pi*samples*4*freq/fs) +phaseshift)
        harm2 = amp_vec*np.sin((2*np.pi*samples*8*freq/fs) +phaseshift)
        
        main = (2*amp_vec*np.sin(wave_samples_minus_last+phaseshift)) + harm1 + harm2
        
        wave = main + 0.1*old
        old= wave
        
        # Update chirping variables
        phaseshift = 2*np.pi*(control_variable/fs)*(duration*fs) + phaseshift
        f0 = control_variable
 

    else:
        if(max(wave) > 500):
            wave=old
            old=0.9*wave       
        else:
            wave=np.ones(samples.size)
    
    # Test wave array for debugging (constant sound output)
    # test = 3000*np.sin(2*np.pi*samples*440/fs)
    #return test
    
    return wave
    

# Plays sound from array output
def play_sound(output):
        if output is None:
            print("No data received")
        else:
            bytestream = np.frombuffer(output.get_obj()).astype("int16").tobytes()
            stream.write(bytestream)
