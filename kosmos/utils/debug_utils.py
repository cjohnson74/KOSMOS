"""
Debug utilities for KOSMOS agents
Provides consistent debugging and logging functionality across all agents
"""

import os
import time
from typing import Any, Dict, List, Optional
from datetime import datetime


class DebugLogger:
    """Centralized debug logging for KOSMOS agents"""
    
    def __init__(self, agent_name: str, debug_level: str = "INFO"):
        self.agent_name = agent_name
        self.debug_level = debug_level
        self.start_time = time.time()
        
        # Debug levels: DEBUG, INFO, WARNING, ERROR
        self.levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
        
    def _should_log(self, level: str) -> bool:
        """Check if message should be logged based on debug level"""
        return self.levels.get(level, 1) >= self.levels.get(self.debug_level, 1)
    
    def _format_message(self, level: str, message: str, **kwargs) -> str:
        """Format debug message with timestamp and agent info"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        elapsed = f"{time.time() - self.start_time:.3f}s"
        
        # Color codes for different levels
        colors = {
            "DEBUG": "\033[36m",    # Cyan
            "INFO": "\033[32m",     # Green  
            "WARNING": "\033[33m",  # Yellow
            "ERROR": "\033[31m",    # Red
        }
        reset = "\033[0m"
        
        color = colors.get(level, "")
        formatted = f"{color}🔍 {level}: {self.agent_name} [{timestamp}|{elapsed}] {message}{reset}"
        
        # Add any additional context
        if kwargs:
            context = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
            formatted += f" ({context})"
            
        return formatted
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        if self._should_log("DEBUG"):
            print(self._format_message("DEBUG", message, **kwargs))
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        if self._should_log("INFO"):
            print(self._format_message("INFO", message, **kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        if self._should_log("WARNING"):
            print(self._format_message("WARNING", message, **kwargs))
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        if self._should_log("ERROR"):
            print(self._format_message("ERROR", message, **kwargs))


def create_debug_logger(agent_name: str, debug_level: str = None) -> DebugLogger:
    """Create a debug logger for an agent"""
    if debug_level is None:
        debug_level = os.getenv("KOSMOS_DEBUG_LEVEL", "INFO")
    return DebugLogger(agent_name, debug_level)