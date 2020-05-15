import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation
from itertools import count


fs = 44100							# Sample frequency of sound wave
freq = 0							# Sound frequency in Hz
duration = 1						# Duration in s of audio output
samples = np.arange(duration*fs) 	# Sampling numbers
n = 100                         	# number of samples to plot
timev = np.linspace(0, n/fs, n)		# X values array for plotwave = 0
wave = 0.1*np.sin(2*np.pi*samples*freq/fs)
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


'''def sound_initiate():
	plt.show()
	#fig.canvas.draw()
	
	#plt.style.use('fivethirtyeight')

	plt.title('Sine wave')
	plt.xlabel('Time')
	plt.ylabel('Amplitude = sin(time)')
	#plt.axes().set_facecolor("lightgrey")
	ax.set_facecolor('#eafff5')
	t = plt.text(0.0015, 0.05, 'Very Close', fontsize=15)
	t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red', boxstyle='square,pad=0.5'))

	plt.grid(True, which='both') 
	plt.axhline(y=0, color='k')
	 
	#plt.plot(timev, wave[0:n])  	# Plotting n samples
	#plt.show(block=False)          # Display the sound wave '''
	
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
 
    plt.plot(x, y, label='Sensor 1')

def sound_generator(control_variable, freq_p):
	global freq
	
	if control_variable > 140:
		freq_p.value = 1740.0
		freq = freq_p.value
		
	elif control_variable > 100 and control_variable < 140:
		freq_p.value = 880.0
		freq = freq_p.value
		
	else:
		freq_p.value = 440.0
		freq = freq_p.value
		
	print(freq_p.value)
	print(freq)
	
	global wave
	wave = 0.1*np.sin(2*np.pi*samples*freq/fs)
	
	sd.play(wave,fs)				# Audio production from sinusoid
	
	time.sleep(duration)			# Wait out the audio output

def wave_plotter(freq_p):
	print("wave plotter")

	print(freq_p)
	
	while True is True:
		ani = FuncAnimation(plt.gcf(), animate, repeat=False, fargs=(freq_p,), interval=1000)
		plt.show()

