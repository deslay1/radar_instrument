# BASIC

"""
   A simple example of an animated plot
   """

import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


plt.style.use("fivethirtyeight")

fig, axs = plt.subplots(2)
        
x = []
y = []

#x = np.linspace(0, duration, 4409)        # x-array

data = np.loadtxt("data.csv", delimiter=",")
data2 = np.loadtxt("data2.csv", delimiter=",")
#x = np.arange(data[0].size)
#line, = ax.plot(x, data[0])

def main():

    def animate(i):
        #data = pd.read_csv("data.csv")
        x = np.arange(data[i].size)
        y = data[i]
        
        x2 = np.arange(10)
        y2 = data2[i]*np.ones(10)
        
        plt.cla()
        axs[0].clear()
        axs[0].plot(x, y, label="SENSOR DATA")
        axs[0].set_ylabel("Amplitude")
        axs[0].set_xlabel("Distance from sensor")
        
        axs[1].plot(x2, y2, label="FREQUENCY", color="r")
        axs[1].set_ylabel("Frequency / Hz")
        axs[1].set_ylim(200, 1200)
        axs[1].set_xticklabels([])
        axs[1].legend([f"{y2[0]} Hz"])
        
        "plt.savefig(f"sweep{i}.png", bbox_inches='tight')
        
        plt.tight_layout()
        

    ani = animation.FuncAnimation(fig, animate, frames= np.size(data, 1)-1, repeat=False,
                                  interval=1)
    plt.show()
    
if __name__ == "__main__":
    main()
