"""
System Monitor - Monitors system resources and provides status information.
"""

import os
import platform
import logging
import time
import threading
from datetime import datetime

# Try importing system monitoring libraries
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    import GPUtil
    GPUTIL_AVAILABLE = True
except ImportError:
    GPUTIL_AVAILABLE = False

class SystemMonitor:
    """Monitors and reports on system resources and status."""
    
    def __init__(self, config=None):
        """Initialize the System Monitor.
        
        Args:
            config: Optional configuration object
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        
        # Check for monitoring libraries
        if not PSUTIL_AVAILABLE:
            self.logger.warning("psutil library not available. Install it for full system monitoring.")
        
        # System info
        self.system_info = self._get_system_info()
        
        # Resource usage history
        self.cpu_history = []
        self.memory_history = []
        self.disk_history = []
        self.network_history = []
        
        # Maximum history points to keep
        self.max_history = 60
        
        # Whether continuous monitoring is active
        self.monitoring = False
        self.monitor_thread = None
        self.monitor_interval = 5  # seconds
        
        self.logger.info("System Monitor initialized")
    
    def _get_system_info(self):
        """Get basic system information.
        
        Returns:
            Dictionary with system information
        """
        info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        }
        
        if PSUTIL_AVAILABLE:
            info["cpu_count_physical"] = psutil.cpu_count(logical=False)
            info["cpu_count_logical"] = psutil.cpu_count(logical=True)
            
            try:
                info["cpu_freq"] = psutil.cpu_freq().max
            except Exception:
                info["cpu_freq"] = "Unknown"
                
            mem = psutil.virtual_memory()
            info["total_memory"] = mem.total
            
            disk = psutil.disk_usage('/')
            info["total_disk"] = disk.total
        
        return info
    
    def get_system_info(self):
        """Get a formatted string with system information.
        
        Returns:
            String with system info
        """
        if not self.system_info:
            return "System information not available."
        
        info = self.system_info
        
        result = (
            f"System: {info['platform']} {info['platform_release']} ({info['architecture']})\n"
            f"Hostname: {info['hostname']}\n"
            f"Processor: {info['processor']}\n"
        )
        
        if PSUTIL_AVAILABLE:
            result += (
                f"CPU Cores: {info['cpu_count_physical']} physical, {info['cpu_count_logical']} logical\n"
                f"CPU Frequency: {info.get('cpu_freq', 'Unknown')} MHz\n"
                f"Total Memory: {self._format_bytes(info['total_memory'])}\n"
                f"Total Disk: {self._format_bytes(info['total_disk'])}\n"
            )
        
        return result
    
    def get_current_usage(self):
        """Get current system resource usage.
        
        Returns:
            Dictionary with current usage statistics
        """
        if not PSUTIL_AVAILABLE:
            return {"error": "psutil library not available"}
        
        usage = {}
        
        # CPU usage
        usage["cpu_percent"] = psutil.cpu_percent(interval=0.1)
        usage["cpu_per_core"] = psutil.cpu_percent(interval=0.1, percpu=True)
        
        # Memory usage
        mem = psutil.virtual_memory()
        usage["memory_total"] = mem.total
        usage["memory_available"] = mem.available
        usage["memory_percent"] = mem.percent
        usage["memory_used"] = mem.used
        
        # Disk usage
        disk = psutil.disk_usage('/')
        usage["disk_total"] = disk.total
        usage["disk_used"] = disk.used
        usage["disk_free"] = disk.free
        usage["disk_percent"] = disk.percent
        
        # Network usage
        net_io = psutil.net_io_counters()
        usage["net_bytes_sent"] = net_io.bytes_sent
        usage["net_bytes_recv"] = net_io.bytes_recv
        
        # Battery info (if available)
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()
            if battery:
                usage["battery_percent"] = battery.percent
                usage["battery_power_plugged"] = battery.power_plugged
                usage["battery_time_left"] = battery.secsleft if battery.secsleft != -1 else None
        
        # GPU info (if available)
        if GPUTIL_AVAILABLE:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]  # Get the first GPU
                    usage["gpu_name"] = gpu.name
                    usage["gpu_load"] = gpu.load * 100
                    usage["gpu_memory_total"] = gpu.memoryTotal
                    usage["gpu_memory_used"] = gpu.memoryUsed
                    usage["gpu_temperature"] = gpu.temperature
            except Exception as e:
                self.logger.error(f"Error getting GPU info: {e}")
        
        # Update history
        self._update_history(usage)
        
        return usage
    
    def _update_history(self, usage):
        """Update resource usage history.
        
        Args:
            usage: Current usage dictionary
        """
        timestamp = datetime.now()
        
        # CPU history
        self.cpu_history.append((timestamp, usage["cpu_percent"]))
        if len(self.cpu_history) > self.max_history:
            self.cpu_history.pop(0)
        
        # Memory history
        self.memory_history.append((timestamp, usage["memory_percent"]))
        if len(self.memory_history) > self.max_history:
            self.memory_history.pop(0)
        
        # Disk history
        self.disk_history.append((timestamp, usage["disk_percent"]))
        if len(self.disk_history) > self.max_history:
            self.disk_history.pop(0)
        
        # Network history
        if len(self.network_history) > 0:
            last_bytes_sent = self.network_history[-1][1]
            last_bytes_recv = self.network_history[-1][2]
            bytes_sent_rate = (usage["net_bytes_sent"] - last_bytes_sent) / self.monitor_interval
            bytes_recv_rate = (usage["net_bytes_recv"] - last_bytes_recv) / self.monitor_interval
        else:
            bytes_sent_rate = 0
            bytes_recv_rate = 0
        
        self.network_history.append((timestamp, usage["net_bytes_sent"], usage["net_bytes_recv"], bytes_sent_rate, bytes_recv_rate))
        if len(self.network_history) > self.max_history:
            self.network_history.pop(0)
    
    def get_formatted_usage(self):
        """Get a formatted string with current resource usage.
        
        Returns:
            String with formatted usage information
        """
        usage = self.get_current_usage()
        
        if "error" in usage:
            return usage["error"]
        
        result = "System Status:\n"
        
        # CPU
        result += f"CPU Usage: {usage['cpu_percent']}%\n"
        
        # Memory
        result += (
            f"Memory: {self._format_bytes(usage['memory_used'])} / "
            f"{self._format_bytes(usage['memory_total'])} "
            f"({usage['memory_percent']}%)\n"
        )
        
        # Disk
        result += (
            f"Disk: {self._format_bytes(usage['disk_used'])} / "
            f"{self._format_bytes(usage['disk_total'])} "
            f"({usage['disk_percent']}%)\n"
        )
        
        # Network
        if len(self.network_history) > 1:
            result += (
                f"Network: ↑ {self._format_bytes(self.network_history[-1][3])}/s, "
                f"↓ {self._format_bytes(self.network_history[-1][4])}/s\n"
            )
        
        # Battery
        if "battery_percent" in usage:
            result += f"Battery: {usage['battery_percent']}%"
            if usage["battery_power_plugged"]:
                result += " (Plugged in)"
            elif usage["battery_time_left"]:
                hours, remainder = divmod(usage["battery_time_left"], 3600)
                minutes, seconds = divmod(remainder, 60)
                result += f" ({int(hours)}h {int(minutes)}m remaining)"
            result += "\n"
        
        # GPU
        if "gpu_name" in usage:
            result += (
                f"GPU: {usage['gpu_name']}, Load: {usage['gpu_load']:.1f}%, "
                f"Memory: {usage['gpu_memory_used']}/{usage['gpu_memory_total']} MB, "
                f"Temperature: {usage['gpu_temperature']}°C\n"
            )
        
        return result
    
    def _format_bytes(self, bytes_value):
        """Format bytes value to human-readable string.
        
        Args:
            bytes_value: Bytes value to format
            
        Returns:
            Formatted string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024 or unit == 'TB':
                if unit == 'B':
                    return f"{bytes_value} {unit}"
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024
    
    def start_monitoring(self):
        """Start continuous monitoring of system resources."""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Continuous system monitoring started")
    
    def stop_monitoring(self):
        """Stop continuous monitoring of system resources."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
            self.monitor_thread = None
        self.logger.info("System monitoring stopped")
    
    def _monitor_loop(self):
        """Background thread for continuous resource monitoring."""
        while self.monitoring:
            try:
                self.get_current_usage()
            except Exception as e:
                self.logger.error(f"Error in system monitoring: {e}")
            
            time.sleep(self.monitor_interval)
