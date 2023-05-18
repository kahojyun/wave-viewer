"""
Wave Viewer
===========

A simple GUI for viewing waveforms. It plots the waveform with vispy in a
separate process. The GUI is built with PySide6.

The `WaveViewer` class is the main interface for the wave_viewer package. It
provides methods for adding and removing lines from the plot, clearing the plot,
and closing the GUI.
"""

from ._controller import WaveViewer

__all__ = ["WaveViewer"]
