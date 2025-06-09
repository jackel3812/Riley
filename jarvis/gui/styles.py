"""
GUI Styles - Style definitions for the J.A.R.V.I.S. GUI.
"""

import os
import logging
from PyQt5.QtGui import QPalette, QColor

# Style constants
DARK_STYLE = "dark"
LIGHT_STYLE = "light"

# Dark theme palette
DARK_PALETTE = {
    "window": QColor(30, 30, 30),
    "window_text": QColor(240, 240, 240),
    "base": QColor(40, 40, 40),
    "alternate_base": QColor(45, 45, 45),
    "text": QColor(240, 240, 240),
    "button": QColor(60, 60, 60),
    "button_text": QColor(240, 240, 240),
    "bright_text": QColor(0, 191, 255),  # Deep Sky Blue
    "highlight": QColor(0, 127, 215),
    "highlight_text": QColor(255, 255, 255),
    "tooltip_base": QColor(50, 50, 50),
    "tooltip_text": QColor(240, 240, 240),
    "link": QColor(0, 191, 255),
    "accent": QColor(0, 191, 255)
}

# Light theme palette
LIGHT_PALETTE = {
    "window": QColor(240, 240, 240),
    "window_text": QColor(10, 10, 10),
    "base": QColor(255, 255, 255),
    "alternate_base": QColor(245, 245, 245),
    "text": QColor(10, 10, 10),
    "button": QColor(230, 230, 230),
    "button_text": QColor(10, 10, 10),
    "bright_text": QColor(0, 0, 0),
    "highlight": QColor(0, 120, 210),
    "highlight_text": QColor(255, 255, 255),
    "tooltip_base": QColor(230, 230, 230),
    "tooltip_text": QColor(10, 10, 10),
    "link": QColor(0, 120, 210),
    "accent": QColor(0, 120, 210)
}

# Dark theme stylesheet
DARK_STYLESHEET = """
QMainWindow, QWidget {
    background-color: #1e1e1e;
    color: #f0f0f0;
}

QFrame#headerFrame, QFrame#footerFrame {
    background-color: #262626;
    border-radius: 5px;
    padding: 5px;
}

QFrame#monitorFrame {
    background-color: #262626;
    border-radius: 5px;
    padding: 10px;
    margin: 5px;
}

QTabWidget::pane {
    border: 1px solid #555555;
    border-radius: 5px;
    top: -1px;
    background-color: #262626;
}

QTabBar::tab {
    background-color: #363636;
    color: #f0f0f0;
    min-width: 100px;
    padding: 8px 12px;
    margin-right: 2px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

QTabBar::tab:selected {
    background-color: #00BFFF;
    color: #ffffff;
}

QTabBar::tab:!selected {
    margin-top: 2px;
}

QTextEdit, QLineEdit {
    background-color: #262626;
    color: #f0f0f0;
    border: 1px solid #555555;
    border-radius: 5px;
    padding: 5px;
}

QTextEdit#chatDisplay {
    background-color: #262626;
    color: #f0f0f0;
    font-size: 14px;
}

QTextEdit#systemDetails {
    background-color: #262626;
    color: #f0f0f0;
    font-family: Consolas, Monaco, monospace;
    font-size: 12px;
}

QPushButton {
    background-color: #3c3c3c;
    color: #f0f0f0;
    border: 1px solid #555555;
    border-radius: 5px;
    padding: 8px 16px;
    margin: 2px;
}

QPushButton:hover {
    background-color: #4c4c4c;
    border: 1px solid #666666;
}

QPushButton:pressed {
    background-color: #2c2c2c;
}

QPushButton:checked {
    background-color: #00BFFF;
    color: #ffffff;
}

QProgressBar {
    border: 1px solid #555555;
    border-radius: 5px;
    text-align: center;
    background-color: #262626;
}

QProgressBar::chunk {
    background-color: #00BFFF;
    width: 10px;
    margin: 0.5px;
}

QScrollBar:vertical {
    border: none;
    background-color: #262626;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #555555;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #666666;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #262626;
    height: 10px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background-color: #555555;
    min-width: 20px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #666666;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QLabel {
    color: #f0f0f0;
}

QSplitter::handle {
    background-color: #555555;
}

QMenuBar {
    background-color: #262626;
    color: #f0f0f0;
}

QMenuBar::item {
    background: transparent;
    padding: 5px 10px;
}

QMenuBar::item:selected {
    background-color: #00BFFF;
    color: #ffffff;
}

QMenu {
    background-color: #262626;
    color: #f0f0f0;
    border: 1px solid #555555;
}

QMenu::item {
    padding: 5px 20px 5px 20px;
}

QMenu::item:selected {
    background-color: #00BFFF;
    color: #ffffff;
}

QMenu::separator {
    height: 1px;
    background-color: #555555;
    margin: 5px 10px;
}

QToolTip {
    background-color: #262626;
    color: #f0f0f0;
    border: 1px solid #555555;
    border-radius: 3px;
}
"""

