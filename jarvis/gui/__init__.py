"""
GUI modules for the J.A.R.V.I.S. system.
This package contains the graphical user interface components.
"""

# Import GUI components for easier access
from jarvis.gui.main_window import JarvisGUI
from jarvis.gui.widgets import (
    CircularProgressBar, EnergyCore, VoiceWaveform,
    AnimatedButton, TransparentLineEdit, HolographicDisplay
)
from jarvis.gui.styles import (
    DARK_STYLE, LIGHT_STYLE, get_style_sheet, apply_style
)
