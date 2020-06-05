from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from itertools import count
import radar

root = Tk()
root.title("Radar Instrument GUI")
# root.iconbitmap()
# root.geometry("400x400")

frame = LabelFrame(root, text="Graph Container", padx=50, pady=50)
frame.grid(row=2, column=2, padx=10, pady=10)

plt.style.use('fivethirtyeight')

x_vals = np.arange(0, 4408)
y_wave = np.arange(0, 4408)
fs = 44100  						# Sample frequency of sound wave
freq = 220.0                            # Sound frequency in Hz
duration = 0.1	                    # Duration in s of audio output
samples = np.arange(duration*fs)


def animate(i):
    # set x and y instead of appending them for the instrument
    # the x_vec will be a linspace created here from points 1 to 4408
    # Add After=graphical.target in the unit section of the systemd file!
    # sudo cp <service file location> <destination direction /lib/systemd/system/>

    plt.cla()
    global x_vals
    #x_vals = np.arange(x_vals.size, 2*x_vals.size)
    x_vals = [a + 4408 for a in x_vals]
    global freq
    freq = freq + random.randint(-50, 50)
    #y_wave = np.sin(2*np.pi*samples*freq/fs)[0:4408]
    plt.plot(x_vals, y_wave)


def graph():
    ani = FuncAnimation(plt.gcf(), animate, repeat=False, interval=100)
    plt.tight_layout()
    plt.show()
    
def updateWave(interrupt_handler, shared_wave):
    global y_wave
    while not interrupt_handler.got_signal: 
        y_wave = shared_wave


def printme():
    print("hello")


# Drop Down Menus

def show():
    #menuLabel = Label(frame, text=clicked.get()).grid(row=2, column=2)
    print(clicked.get())


options = [
    "Effect 1",
    "Effect 2",
    "Effect 3",
    "Effect 4"
]

clicked = StringVar()
clicked.set(options[0])

# Radio Buttons
r = IntVar()
r.set("2")


def selected(value):
    myLabel = Label(frame, text=f'This is option {value}')
    myLabel.grid(row=1, column=3)


def main(shared_wave):
    #global y_wave
    #y_wave = wave[:]

    button = Button(frame, text="Open Graph", relief='flat',
                    fg="green", command=graph)
    button2 = Button(frame, text="Print ME", relief='flat',
                     fg="blue", command=printme)
    button.grid(row=0, column=0)
    button2.grid(row=0, column=1)
    #button.place(bordermode=OUTSIDE, height=100, width=100, x=100, y=100)
    #button2.place(bordermode=OUTSIDE, height=100, width=100, x=200, y=100)
    # button.pack()
    # button2.pack()

    radio1 = Radiobutton(frame, text="Option 1", variable=r,
                         value=1, command=lambda: selected(r.get()))
    radio2 = Radiobutton(frame, text="Option 2", variable=r,
                         value=2, command=lambda: selected(r.get()))
    radio1.grid(row=1, column=0)
    radio2.grid(row=1, column=1)

    menu = OptionMenu(frame, clicked, *options).grid(row=2, column=0)

    menuButton = Button(frame, text="show menu item",
                        command=show).grid(row=2, column=1)
    root.mainloop()
        

if __name__ == "__main__":
    
    main()
