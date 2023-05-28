"""
The WaveViewer class is the main interface for the wave_viewer package. It
provides methods for adding and removing lines from the plot, clearing the plot,
and closing the GUI.
"""
import multiprocessing as mp

import numpy as np

from ._viewer import main


class WaveViewer:
    """A simple GUI for viewing waveforms.

    It plots the waveform with vispy in a separate process. The GUI is built with
    PySide6.


    Parameters
    ----------
    daemon : bool, optional
        If True, the viewer process is a daemon process. This means that the
        process will be terminated when the main process exits. If False, the
        viewer process will continue to run after the main process exits. In this
        case, the viewer process must be closed manually by calling the `close`
        method. The default is True.
    """

    def __init__(self, daemon: bool = True) -> None:
        self._conn = mp.Queue()
        self._process = mp.Process(target=main, args=(self._conn,), daemon=daemon)
        self._process.start()

    def _ensure_open(self) -> None:
        if not self._process.is_alive():
            raise RuntimeError("WaveViewer is closed")

    def add_line(self, name: str, t: np.ndarray, ys: list, offset: float) -> None:
        """Add a line to the plot.

        The method accepts a list of y values and plots them against the time axis.
        The y values are plotted with different colors. The name will also be added
        to the right of the line.

        If a line with the same name already exists, it is replaced.

        Parameters
        ----------
        name : str
            The name of the line.
        t : np.ndarray
            The time axis.
        ys : list of np.ndarray
            The y values.
        offset : float
            The offset of the line.

        Warning
        -------
        The WaveViewer class uses `multiprocessing.Pipe` to communicate with the
        separate process, which may fail if the message size is too large. If you
        encounter this issue, try reducing the number of points in the waveform.

        Raises
        ------
        TypeError
            If name is not a string, t is not a numpy array, or ys is not a list.
        ValueError
            If t is not 1D, or if ys does not have the same shape as t.
        RuntimeError
            If the WaveViewer is closed.
        """
        self._ensure_open()
        # check inputs
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(t, np.ndarray):
            raise TypeError("t must be a numpy array")
        if not isinstance(ys, list):
            raise TypeError("ys must be a list")
        offset = float(offset)
        if t.ndim != 1:
            raise ValueError("t must be 1D")
        for y in ys:
            if not isinstance(y, np.ndarray):
                raise TypeError("ys must be a list of numpy arrays")
            if y.ndim != 1:
                raise ValueError("ys must be a list of 1D numpy arrays")
            if y.shape != t.shape:
                raise ValueError("ys must have the same shape as t")
        msg = {
            "type": "add_line",
            "name": name,
            "t": t,
            "ys": ys,
            "offset": offset,
        }
        self._conn.put(msg)

    def remove_line(self, name: str) -> None:
        """Remove a line from the plot.

        Parameters
        ----------
        name : str
            The name of the line.

        Raises
        ------
        TypeError
            If name is not a string.
        RuntimeError
            If the WaveViewer is closed.
        """
        self._ensure_open()
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        msg = {"type": "remove_line", "name": name}
        self._conn.put(msg)

    def clear(self) -> None:
        """Clear the plot.

        Raises
        ------
        RuntimeError
            If the WaveViewer is closed.
        """
        self._ensure_open()
        msg = {"type": "clear"}
        self._conn.put(msg)

    def autoscale(self) -> None:
        """Autoscale the plot.

        Raises
        ------
        RuntimeError
            If the WaveViewer is closed.
        """
        self._ensure_open()
        msg = {"type": "autoscale"}
        self._conn.put(msg)

    def close(self) -> None:
        """Close the WaveViewer."""
        self._process.terminate()
        self._process.join()
        self._conn.close()

    def wait(self) -> None:
        """Wait for the WaveViewer to close."""
        self._process.join()
