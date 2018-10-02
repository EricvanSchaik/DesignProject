import pandas as pd


names = ["Time", "Ax", "Ay", "Az", "Gx", "Gy", "Gz", "Mx", "My", "Mz", "T"]
data = pd.read_csv("../data/DATA-001.CSV", header=None, names=names, comment=";")

data.eval("Ax = Ax * 9.807 / 4096", inplace=True)
data.eval("Ay = Ay * 9.807 / 4096", inplace=True)
data.eval("Az = Az * 9.807 / 4096", inplace=True)

data.eval("Vector = (Ax**2 + Ay**2 + Az**2)**0.5", inplace=True)
print(data.head())
