
import pyaudio

pya = pyaudio.PyAudio()

for i in range(pya.get_device_count()):
    print(pya.get_device_info_by_index(i))
