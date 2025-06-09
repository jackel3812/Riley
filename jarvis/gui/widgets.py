"""
Custom Widgets - Custom UI widgets for the J.A.R.V.I.S. GUI.
"""

import math
import logging
import random
from datetime import datetime

# Try importing PyQt5 for GUI
try:
    from PyQt5.QtWidgets import (
        QWidget, QProgressBar, QSizePolicy, QPushButton,
        QLineEdit, QLabel, QVBoxLayout, QHBoxLayout
    )
    from PyQt5.QtCore import (
        Qt, QTimer, QSize, QRectF, QPointF, QPropertyAnimation,
        pyqtProperty, QSequentialAnimationGroup, QPauseAnimation, QEasingCurve
    )
    from PyQt5.QtGui import (
        QPainter, QColor, QFont, QPen, QBrush, QRadialGradient,
        QLinearGradient, QPainterPath, QConicalGradient, QFontMetrics
    )
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    QWidget = object  # Fallback base class

class CircularProgressBar(QWidget):
    """Custom circular progress bar widget."""
    
    def __init__(self, parent=None):
        """Initialize the circular progress bar.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Properties
        self._value = 0
        self._maximum = 100
        self._minimum = 0
        self._prefix = ""
        self._suffix = "%"
        self._text_visible = True
        
        # Style
        self._bar_color = QColor("#00BFFF")  # Deep Sky Blue
        self._background_color = QColor(40, 40, 40, 100)
        self._text_color = QColor(255, 255, 255)
        
        # Size
        self.setMinimumSize(100, 100)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        # Animation
        self._animation_value = 0
        self._animation = QPropertyAnimation(self, b"animationValue")
        self._animation.setDuration(500)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def setValue(self, value):
        """Set the progress value.
        
        Args:
            value: Progress value (0-100)
        """
        # Constrain value to range
        value = max(self._minimum, min(self._maximum, value))
        
        if self._value != value:
            # Start animation
            self._animation.stop()
            self._animation.setStartValue(self._animation_value)
            self._animation.setEndValue(value)
            self._animation.start()
            
            self._value = value
            self.update()
    
    def setRange(self, minimum, maximum):
        """Set the progress range.
        
        Args:
            minimum: Minimum value
            maximum: Maximum value
        """
        if minimum < maximum:
            self._minimum = minimum
            self._maximum = maximum
            
            # Constrain value to new range
            self.setValue(self._value)
            self.update()
    
    def setBarColor(self, color):
        """Set the color of the progress bar.
        
        Args:
            color: QColor instance
        """
        self._bar_color = color
        self.update()
    
    def value(self):
        """Get the current progress value.
        
        Returns:
            Current value
        """
        return self._value
    
    def animationValue(self):
        """Get the animation value for property animation.
        
        Returns:
            Animation value
        """
        return self._animation_value
    
    def setAnimationValue(self, value):
        """Set the animation value.
        
        Args:
            value: New animation value
        """
        self._animation_value = value
        self.update()
    
    # Define property for animation
    animationValue = pyqtProperty(float, animationValue, setAnimationValue)
    
    def paintEvent(self, event):
        """Paint the progress bar.
        
        Args:
            event: Paint event
        """
        # Initialize painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate dimensions
        width = self.width()
        height = self.height()
        size = min(width, height)
        
        # Center the drawing
        painter.translate(width / 2, height / 2)
        painter.scale(size / 200.0, size / 200.0)
        
        # Draw background
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._background_color)
        painter.drawEllipse(QRectF(-90, -90, 180, 180))
        
        # Draw progress bar
        pen = QPen(self._bar_color)
        pen.setWidth(10)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        
        # Calculate span angle for current value
        span_angle = int(360.0 * (self._animation_value - self._minimum) / 
                          (self._maximum - self._minimum))
        
        # Draw arc
        painter.drawArc(QRectF(-85, -85, 170, 170), 90 * 16, -span_angle * 16)
        
        # Draw text
        if self._text_visible:
            painter.setPen(self._text_color)
            painter.setBrush(Qt.NoBrush)
            
            font = QFont("Helvetica", 25, QFont.Bold)
            painter.setFont(font)
            
            text = f"{self._prefix}{int(self._animation_value)}{self._suffix}"
            painter.drawText(QRectF(-80, -40, 160, 80), Qt.AlignCenter, text)
    
    def sizeHint(self):
        """Get the recommended size.
        
        Returns:
            Recommended size
        """
        return QSize(120, 120)

class EnergyCore(QWidget):
    """Iron Man-style energy core widget."""
    
    def __init__(self, parent=None, size=100):
        """Initialize the energy core widget.
        
        Args:
            parent: Parent widget
            size: Widget size
        """
        super().__init__(parent)
        
        # Properties
        self._size = size
        self._pulse_factor = 1.0
        self._power_level = 100.0
        self._rotation = 0.0
        
        # Size
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)
        
        # Animation timers
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._update_pulse)
        self._pulse_timer.start(50)
        
        self._rotation_timer = QTimer(self)
        self._rotation_timer.timeout.connect(self._update_rotation)
        self._rotation_timer.start(30)
    
    def setPowerLevel(self, level):
        """Set the power level of the energy core.
        
        Args:
            level: Power level (0-100)
        """
        self._power_level = max(0, min(100, level))
        self.update()
    
    def pulse(self):
        """Trigger a pulse animation."""
        # Start a pulse effect
        self._pulse_factor = 1.3
    
    def _update_pulse(self):
        """Update the pulse animation."""
        # Gradually return to normal
        if self._pulse_factor > 1.0:
            self._pulse_factor = max(1.0, self._pulse_factor - 0.05)
            self.update()
    
    def _update_rotation(self):
        """Update the rotation animation."""
        self._rotation = (self._rotation + 1) % 360
        self.update()
    
    def paintEvent(self, event):
        """Paint the energy core.
        
        Args:
            event: Paint event
        """
        # Initialize painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate dimensions
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) / 2 * self._pulse_factor
        
        # Draw outer ring
        outer_gradient = QRadialGradient(center_x, center_y, radius)
        ring_color = QColor(0, 191, 255, 200)  # Deep Sky Blue
        
        # Adjust color based on power level
        if self._power_level < 50:
            # Transition to orange then red as power decreases
            hue = int(120 * (self._power_level / 50.0))  # 0 = red, 60 = yellow, 120 = green
            ring_color = QColor.fromHsv(hue, 255, 255, 200)
        
        outer_gradient.setColorAt(0.8, ring_color)
        outer_gradient.setColorAt(1.0, QColor(0, 0, 0, 0))
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(outer_gradient))
        painter.drawEllipse(QRectF(
            center_x - radius,
            center_y - radius,
            radius * 2,
            radius * 2
        ))
        
        # Draw inner core
        inner_radius = radius * 0.6
        inner_gradient = QRadialGradient(center_x, center_y, inner_radius)
        
        core_color = QColor(0, 191, 255, 200)  # Deep Sky Blue
        
        # Adjust color based on power level
        if self._power_level < 50:
            # Transition to orange then red as power decreases
            hue = int(120 * (self._power_level / 50.0))  # 0 = red, 60 = yellow, 120 = green
            core_color = QColor.fromHsv(hue, 255, 255, 200)
        
        inner_gradient.setColorAt(0.0, QColor(255, 255, 255, 230))
        inner_gradient.setColorAt(0.4, core_color)
        inner_gradient.setColorAt(1.0, QColor(0, 0, 0, 0))
        
        painter.setBrush(QBrush(inner_gradient))
        painter.drawEllipse(QRectF(
            center_x - inner_radius,
            center_y - inner_radius,
            inner_radius * 2,
            inner_radius * 2
        ))
        
        # Draw rotating segments
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self._rotation)
        
        segment_radius = radius * 0.9
        segment_width = 10
        num_segments = 6
        
        pen = QPen(core_color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        
        for i in range(num_segments):
            angle = i * (360 / num_segments)
            painter.save()
            painter.rotate(angle)
            
            # Draw triangular segment
            path = QPainterPath()
            path.moveTo(segment_radius - segment_width, 0)
            path.lineTo(segment_radius, segment_width / 2)
            path.lineTo(segment_radius, -segment_width / 2)
            path.closeSubpath()
            
            painter.drawPath(path)
            painter.restore()
        
        painter.restore()

class VoiceWaveform(QWidget):
    """Voice waveform visualization widget."""
    
    def __init__(self, parent=None):
        """Initialize the voice waveform widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Properties
        self._active = False
        self._amplitude = 0.0
        self._points = []
        self._num_points = 100
        
        # Initialize points
        for i in range(self._num_points):
            self._points.append(0.0)
        
        # Animation timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_waveform)
        self._timer.start(30)  # 30ms updates (about 33 fps)
        
        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(30, 30, 30))
        self.setPalette(palette)
    
    def setActive(self, active):
        """Set whether the waveform is active.
        
        Args:
            active: True if active, False otherwise
        """
        self._active = active
        
        if not active:
            # Reset waveform
            for i in range(self._num_points):
                self._points[i] = 0.0
        
        self.update()
    
    def pulse(self):
        """Trigger a pulse in the waveform."""
        # Set a high amplitude that will decay
        self._amplitude = 1.0
    
    def _update_waveform(self):
        """Update the waveform animation."""
        if self._active:
            # Decay amplitude
            self._amplitude = max(0.2, self._amplitude * 0.95)
            
            # Generate new point with random variation
            new_point = self._amplitude * (0.5 + 0.5 * random.random())
            
            # Shift points
            self._points.pop(0)
            self._points.append(new_point)
            
            # Randomly add a pulse
            if random.random() < 0.05:
                self.pulse()
            
        else:
            # When inactive, animate to flat line
            for i in range(len(self._points)):
                self._points[i] *= 0.9
        
        self.update()
    
    def paintEvent(self, event):
        """Paint the waveform.
        
        Args:
            event: Paint event
        """
        # Initialize painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate dimensions
        width = self.width()
        height = self.height()
        center_y = height / 2
        
        # Draw waveform
        path = QPainterPath()
        
        # Starting point
        path.moveTo(0, center_y)
        
        # Draw each point
        point_width = width / self._num_points
        
        for i, point in enumerate(self._points):
            x = i * point_width
            y = center_y - (point * center_y * 0.8)
            path.lineTo(x, y)
        
        # Complete path to make closed shape for filling
        path.lineTo(width, center_y)
        path.lineTo(0, center_y)
        
        # Create gradient
        gradient = QLinearGradient(0, 0, 0, height)
        
        if self._active:
            gradient.setColorAt(0, QColor(0, 191, 255, 150))  # Deep Sky Blue
            gradient.setColorAt(1, QColor(0, 65, 155, 80))
        else:
            gradient.setColorAt(0, QColor(100, 100, 100, 150))
            gradient.setColorAt(1, QColor(50, 50, 50, 80))
        
        # Fill the path
        painter.fillPath(path, gradient)
        
        # Draw the path outline
        pen = QPen(QColor(0, 191, 255) if self._active else QColor(120, 120, 120))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # Draw horizontal midline
        pen = QPen(QColor(255, 255, 255, 30))
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(0, center_y, width, center_y)

