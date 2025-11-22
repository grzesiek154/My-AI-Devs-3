from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class ContentDescription:
    """
    Represents a description of content (image, audio, text) with caching information.
    
    Attributes:
        file_path: Path to the original file
        content_type: Type of content (image, audio, text)
        description: LLM-generated description of the content
        created_at: When the description was generated
        last_used: When the description was last used
        use_count: How many times this description has been used
    """
    file_path: str
    content_type: str
    description: str
    created_at: datetime
    last_used: datetime
    use_count: int = 0

    def to_dict(self) -> dict:
        """Convert the description to a dictionary for storage."""
        return {
            'file_path': self.file_path,
            'content_type': self.content_type,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'last_used': self.last_used.isoformat(),
            'use_count': self.use_count
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ContentDescription':
        """Create a ContentDescription from a dictionary."""
        return cls(
            file_path=data['file_path'],
            content_type=data['content_type'],
            description=data['description'],
            created_at=datetime.fromisoformat(data['created_at']),
            last_used=datetime.fromisoformat(data['last_used']),
            use_count=data['use_count']
        ) 