import json
import os
from typing import Optional, Dict, List
from datetime import datetime
from pathlib import Path
from ..models.content_description import ContentDescription

class CacheService:
    def __init__(self, cache_dir: str = "cache"):
        """
        Initialize the cache service.
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "descriptions.json"
        self._load_cache()

    def _load_cache(self) -> None:
        """Load the cache from disk."""
        if self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.cache = {item['file_path']: ContentDescription.from_dict(item) 
                            for item in data}
        else:
            self.cache = {}

    def _save_cache(self) -> None:
        """Save the cache to disk."""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump([desc.to_dict() for desc in self.cache.values()], 
                     f, ensure_ascii=False, indent=2)

    def get_description(self, file_path: str) -> Optional[ContentDescription]:
        """
        Get a cached description for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            ContentDescription if found, None otherwise
        """
        if file_path in self.cache:
            desc = self.cache[file_path]
            desc.last_used = datetime.now()
            desc.use_count += 1
            self._save_cache()
            return desc
        return None

    def save_description(self, description: ContentDescription) -> None:
        """
        Save a description to the cache.
        
        Args:
            description: ContentDescription to save
        """
        self.cache[description.file_path] = description
        self._save_cache()

    def get_all_descriptions(self) -> List[ContentDescription]:
        """
        Get all cached descriptions.
        
        Returns:
            List of all ContentDescriptions
        """
        return list(self.cache.values())

    def clear_cache(self) -> None:
        """Clear the entire cache."""
        self.cache.clear()
        self._save_cache()

    def remove_description(self, file_path: str) -> None:
        """
        Remove a description from the cache.
        
        Args:
            file_path: Path to the file to remove
        """
        if file_path in self.cache:
            del self.cache[file_path]
            self._save_cache() 