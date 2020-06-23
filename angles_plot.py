import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")

fig, axs = plt.subplots(3)
        
hor = np.loadtxt("horizontal_angle.csv", delimiter=",")
ver = np.loadtxt("vertical_angle.csv", delimiter=",")
middle = np.loadtxt("middle.csv", delimiter=",")

x = np.arange(np.size(ver, 1))

mean_middle = np.mean(middle, axis=0)
mean_ver = np.mean(ver, axis=0)
mean_hor = np.mean(hor, axis=0)

axs[0].plot(x, mean_middle, color="b")
axs[1].plot(x, mean_ver, color="r")
axs[2].plot(x, mean_hor, color="g")

for ax in axs:
	ax.set_ylabel("Amplitude")
	ax.set_xlabel("Distance from sensor")

axs[0].legend(["0$^\circ$ center"])
axs[0].set_title("Centered at maximum amplitude")
axs[1].legend(["9.45$^\circ$ elevation"])
axs[1].set_title("Elevation HPBW")
axs[2].legend(["12.35$^\circ$ horizontal"])
axs[2].set_title("Horizontal HPBW")

plt.tight_layout()

plt.show()
