from typing import Dict, Any, List
from datetime import datetime

class ContentMetadata:
    def __init__(self, content_type: str, source_url: str, timestamp: str = None, context: Dict[str, Any] = None):
        self.content_type = content_type
        self.source_url = source_url
        self.timestamp = timestamp or datetime.now().isoformat()
        self.context = context or {}
        self.related_files: List[str] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_type": self.content_type,
            "source_url": self.source_url,
            "timestamp": self.timestamp,
            "context": self.context,
            "related_files": self.related_files
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContentMetadata':
        return cls(
            content_type=data["content_type"],
            source_url=data["source_url"],
            timestamp=data["timestamp"],
            context=data["context"]
        )
