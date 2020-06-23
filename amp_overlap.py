import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")

close = np.loadtxt("amp_close.csv", delimiter=",")
far = np.loadtxt("amp_far.csv", delimiter=",")

x = np.arange(np.size(close, 1))

mean_close = np.mean(close, axis=0)
mean_far = np.mean(far, axis=0)

plt.plot(x, mean_close, mean_far)
plt.tight_layout()

plt.legend(["Hand close to sensor", "Hand far away from sensor"])
plt.title("Typical detection data")
plt.ylabel("Amplitude")
plt.xlabel("Distance from sensor")

plt.savefig("AmpOverlap.png", bbox_inches='tight')

plt.show()

