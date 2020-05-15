from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from itertools import count

root = Tk()
root.title("Radar Instrument GUI")
# root.iconbitmap()
root.geometry("400x200")

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()


def animate(i):
    x_vals.append(next(index))
    y_vals.append(random.randint(0, 5))

    plt.cla()
    plt.plot(x_vals, y_vals)


def graph():
    #house_prices = np.random.normal(200000, 25000, 5000)
    # plt.hist(house_prices)
    ani = FuncAnimation(plt.gcf(), animate, interval=10)
    plt.tight_layout()
    plt.show()


button = Button(root, text="Open Graph", command=graph)
button.pack()

#myLabel = Label(root, text="Hi there!")
# myLabel.pack()

root.mainloop()
