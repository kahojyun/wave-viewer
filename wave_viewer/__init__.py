"""
Wave Viewer
===========

A simple GUI for viewing waveforms. It plots the waveform with vispy in a
separate process. The GUI is built with PySide6.

The `WaveViewer` class is the main interface for the wave_viewer package. It
provides methods for adding and removing lines from the plot, clearing the plot,
and closing the GUI.
"""

from importlib import metadata

from ._controller import WaveViewer

__all__ = ["WaveViewer"]

# from setuptools-scm docs
try:
    __version__ = metadata.version("wave-viewer")
except metadata.PackageNotFoundError:
    # package is not installed
    pass
