import numpy as np
import pyqtgraph as pg

n = 100000
sr = 2e9
t = np.arange(n) / sr
f = 250e6
y = 0.4 * np.sin(2 * np.pi * f * t)

data = y
w = pg.plot(
    data,
    title="Simplest possible plotting example",
)
w.getPlotItem().setDownsampling(auto=True, mode="peak")
w.getPlotItem().setClipToView(True)
for i in range(1, 60):
    w.plot(data + i)

# data = np.random.normal(size=(500,500))
# pg.image(data, title="Simplest possible image example")

if __name__ == "__main__":
    pg.exec()
