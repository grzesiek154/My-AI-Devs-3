import os
import aiohttp
import zipfile
import io
import asyncio
from typing import Dict, List, Optional
from pathlib import Path
from .ai_service import AIService
from .cache_service import CacheService
from utils.constants import SUPPORTED_EXTENSIONS, ERROR_MESSAGES

class FileService:
    def __init__(self, ai_service: AIService, cache_service: CacheService):
        self.ai_service = ai_service
        self.cache_service = cache_service
        self.supported_extensions = set(SUPPORTED_EXTENSIONS.keys())

    async def process_directory(self, directory: str) -> Dict[str, List[str]]:
        """
        Processes all files in directory and categorizes them.
        Returns dictionary with categorized filenames.
        """ 
        result = {
            "people": [],
            "hardware": []
        }

        try:
            # Collect all files to process
            files_to_process = []
            for root, _, files in os.walk(directory):
                # Skip "facts" directory
                if "facts" in root:
                    continue

                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[1].lower()

                    if file_ext not in self.supported_extensions:
                        continue

                    files_to_process.append((file_path, file))

            # Process files concurrently
            tasks = [self.process_file(file_path) for file_path, _ in files_to_process]
            categorizations = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            for (file_path, file), categorization in zip(files_to_process, categorizations):
                if isinstance(categorization, Exception):
                    print(f"Error processing {file}: {str(categorization)}")
                    continue

                # Add to appropriate category
                if categorization["has_people"]:
                    result["people"].append(file)
                if categorization["has_hardware"]:
                    result["hardware"].append(file)
            
            # Sort filenames alphabetically
            result["people"].sort()
            result["hardware"].sort()

            return result

        except Exception as e:
            print(f"Error processing directory: {str(e)}")
            return result     

    async def process_file(self, file_path: str) -> Dict[str, bool]:
        """
        Processes individual file and returns categorization.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Dictionary containing categorization results
        """
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            content_type = SUPPORTED_EXTENSIONS.get(file_ext)
            
            if not content_type:
                raise ValueError(ERROR_MESSAGES['invalid_file_type'])

            # Read file content
            with open(file_path, 'rb') as f:
                content = f.read()

            # Analyze content using AI service
            return await self.ai_service.analyze_content(content, content_type, file_path)

        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return {"has_people": False, "has_hardware": False} 