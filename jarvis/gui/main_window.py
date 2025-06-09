"""
Main Window - The main GUI window for the J.A.R.V.I.S. system.
"""

import os
import sys
import logging
import time
from datetime import datetime
import threading

# Try importing PyQt5 for GUI
try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QTextEdit, QLineEdit, QTabWidget,
        QSystemTrayIcon, QMenu, QAction, QGridLayout, QFrame,
        QSplitter, QProgressBar, QScrollArea, QSizePolicy
    )
    from PyQt5.QtCore import Qt, QTimer, QSize, QThread, pyqtSignal, pyqtSlot, QUrl
    from PyQt5.QtGui import QIcon, QPixmap, QFont, QPalette, QColor, QMovie
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False

from jarvis.gui.widgets import (
    CircularProgressBar, EnergyCore, VoiceWaveform,
    AnimatedButton, TransparentLineEdit, HolographicDisplay
)
from jarvis.gui.styles import apply_style

class VoiceThread(QThread):
    """Thread for processing voice recognition."""
    
    text_captured = pyqtSignal(str)
    
    def __init__(self, voice_engine):
        """Initialize the voice thread.
        
        Args:
            voice_engine: Voice engine instance
        """
        super().__init__()
        self.voice_engine = voice_engine
        self.running = False
    
    def run(self):
        """Run the voice recognition thread."""
        self.running = True
        
        # Register callback for speech recognition
        if self.voice_engine:
            self.voice_engine.register_speech_callback(self.on_speech)
            
            # Start listening in this thread
            self.voice_engine.start_listening()
    
    def on_speech(self, text):
        """Callback for speech recognition.
        
        Args:
            text: Recognized speech text
        """
        self.text_captured.emit(text)
    
    def stop(self):
        """Stop the voice recognition thread."""
        self.running = False
        if self.voice_engine:
            self.voice_engine.stop_listening()

