""" import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def data_gen():
    '''t = data_gen.t
    cnt = 0
    while cnt < 4408:
        cnt += 1
        t += 0.05
        yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)'''
    t = 0
    cnt = 0
    while cnt < 4408:
        cnt += 1
        t += 0.1
        yield t, np.sin(2*np.pi*t*440/44100)


data_gen.t = 0

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(-1.1, 1.1)
ax.set_xlim(0, 5)
ax.grid()
xdata, ydata = [], []


def run(data):
    # update the data
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,


ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=1,
                              repeat=False)
plt.show()
 """

# BASIC

"""
   A simple example of an animated plot
   """

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
fig, ax = plt.subplots()

fs = 44100  						# Sample frequency of sound wave
freq = 220.0                            # Sound frequency in Hz
duration = 0.1	                    # Duration in s of audio output
samples = np.arange(duration*fs)

x = np.linspace(0, duration, 4409)        # x-array
line, = ax.plot(x, np.sin(2*np.pi*samples*freq/fs)[0:4408])


def main():
    def freq_gen():
        yield freq - 100

    def animate(i):
        global freq
        freq = freq + random.randint(-5, 1)
        line.set_ydata(np.sin(2*np.pi*samples*freq/fs)
                       [1:4409])  # update the data
        return line,

    # Init only required for blitting to give a clean slate.

    def init():
        line.set_ydata(np.ma.array(x, mask=True))
        return line,

    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200),
                                  interval=25, blit=True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
