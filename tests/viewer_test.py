import time
import unittest

import numpy as np

from wave_viewer import WaveViewer


class TestWaveViewer(unittest.TestCase):
    def test_all(self):
        wv = WaveViewer()
        x = np.linspace(0, 2 * np.pi, 100)
        wv.add_line("sin", x + 1, [np.sin(x)], 0)
        wv.add_line("cos", x, [np.cos(x)], 2)
        wv.add_line("cossin", x, [np.cos(x), np.sin(x)], 4)
        wv.autoscale()
        time.sleep(3.5)
        wv.remove_line("cos")
        wv.remove_line("sin")
        wv.autoscale()
        time.sleep(1.5)
        wv.clear()
        time.sleep(1.5)
        wv.close()


if __name__ == "__main__":
    unittest.main()