class JarvisGUI(QMainWindow):
    """Main GUI window for J.A.R.V.I.S."""
    
    def __init__(self, ai_engine, voice_engine, config):
        """Initialize the main window.
        
        Args:
            ai_engine: AI engine instance
            voice_engine: Voice engine instance
            config: Configuration object
        """
        if not PYQT_AVAILABLE:
            raise ImportError("PyQt5 is required for the GUI")
        
        super().__init__()
        
        self.logger = logging.getLogger(__name__)
        self.ai_engine = ai_engine
        self.voice_engine = voice_engine
        self.config = config
        
        # GUI state
        self.fullscreen = False
        self.voice_active = voice_engine is not None
        self.conversation_history = []
        
        # Initialize UI
        self._init_ui()
        
        # Start voice recognition thread if available
        if self.voice_active:
            self._start_voice_thread()
        
        # Register for AI engine callbacks
        self.ai_engine.register_response_callback(self.on_ai_response)
        
        # Setup system monitoring
        self._setup_system_monitor()
        
        # Create system tray icon
        self._create_system_tray()
        
        self.logger.info("JARVIS GUI initialized")
    
    def _init_ui(self):
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle("J.A.R.V.I.S.")
        self.setMinimumSize(1024, 768)
        
        # Set stylesheet
        apply_style(self, self.config.get('ui', 'theme', default='dark'))
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        
        # Header with Energy Core
        self._create_header()
        
        # Main content area with tabs
        self._create_main_content()
        
        # Footer with input and controls
        self._create_footer()
        
        # Setup timers for updates
        self._setup_timers()
    
    def _create_header(self):
        """Create the header section with Energy Core."""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        
        # Logo and title
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "jarvis_logo.svg")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(logo_pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo_label.setText("J.A.R.V.I.S.")
            logo_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        
        title_label = QLabel("J.A.R.V.I.S. - Just A Rather Very Intelligent System")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        # System time and date
        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 14px;")
        self.date_label = QLabel()
        self.date_label.setStyleSheet("font-size: 14px;")
        self._update_time()  # Initial update
        
        # Energy Core display
        self.energy_core = EnergyCore(size=60)
        
        # Add to layout
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        time_date_layout = QVBoxLayout()
        time_date_layout.addWidget(self.time_label, alignment=Qt.AlignRight)
        time_date_layout.addWidget(self.date_label, alignment=Qt.AlignRight)
        
        header_layout.addLayout(time_date_layout)
        header_layout.addWidget(self.energy_core)
        
        self.main_layout.addWidget(header_frame)
    
    def _create_main_content(self):
        """Create the main content area with tabs."""
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("mainTabs")
        
        # Chat tab
        self.chat_tab = QWidget()
        chat_layout = QVBoxLayout(self.chat_tab)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setObjectName("chatDisplay")
        
        # Voice waveform
        self.voice_waveform = VoiceWaveform()
        self.voice_waveform.setMinimumHeight(50)
        self.voice_waveform.setMaximumHeight(100)
        self.voice_waveform.setActive(self.voice_active)
        
        chat_layout.addWidget(self.chat_display)
        chat_layout.addWidget(self.voice_waveform)
        
        # System tab
        self.system_tab = QWidget()
        system_layout = QGridLayout(self.system_tab)
        
        # CPU usage
        cpu_frame = QFrame()
        cpu_frame.setObjectName("monitorFrame")
        cpu_layout = QVBoxLayout(cpu_frame)
        cpu_layout.setContentsMargins(10, 10, 10, 10)
        
        cpu_label = QLabel("CPU Usage")
        cpu_label.setStyleSheet("font-weight: bold;")
        self.cpu_progress = CircularProgressBar()
        self.cpu_progress.setFixedSize(120, 120)
        self.cpu_details = QLabel("Waiting for data...")
        
        cpu_layout.addWidget(cpu_label, alignment=Qt.AlignCenter)
        cpu_layout.addWidget(self.cpu_progress, alignment=Qt.AlignCenter)
        cpu_layout.addWidget(self.cpu_details, alignment=Qt.AlignCenter)
        
        # Memory usage
        memory_frame = QFrame()
        memory_frame.setObjectName("monitorFrame")
        memory_layout = QVBoxLayout(memory_frame)
        memory_layout.setContentsMargins(10, 10, 10, 10)
        
        memory_label = QLabel("Memory Usage")
        memory_label.setStyleSheet("font-weight: bold;")
        self.memory_progress = CircularProgressBar()
        self.memory_progress.setFixedSize(120, 120)
        self.memory_details = QLabel("Waiting for data...")
        
        memory_layout.addWidget(memory_label, alignment=Qt.AlignCenter)
        memory_layout.addWidget(self.memory_progress, alignment=Qt.AlignCenter)
        memory_layout.addWidget(self.memory_details, alignment=Qt.AlignCenter)
        
        # Battery status
        battery_frame = QFrame()
        battery_frame.setObjectName("monitorFrame")
        battery_layout = QVBoxLayout(battery_frame)
        battery_layout.setContentsMargins(10, 10, 10, 10)
        
        battery_label = QLabel("Battery Status")
        battery_label.setStyleSheet("font-weight: bold;")
        self.battery_progress = CircularProgressBar()
        self.battery_progress.setFixedSize(120, 120)
        self.battery_details = QLabel("Waiting for data...")
        
        battery_layout.addWidget(battery_label, alignment=Qt.AlignCenter)
        battery_layout.addWidget(self.battery_progress, alignment=Qt.AlignCenter)
        battery_layout.addWidget(self.battery_details, alignment=Qt.AlignCenter)
        
        # Energy Core status
        energy_frame = QFrame()
        energy_frame.setObjectName("monitorFrame")
        energy_layout = QVBoxLayout(energy_frame)
        energy_layout.setContentsMargins(10, 10, 10, 10)
        
        energy_label = QLabel("Energy Core")
        energy_label.setStyleSheet("font-weight: bold;")
        
        # Use a larger Energy Core display for this tab
        self.energy_core_display = EnergyCore(size=120)
        self.energy_details = QLabel("Energy Core Online")
        
        energy_layout.addWidget(energy_label, alignment=Qt.AlignCenter)
        energy_layout.addWidget(self.energy_core_display, alignment=Qt.AlignCenter)
        energy_layout.addWidget(self.energy_details, alignment=Qt.AlignCenter)
        
        # System details text
        self.system_details = QTextEdit()
        self.system_details.setReadOnly(True)
        self.system_details.setObjectName("systemDetails")
        self.system_details.setMinimumHeight(150)
        
        # Add to system layout
        system_layout.addWidget(cpu_frame, 0, 0)
        system_layout.addWidget(memory_frame, 0, 1)
        system_layout.addWidget(battery_frame, 0, 2)
        system_layout.addWidget(energy_frame, 0, 3)
        system_layout.addWidget(self.system_details, 1, 0, 1, 4)
        
        # Features tab
        self.features_tab = QWidget()
        features_layout = QVBoxLayout(self.features_tab)
        
        # Create a grid of feature buttons
        feature_grid = QGridLayout()
        
        # Feature buttons
        features = [
            {"name": "Weather", "icon": "☁️", "action": self._feature_weather},
            {"name": "News", "icon": "📰", "action": self._feature_news},
            {"name": "Web Search", "icon": "🔍", "action": self._feature_web_search},
            {"name": "Calendar", "icon": "📅", "action": self._feature_calendar},
            {"name": "Media Player", "icon": "🎵", "action": self._feature_media},
            {"name": "Email", "icon": "✉️", "action": self._feature_email},
            {"name": "Notes", "icon": "📝", "action": self._feature_notes},
            {"name": "Calculator", "icon": "🧮", "action": self._feature_calculator},
            {"name": "Wikipedia", "icon": "📚", "action": self._feature_wikipedia},
            {"name": "System Info", "icon": "💻", "action": self._feature_system_info},
            {"name": "Jokes", "icon": "😄", "action": self._feature_jokes},
            {"name": "Settings", "icon": "⚙️", "action": self._feature_settings}
        ]
        
        row, col = 0, 0
        for feature in features:
            button = AnimatedButton(f"{feature['icon']} {feature['name']}")
            button.clicked.connect(feature["action"])
            feature_grid.addWidget(button, row, col)
            
            col += 1
            if col > 3:  # 4 columns
                col = 0
                row += 1
        
        # Feature display area
        self.feature_display = QTextEdit()
        self.feature_display.setReadOnly(True)
        self.feature_display.setMinimumHeight(400)
        
        features_layout.addLayout(feature_grid)
        features_layout.addWidget(self.feature_display)
        
        # Add all tabs
        self.tab_widget.addTab(self.chat_tab, "Assistant")
        self.tab_widget.addTab(self.system_tab, "System")
        self.tab_widget.addTab(self.features_tab, "Features")
        
        self.main_layout.addWidget(self.tab_widget)
    
    def _create_footer(self):
        """Create the footer section with input and controls."""
        footer_frame = QFrame()
        footer_frame.setObjectName("footerFrame")
        footer_layout = QHBoxLayout(footer_frame)
        
        # Voice control button
        self.voice_button = AnimatedButton()
        self.voice_button.setIcon(QIcon.fromTheme("microphone"))
        self.voice_button.setToolTip("Toggle voice recognition")
        self.voice_button.setCheckable(True)
        self.voice_button.setChecked(self.voice_active)
        self.voice_button.clicked.connect(self._toggle_voice)
        
        # Input field
        self.input_field = TransparentLineEdit()
        self.input_field.setPlaceholderText("Type a message or command...")
        self.input_field.returnPressed.connect(self._send_message)
        
        # Send button
        self.send_button = AnimatedButton()
        self.send_button.setIcon(QIcon.fromTheme("send"))
        self.send_button.setToolTip("Send message")
        self.send_button.clicked.connect(self._send_message)
        
        # Fullscreen button
        self.fullscreen_button = AnimatedButton()
        self.fullscreen_button.setIcon(QIcon.fromTheme("view-fullscreen"))
        self.fullscreen_button.setToolTip("Toggle fullscreen")
        self.fullscreen_button.clicked.connect(self._toggle_fullscreen)
        
        # Add to layout
        footer_layout.addWidget(self.voice_button)
        footer_layout.addWidget(self.input_field)
        footer_layout.addWidget(self.send_button)
        footer_layout.addWidget(self.fullscreen_button)
        
        self.main_layout.addWidget(footer_frame)
    
    def _setup_timers(self):
        """Setup timers for regular updates."""
        # Timer for time/date updates
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self._update_time)
        self.time_timer.start(1000)  # Update every second
        
        # Timer for system status updates
        self.system_timer = QTimer(self)
        self.system_timer.timeout.connect(self._update_system_status)
        self.system_timer.start(2000)  # Update every 2 seconds
        
        # Timer for energy core animation
        self.energy_timer = QTimer(self)
        self.energy_timer.timeout.connect(self._update_energy_core)
        self.energy_timer.start(100)  # Update every 100ms
    
    def _create_system_tray(self):
        """Create the system tray icon and menu."""
        try:
            self.tray_icon = QSystemTrayIcon(self)
            
            # Try to use the logo
            logo_path = os.path.join(os.path.dirname(__file__), "assets", "jarvis_logo.svg")
            if os.path.exists(logo_path):
                self.tray_icon.setIcon(QIcon(logo_path))
            else:
                self.tray_icon.setIcon(QIcon.fromTheme("assistant"))
            
            # Create tray menu
            tray_menu = QMenu()
            
            show_action = QAction("Show J.A.R.V.I.S.", self)
            show_action.triggered.connect(self.show)
            
            hide_action = QAction("Hide J.A.R.V.I.S.", self)
            hide_action.triggered.connect(self.hide)
            
            toggle_voice_action = QAction("Toggle Voice Recognition", self)
            toggle_voice_action.triggered.connect(self._toggle_voice)
            
            exit_action = QAction("Exit", self)
            exit_action.triggered.connect(self._exit_application)
            
            tray_menu.addAction(show_action)
            tray_menu.addAction(hide_action)
            tray_menu.addSeparator()
            tray_menu.addAction(toggle_voice_action)
            tray_menu.addSeparator()
            tray_menu.addAction(exit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.setToolTip("J.A.R.V.I.S.")
            self.tray_icon.show()
            
            # Connect activation signal
            self.tray_icon.activated.connect(self._tray_icon_activated)
            
        except Exception as e:
            self.logger.error(f"Error creating system tray: {e}")
    
    def _setup_system_monitor(self):
        """Setup system monitoring."""
        try:
            from jarvis.core.system_monitor import SystemMonitor
            self.system_monitor = SystemMonitor()
            self.system_monitor.start_monitoring()
            
            from jarvis.core.energy_core import EnergyCore
            self.energy_core_monitor = EnergyCore()
            self.energy_core_monitor.start_monitoring()
            
        except Exception as e:
            self.logger.error(f"Error setting up system monitor: {e}")
            self.system_monitor = None
            self.energy_core_monitor = None
    
    def _start_voice_thread(self):
        """Start the voice recognition thread."""
        self.voice_thread = VoiceThread(self.voice_engine)
        self.voice_thread.text_captured.connect(self._process_voice_input)
        self.voice_thread.start()
    
    def _update_time(self):
        """Update the time and date display."""
        now = datetime.now()
        self.time_label.setText(now.strftime("%I:%M:%S %p"))
        self.date_label.setText(now.strftime("%A, %B %d, %Y"))
    
    def _update_system_status(self):
        """Update system status displays."""
        if self.system_monitor:
            try:
                # Get current usage
                usage = self.system_monitor.get_current_usage()
                
                # Update CPU display
                cpu_percent = usage.get("cpu_percent", 0)
                self.cpu_progress.setValue(cpu_percent)
                self.cpu_details.setText(f"{cpu_percent:.1f}%")
                
                # Update memory display
                memory_percent = usage.get("memory_percent", 0)
                self.memory_progress.setValue(memory_percent)
                memory_used = usage.get("memory_used", 0)
                memory_total = usage.get("memory_total", 1)
                memory_used_gb = memory_used / (1024**3)
                memory_total_gb = memory_total / (1024**3)
                self.memory_details.setText(f"{memory_percent:.1f}%\n{memory_used_gb:.1f}/{memory_total_gb:.1f} GB")
                
                # Update battery display if available
                if "battery_percent" in usage:
                    battery_percent = usage.get("battery_percent", 0)
                    self.battery_progress.setValue(battery_percent)
                    
                    battery_status = "Plugged In" if usage.get("battery_power_plugged", False) else "Discharging"
                    battery_time = ""
                    
                    if "battery_time_left" in usage and usage["battery_time_left"] and usage["battery_time_left"] > 0:
                        hours = usage["battery_time_left"] // 3600
                        minutes = (usage["battery_time_left"] % 3600) // 60
                        battery_time = f"\n{int(hours)}h {int(minutes)}m remaining"
                    
                    self.battery_details.setText(f"{battery_percent}%\n{battery_status}{battery_time}")
                else:
                    self.battery_progress.setValue(0)
                    self.battery_details.setText("No battery detected")
                
                # Update system details text
                if self.tab_widget.currentIndex() == 1:  # System tab
                    details = self.system_monitor.get_formatted_usage()
                    self.system_details.setText(details)
            
            except Exception as e:
                self.logger.error(f"Error updating system status: {e}")
        
        # Update Energy Core display
        if self.energy_core_monitor:
            try:
                status = self.energy_core_monitor.get_status()
                
                # Update Energy Core display
                power_level = status.get("power_level", 100)
                self.energy_core_display.setPowerLevel(power_level)
                
                # Update energy details
                if self.tab_widget.currentIndex() == 1:  # System tab
                    energy_text = (
                        f"Power Level: {power_level:.1f}%\n"
                        f"Temperature: {status.get('temperature', 0):.1f}°C\n"
                        f"Efficiency: {status.get('efficiency', 0):.1f}%\n"
                        f"Output: {status.get('output', 0):.2f} GW"
                    )
                    self.energy_details.setText(energy_text)
            
            except Exception as e:
                self.logger.error(f"Error updating energy core: {e}")
    
    def _update_energy_core(self):
        """Update Energy Core animations."""
        # Just pulse the animation
        self.energy_core.pulse()
        self.energy_core_display.pulse()
    
    def _toggle_voice(self):
        """Toggle voice recognition on/off."""
        self.voice_active = not self.voice_active
        self.voice_button.setChecked(self.voice_active)
        
        if self.voice_active:
            if hasattr(self, 'voice_thread') and self.voice_thread.isRunning():
                self.voice_thread.terminate()
            
            self._start_voice_thread()
            self.voice_waveform.setActive(True)
            self._add_to_chat("System", "Voice recognition activated")
        else:
            if hasattr(self, 'voice_thread') and self.voice_thread.isRunning():
                self.voice_thread.stop()
                self.voice_thread.terminate()
            
            self.voice_waveform.setActive(False)
            self._add_to_chat("System", "Voice recognition deactivated")
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.fullscreen:
            self.showNormal()
        else:
            self.showFullScreen()
        
        self.fullscreen = not self.fullscreen
    
    def _send_message(self):
        """Send the current input as a message to the AI."""
        message = self.input_field.text().strip()
        if not message:
            return
        
        # Clear input field
        self.input_field.clear()
        
        # Add to chat display
        self._add_to_chat("You", message)
        
        # Process with AI engine
        threading.Thread(target=self._process_message, args=(message,), daemon=True).start()
    
    def _process_message(self, message):
        """Process a message with the AI engine.
        
        Args:
            message: Message text to process
        """
        try:
            response = self.ai_engine.process_input(message)
            
            # TTS for the response
            if self.voice_engine and self.voice_active:
                self.voice_engine.speak(response)
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            response = f"I'm sorry, I encountered an error: {str(e)}"
            
            # Add to chat display
            self._add_to_chat("JARVIS", response)
    
    def _process_voice_input(self, text):
        """Process voice input.
        
        Args:
            text: Recognized voice text
        """
        if not text:
            return
        
        # Add to chat display
        self._add_to_chat("You (voice)", text)
        
        # Animate voice waveform
        self.voice_waveform.pulse()
        
        # Process with AI engine
        threading.Thread(target=self._process_message, args=(text,), daemon=True).start()
    
    def on_ai_response(self, response):
        """Callback for AI engine responses.
        
        Args:
            response: Response text from AI
        """
        self._add_to_chat("JARVIS", response)
    
    def _add_to_chat(self, sender, message):
        """Add a message to the chat display.
        
        Args:
            sender: Sender name
            message: Message text
        """
        # Format timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format message
        formatted_message = f"<b>[{timestamp}] {sender}:</b> {message}"
        
        # Add to chat display
        self.chat_display.append(formatted_message)
        
        # Scroll to bottom
        scrollbar = self.chat_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # Add to conversation history
        self.conversation_history.append({
            "sender": sender,
            "message": message,
            "timestamp": timestamp
        })
    
    def _tray_icon_activated(self, reason):
        """Handle tray icon activation.
        
        Args:
            reason: Activation reason
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.activateWindow()
    
    def _exit_application(self):
        """Exit the application."""
        # Stop threads
        if hasattr(self, 'voice_thread') and self.voice_thread.isRunning():
            self.voice_thread.stop()
            self.voice_thread.terminate()
        
        # Stop monitoring
        if hasattr(self, 'system_monitor') and self.system_monitor:
            self.system_monitor.stop_monitoring()
        
        if hasattr(self, 'energy_core_monitor') and self.energy_core_monitor:
            self.energy_core_monitor.stop_monitoring()
        
        # Exit application
        QApplication.quit()
    
    def closeEvent(self, event):
        """Handle window close event.
        
        Args:
            event: Close event
        """
        # Minimize to tray instead of closing
        event.ignore()
        self.hide()
        
        # Show notification
        if hasattr(self, 'tray_icon'):
            self.tray_icon.showMessage(
                "J.A.R.V.I.S.",
                "I'll continue running in the background. Double-click to restore.",
                QSystemTrayIcon.Information,
                2000
            )
    
    # Feature methods
    def _feature_weather(self):
        """Weather feature."""
        self.input_field.setText("What's the weather today?")
        self._send_message()
    
    def _feature_news(self):
        """News feature."""
        self.input_field.setText("Tell me the latest news")
        self._send_message()
    
    def _feature_web_search(self):
        """Web search feature."""
        self.input_field.setText("Search for ")
        self.input_field.setFocus()
        # Move cursor to end
        self.input_field.setCursorPosition(len(self.input_field.text()))
    
    def _feature_calendar(self):
        """Calendar feature."""
        self.input_field.setText("What's on my calendar today?")
        self._send_message()
    
    def _feature_media(self):
        """Media player feature."""
        self.input_field.setText("Play ")
        self.input_field.setFocus()
        # Move cursor to end
        self.input_field.setCursorPosition(len(self.input_field.text()))
    
    def _feature_email(self):
        """Email feature."""
        self.input_field.setText("Check my emails")
        self._send_message()
    
    def _feature_notes(self):
        """Notes feature."""
        self.input_field.setText("Take a note: ")
        self.input_field.setFocus()
        # Move cursor to end
        self.input_field.setCursorPosition(len(self.input_field.text()))
    
    def _feature_calculator(self):
        """Calculator feature."""
        self.input_field.setText("Calculate ")
        self.input_field.setFocus()
        # Move cursor to end
        self.input_field.setCursorPosition(len(self.input_field.text()))
    
    def _feature_wikipedia(self):
        """Wikipedia feature."""
        self.input_field.setText("Tell me about ")
        self.input_field.setFocus()
        # Move cursor to end
        self.input_field.setCursorPosition(len(self.input_field.text()))
    
    def _feature_system_info(self):
        """System info feature."""
        self.input_field.setText("Show system status")
        self._send_message()
    
    def _feature_jokes(self):
        """Jokes feature."""
        self.input_field.setText("Tell me a joke")
        self._send_message()
    
    def _feature_settings(self):
        """Settings feature."""
        self.tab_widget.setCurrentIndex(1)  # Switch to System tab
        self._add_to_chat("System", "Settings opened in System tab")
    
    def exec_(self):
        """Execute the application."""
        return QApplication.exec_()
