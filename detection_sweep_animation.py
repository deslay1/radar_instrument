import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

plt.style.use("fivethirtyeight")

#fig, axs = plt.subplots(2)

data = np.loadtxt("data.csv", delimiter=",")
data_frequency = np.loadtxt("data2.csv", delimiter=",") 

def main():

    def animate(i):
        global prev
        # Detection data subplot
        x = np.arange(data[i].size)
        y = data[i]
        
        '''
        # Frequency subplot
        x2 = np.arange(10)
        y2 = data_frequency[i]*np.ones(10)
        
        axs[0].clear() # Clear previous detection data
        axs[0].plot(x, y, label="SENSOR DATA")
        axs[0].set_ylim(0, 2000)
        axs[0].set_ylabel("Amplitude")
        axs[0].set_xlabel("Distance from sensor")
        
        axs[1].plot(x2, y2, label="FREQUENCY", color="r")
        axs[1].set_ylabel("Frequency / Hz")
        axs[1].set_ylim(200, 1200)
        axs[1].set_xticklabels([])
        axs[1].legend([f"{y2[0]} Hz"])
        '''
        arg = np.argmax(data[i])
        l = np.size(data, 1)
        
        prev = 0
        value = 0
        if arg / l < 1/14:
                value = 1/14
        elif arg / l < 2/14:
                prev = 1/14
                value = 2/14
        elif arg / l < 3/14:
                prev = 2/14
                value = 3/14
        elif arg / l < 4/14:
                prev = 3/14
                value = 4/14
        elif arg / l < 5/14:
                prev = 4/14
                value = 5/14
        elif arg / l < 6/14:
                prev = 5/14
                value = 6/14
        elif arg / l < 7/14:
                prev = 6/14
                value = 7/14
        elif arg / l < 8/14:
                prev = 7/14
                value = 8/14
        elif arg / l < 9/14:
                prev = 8/14
                value = 9/14
        elif arg / l < 10/14:
                prev = 9/14
                value = 10/14
        elif arg / l < 11/14:
                prev = 10/14
                value = 11/14
        elif arg / l < 12/14:
                prev = 11/14
                value = 12/14
        elif arg / l < 13/14:
                prev = 12/14
                value = 13/14
        elif arg / l < 14/14:
                prev = 13/14
                value = 14/14
        
        
        x2 = l*prev*np.ones(2000)
        x3 = l*value*np.ones(2000)
        y2 = np.arange(0, 2000)
        
        plt.cla()
        
        plt.plot(x, y, 'r', x2, y2, 'g--', x3, y2, 'g--')
        plt.ylabel("Amplitude")
        plt.xlabel("Distance from sensor")
        #plt.legend(["Detection data", f"{}", "Hi2"])
        plt.text(1250, 1500, f"Sound frequency: \n {data_frequency[i]} Hz", fontsize=14, verticalalignment="top", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8) )

        
        # Save image frames in current directory
        plt.savefig(f"sweep{i}.png", bbox_inches='tight')
        
        plt.tight_layout()
        

    ani = animation.FuncAnimation(plt.gcf(), animate, frames= np.size(data, 1)-1, repeat=False,
                                  interval=1)
    plt.show()
    
if __name__ == "__main__":
    main()
