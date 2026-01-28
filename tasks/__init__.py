"""
Maintenance Tasks

Various maintenance tasks (incremental update, full sync, validation, repair).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class MaintenanceTask(ABC):
    """
    Abstract base class for maintenance tasks
    
    All maintenance tasks must inherit this class and implement
    the abstract methods.
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize maintenance task
        
        Args:
            name: Task name
            config: Task-specific configuration
        """
        self.name = name
        self.config = config or {}
        self._status = "idle"  # idle, running, completed, failed
        self._last_run_time: Optional[datetime] = None
        self._last_result: Optional[Dict[str, Any]] = None
    
    @property
    def status(self) -> str:
        """Current task status"""
        return self._status
    
    @property
    def last_run_time(self) -> Optional[datetime]:
        """Last run time"""
        return self._last_run_time
    
    @property
    def last_result(self) -> Optional[Dict[str, Any]]:
        """Last execution result"""
        return self._last_result
    
    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """
        Execute the task
        
        Returns:
            Dict with execution results:
            {
                "success": bool,
                "message": str,
                "data_count": int,  # Optional: number of records processed
                "duration": float,  # Optional: execution time in seconds
                "error": str,  # Optional: error message if failed
            }
        """
        pass
    
    def run(self) -> Dict[str, Any]:
        """
        Run the task (wrapper with status tracking)
        
        Returns:
            Execution result
        """
        import time
        
        self._status = "running"
        start_time = time.time()
        
        try:
            result = self.execute()
            duration = time.time() - start_time
            
            # Add duration to result
            if isinstance(result, dict):
                result["duration"] = duration
            else:
                result = {
                    "success": True,
                    "message": "Task completed",
                    "duration": duration,
                }
            
            self._status = "completed" if result.get("success", True) else "failed"
            self._last_run_time = datetime.now()
            self._last_result = result
            
            return result
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Task {self.name} failed: {e}", exc_info=True)
            
            duration = time.time() - start_time
            result = {
                "success": False,
                "message": f"Task failed: {str(e)}",
                "error": str(e),
                "duration": duration,
            }
            
            self._status = "failed"
            self._last_run_time = datetime.now()
            self._last_result = result
            
            return result
