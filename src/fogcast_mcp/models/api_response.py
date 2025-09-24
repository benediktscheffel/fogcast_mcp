"""
API response models for consistent data handling.
"""

from dataclasses import dataclass
from typing import Any, Optional, List, Dict


@dataclass
class APIResponse:
    """Standard API response wrapper."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        response = {
            'success': self.success,
            'message': self.message
        }
        
        if self.data is not None:
            response['data'] = self.data
            
        if self.error is not None:
            response['error'] = self.error
            
        return response
    
    @classmethod
    def success_response(cls, data: Any = None, message: str = "Operation successful") -> 'APIResponse':
        """Create a successful response."""
        return cls(success=True, data=data, message=message)
    
    @classmethod
    def error_response(cls, error: str, message: str = "Operation failed") -> 'APIResponse':
        """Create an error response."""
        return cls(success=False, error=error, message=message)