# Light theme stylesheet
LIGHT_STYLESHEET = """
QMainWindow, QWidget {
    background-color: #f0f0f0;
    color: #0a0a0a;
}

QFrame#headerFrame, QFrame#footerFrame {
    background-color: #e0e0e0;
    border-radius: 5px;
    padding: 5px;
}

QFrame#monitorFrame {
    background-color: #e0e0e0;
    border-radius: 5px;
    padding: 10px;
    margin: 5px;
}

QTabWidget::pane {
    border: 1px solid #c0c0c0;
    border-radius: 5px;
    top: -1px;
    background-color: #e0e0e0;
}

QTabBar::tab {
    background-color: #d0d0d0;
    color: #0a0a0a;
    min-width: 100px;
    padding: 8px 12px;
    margin-right: 2px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

QTabBar::tab:selected {
    background-color: #0078d2;
    color: #ffffff;
}

QTabBar::tab:!selected {
    margin-top: 2px;
}

QTextEdit, QLineEdit {
    background-color: #ffffff;
    color: #0a0a0a;
    border: 1px solid #c0c0c0;
    border-radius: 5px;
    padding: 5px;
}

QTextEdit#chatDisplay {
    background-color: #ffffff;
    color: #0a0a0a;
    font-size: 14px;
}

QTextEdit#systemDetails {
    background-color: #ffffff;
    color: #0a0a0a;
    font-family: Consolas, Monaco, monospace;
    font-size: 12px;
}

QPushButton {
    background-color: #e6e6e6;
    color: #0a0a0a;
    border: 1px solid #c0c0c0;
    border-radius: 5px;
    padding: 8px 16px;
    margin: 2px;
}

QPushButton:hover {
    background-color: #d6d6d6;
    border: 1px solid #b0b0b0;
}

QPushButton:pressed {
    background-color: #f6f6f6;
}

QPushButton:checked {
    background-color: #0078d2;
    color: #ffffff;
}

QProgressBar {
    border: 1px solid #c0c0c0;
    border-radius: 5px;
    text-align: center;
    background-color: #ffffff;
}

QProgressBar::chunk {
    background-color: #0078d2;
    width: 10px;
    margin: 0.5px;
}

QScrollBar:vertical {
    border: none;
    background-color: #e0e0e0;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #c0c0c0;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #a0a0a0;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #e0e0e0;
    height: 10px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background-color: #c0c0c0;
    min-width: 20px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #a0a0a0;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QLabel {
    color: #0a0a0a;
}

QSplitter::handle {
    background-color: #c0c0c0;
}

QMenuBar {
    background-color: #e0e0e0;
    color: #0a0a0a;
}

QMenuBar::item {
    background: transparent;
    padding: 5px 10px;
}

QMenuBar::item:selected {
    background-color: #0078d2;
    color: #ffffff;
}

QMenu {
    background-color: #e0e0e0;
    color: #0a0a0a;
    border: 1px solid #c0c0c0;
}

QMenu::item {
    padding: 5px 20px 5px 20px;
}

QMenu::item:selected {
    background-color: #0078d2;
    color: #ffffff;
}

QMenu::separator {
    height: 1px;
    background-color: #c0c0c0;
    margin: 5px 10px;
}

QToolTip {
    background-color: #e0e0e0;
    color: #0a0a0a;
    border: 1px solid #c0c0c0;
    border-radius: 3px;
}
"""

def get_style_sheet(theme):
    """Get the stylesheet for a theme.
    
    Args:
        theme: Theme name ('dark' or 'light')
        
    Returns:
        Stylesheet string
    """
    if theme == LIGHT_STYLE:
        return LIGHT_STYLESHEET
    else:
        return DARK_STYLESHEET

def apply_style(widget, theme):
    """Apply a theme to a widget.
    
    Args:
        widget: Widget to style
        theme: Theme name ('dark' or 'light')
    """
    logger = logging.getLogger(__name__)
    
    # Set stylesheet
    widget.setStyleSheet(get_style_sheet(theme))
    
    # Set palette
    palette = QPalette()
    
    if theme == LIGHT_STYLE:
        colors = LIGHT_PALETTE
    else:
        colors = DARK_PALETTE
    
    # Set palette colors
    palette.setColor(QPalette.Window, colors["window"])
    palette.setColor(QPalette.WindowText, colors["window_text"])
    palette.setColor(QPalette.Base, colors["base"])
    palette.setColor(QPalette.AlternateBase, colors["alternate_base"])
    palette.setColor(QPalette.Text, colors["text"])
    palette.setColor(QPalette.Button, colors["button"])
    palette.setColor(QPalette.ButtonText, colors["button_text"])
    palette.setColor(QPalette.BrightText, colors["bright_text"])
    palette.setColor(QPalette.Highlight, colors["highlight"])
    palette.setColor(QPalette.HighlightedText, colors["highlight_text"])
    palette.setColor(QPalette.ToolTipBase, colors["tooltip_base"])
    palette.setColor(QPalette.ToolTipText, colors["tooltip_text"])
    palette.setColor(QPalette.Link, colors["link"])
    
    widget.setPalette(palette)
    
    logger.debug(f"Applied {theme} theme to widget")