class AnimatedButton(QPushButton):
    """Button with animation effects."""
    
    def __init__(self, text="", parent=None):
        """Initialize the animated button.
        
        Args:
            text: Button text
            parent: Parent widget
        """
        super().__init__(text, parent)
        
        # Properties
        self._hover = False
        self._press = False
        
        # Styling
        self.setAutoFillBackground(True)
        self.setCursor(Qt.PointingHandCursor)
        
        # Fixed size if no text
        if not text:
            self.setFixedSize(40, 40)
    
    def enterEvent(self, event):
        """Handle mouse enter event.
        
        Args:
            event: Mouse event
        """
        self._hover = True
        self.update()
    
    def leaveEvent(self, event):
        """Handle mouse leave event.
        
        Args:
            event: Mouse event
        """
        self._hover = False
        self.update()
    
    def mousePressEvent(self, event):
        """Handle mouse press event.
        
        Args:
            event: Mouse event
        """
        self._press = True
        self.update()
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release event.
        
        Args:
            event: Mouse event
        """
        self._press = False
        self.update()
        super().mouseReleaseEvent(event)
    
    def paintEvent(self, event):
        """Paint the button.
        
        Args:
            event: Paint event
        """
        # Let the default implementation draw the basic button
        super().paintEvent(event)
        
        # Add hover/press effects
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self._press:
            # Press effect - inner shadow
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 0, 40))
            painter.drawRoundedRect(self.rect(), 5, 5)
        elif self._hover:
            # Hover effect - glow
            painter.setPen(Qt.NoPen)
            
            # Draw glow
            gradient = QRadialGradient(
                self.rect().center(),
                max(self.width(), self.height())
            )
            gradient.setColorAt(0, QColor(0, 191, 255, 40))  # Deep Sky Blue
            gradient.setColorAt(1, QColor(0, 0, 0, 0))
            
            painter.setBrush(gradient)
            painter.drawRoundedRect(self.rect(), 5, 5)

class TransparentLineEdit(QLineEdit):
    """Line edit with a semi-transparent background."""
    
    def __init__(self, parent=None):
        """Initialize the transparent line edit.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Styling
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid rgba(100, 100, 100, 150);
                border-radius: 5px;
                padding: 5px;
                background-color: rgba(30, 30, 30, 150);
                color: white;
                selection-background-color: rgba(0, 191, 255, 150);
            }
            
            QLineEdit:focus {
                border: 1px solid rgba(0, 191, 255, 200);
            }
        """)

class HolographicDisplay(QWidget):
    """Holographic-style display widget."""
    
    def __init__(self, parent=None):
        """Initialize the holographic display.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Properties
        self._text = []
        self._angle = 0.0
        self._opacity = 0.8
        
        # Animation timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_animation)
        self._timer.start(50)
        
        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(0, 0, 0, 0))
        self.setPalette(palette)
        
        # Initial text
        self.setText(["JARVIS", "Initializing..."])
    
    def setText(self, text_lines):
        """Set the text to display.
        
        Args:
            text_lines: List of text lines
        """
        self._text = text_lines
        self.update()
    
    def addText(self, text):
        """Add a line of text.
        
        Args:
            text: Text line to add
        """
        self._text.append(text)
        
        # Limit to 10 lines
        if len(self._text) > 10:
            self._text.pop(0)
        
        self.update()
    
    def _update_animation(self):
        """Update the animation."""
        self._angle = (self._angle + 2) % 360
        
        # Oscillate opacity
        self._opacity = 0.7 + 0.2 * math.sin(math.radians(self._angle))
        
        self.update()
    
    def paintEvent(self, event):
        """Paint the holographic display.
        
        Args:
            event: Paint event
        """
        # Initialize painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate dimensions
        width = self.width()
        height = self.height()
        
        # Create scanner line effect
        scan_y = height * (0.5 + 0.4 * math.sin(math.radians(self._angle)))
        
        # Draw background
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0, QColor(0, 191, 255, int(20 * self._opacity)))
        gradient.setColorAt(1, QColor(0, 65, 155, int(10 * self._opacity)))
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(), 10, 10)
        
        # Draw scanner line
        scanner_gradient = QLinearGradient(0, scan_y - 2, 0, scan_y + 2)
        scanner_gradient.setColorAt(0, QColor(0, 0, 0, 0))
        scanner_gradient.setColorAt(0.5, QColor(0, 191, 255, int(180 * self._opacity)))
        scanner_gradient.setColorAt(1, QColor(0, 0, 0, 0))
        
        painter.setBrush(scanner_gradient)
        painter.drawRect(0, scan_y - 2, width, 4)
        
        # Draw grid lines
        painter.setPen(QPen(QColor(0, 191, 255, int(40 * self._opacity)), 1, Qt.DotLine))
        
        # Horizontal grid lines
        line_spacing = 20
        for y in range(0, height, line_spacing):
            painter.drawLine(0, y, width, y)
        
        # Vertical grid lines
        for x in range(0, width, line_spacing):
            painter.drawLine(x, 0, x, height)
        
        # Draw text
        painter.setPen(QColor(0, 191, 255, int(230 * self._opacity)))
        font = QFont("Consolas", 10)
        painter.setFont(font)
        
        text_y = 20
        for line in self._text:
            # Check if line is near scanner line for highlight effect
            distance = abs(text_y - scan_y)
            if distance < 10:
                # Highlight text near scanner
                painter.setPen(QColor(255, 255, 255, int(255 * self._opacity)))
                glow_font = QFont("Consolas", 10, QFont.Bold)
                painter.setFont(glow_font)
            else:
                painter.setPen(QColor(0, 191, 255, int(230 * self._opacity)))
                painter.setFont(font)
            
            painter.drawText(10, text_y, line)
            text_y += 20
