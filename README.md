# Wave Viewer

A simple GUI for viewing waveforms. It plots the waveform with vispy in a
separate process. The GUI is built with PySide6.

The `WaveViewer` class is the main interface for the wave_viewer package. It
provides methods for adding and removing lines from the plot, clearing the plot,
and closing the GUI.

## Installation

```bash
pip install wave-viewer
```

## Usage

Below is a simple example of how to use the `WaveViewer` class. Avoid calling
`clear` if you only want to update the plot. It is more efficient to update the
plot with `add_line`.

```python
from wave_viewer import WaveViewer
import numpy as np


# This if statement is required for multiprocessing on Windows
if __name__ == "__main__":
    # Create the viewer
    viewer = WaveViewer()

    # Add a line to the plot
    x = np.arange(100000) / 2e9
    y = np.exp(1j * 2 * np.pi * 1e6 * x)
    ys = [y.real, y.imag]
    viewer.add_line("line1", x, ys, offset=0)

    # Add another line to the plot
    viewer.add_line("line2", x, ys, offset=2)

    # Auto scale the plot
    viewer.autoscale()

    # Remove the first line
    viewer.remove_line("line1")

    # Replace the second line
    y = np.exp(1j * 2 * np.pi * 2e6 * x)
    ys = [y.real, y.imag]
    viewer.add_line("line2", x, ys, offset=2)

    # Clear the plot
    viewer.clear()

    # Close the GUI
    viewer.close()
```
