import sounddevice as sd
import numpy as np

def sound_generate(dist):
	sps = 44100.0					# Sample frequency of sound wave
	
	if dist > 140:					# Sound frequency
		freq_hz = 1740.0
	elif dist > 100 and dist < 140:
		freq_hz = 880.0
	else:
		freq_hz = 440.0
		
	duration_s = 1					# Duration of audio output
	
	each_sample_number = np.arange(duration_s*sps) # Sampling numbers
	
	waveform = 0.1*np.sin(2*np.pi*each_sample_number*freq_hz/sps)
	sd.play(waveform,sps)			# Audio production from sinusoid
	
	time.sleep(duration_s)			# Wait out the audio output
