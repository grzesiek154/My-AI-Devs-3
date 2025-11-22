import os
import aiohttp
import zipfile
import io
from typing import Dict, List, Optional
from pathlib import Path
from .ai_service import AIService
from ..utils.constants import SUPPORTED_EXTENSIONS, ERROR_MESSAGES

class FileService:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        # Convert dictionary keys to set for faster lookups
        # SUPPORTED_EXTENSIONS is a dict like {'.txt': 'text', '.png': 'image', '.mp3': 'audio'}
        # .keys() gets just the extensions: dict_keys(['.txt', '.png', '.mp3'])
        # set() converts to: {'.txt', '.png', '.mp3'}
        # This makes checking if a file extension is supported faster
        self.supported_extensions = set(SUPPORTED_EXTENSIONS.keys())

    async def download_and_extract(self, url: str, extract_path: str) -> Optional[str]:
        """
        Downloads ZIP file from URL and extracts it to specified path.
        Returns path to extracted directory or None if failed.
        """
        try:
            # Create extract directory if it doesn't exist
            os.makedirs(extract_path, exist_ok=True)

            # Download ZIP file
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        print(f"Failed to download ZIP file: {response.status}")
                        return None
                    zip_content = await response.read()

            # Extract ZIP file
            with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_ref:
                zip_ref.extractall(extract_path)

            return extract_path

        except Exception as e:
            print(f"Error downloading/extracting ZIP: {str(e)}")
            return None

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
            # Walk through directory
            for root, _, files in os.walk(directory):
                # Skip "facts" directory
                if "facts" in root:
                    continue

                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[1].lower()

                    # Skip unsupported file types
                    if file_ext not in self.supported_extensions:
                        continue

                    # Process file
                    categorization = await self.process_file(file_path)
                    
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
            return await self.ai_service.analyze_content(content, content_type)

        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return {"has_people": False, "has_hardware": False}