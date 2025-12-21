import pandas as pd
import matplotlib.pyplot as plt

filename = "test.ods"

df = pd.read_csv(filename, sep=r"\s+", skiprows=1)

plt.plot(df["Gen"], df["tDistMax"])
plt.xlabel("Generation")
plt.ylabel("tDistMax")
plt.grid(True)
plt.show()