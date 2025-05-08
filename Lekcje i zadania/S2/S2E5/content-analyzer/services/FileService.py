import os
import json
import logging
import asyncio
from typing import Optional, Union, Dict, Any, List
from pathlib import Path
from datetime import datetime
import aiofiles
from models.ContentMetadata import ContentMetadata
from bs4 import BeautifulSoup
from PIL import Image
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileServiceError(Exception):
    """Base exception for FileService errors"""
    pass

class FileService:
    def __init__(self, base_path: str = "data", cache_path: str = "cache", temp_path: str = "temp"):
        """
        Initialize the FileService with base paths.
        
        :param base_path: Base directory for content storage
        :param cache_path: Directory for cached content
        :param temp_path: Directory for temporary files
        """
        self.base_path = Path(base_path)
        self.cache_path = Path(cache_path)
        self.temp_path = Path(temp_path)
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure all required directories exist"""
        for path in [self.base_path, self.cache_path, self.temp_path]:
            try:
                path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise FileServiceError(f"Failed to create directory {path}: {str(e)}")

    async def resize_image(self, image_path: str, max_dimension: int = 1024, quality: int = 85) -> bytes:
        """
        Resize an image if it exceeds maximum dimension.
        
        :param image_path: Path to the image file
        :param max_dimension: Maximum dimension (width or height)
        :param quality: JPEG quality (1-100)
        :return: Resized image data
        """
        try:
            # Read image
            image_data = await self.read_binary(image_path)
            
            # Open image
            img = Image.open(io.BytesIO(image_data))
            
            # Check if resizing is needed
            if max(img.size) <= max_dimension:
                return image_data
            
            # Calculate new dimensions
            ratio = max_dimension / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            
            # Resize image
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert back to bytes
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error resizing image: {str(e)}")
            raise FileServiceError(f"Failed to resize image: {str(e)}")

    async def save_resized_image(self, image_path: str, max_dimension: int = 1024, quality: int = 85) -> str:
        """
        Save a resized version of an image.
        
        :param image_path: Path to the original image
        :param max_dimension: Maximum dimension (width or height)
        :param quality: JPEG quality (1-100)
        :return: Path to the resized image
        """
        try:
            # Create resized image path
            original_path = Path(image_path)
            resized_path = original_path.parent / f"{original_path.stem}_resized{original_path.suffix}"
            
            # Resize image
            resized_data = await self.resize_image(image_path, max_dimension, quality)
            
            # Save resized image
            await self.save_binary(resized_data, str(resized_path))
            
            return str(resized_path)
            
        except Exception as e:
            logger.error(f"Error saving resized image: {str(e)}")
            raise FileServiceError(f"Failed to save resized image: {str(e)}")

    async def save_content(self, content: Union[str, bytes], file_path: str, metadata: ContentMetadata) -> bool:
        """
        Save content with metadata.
        
        :param content: Content to save (text or binary)
        :param file_path: Path to save the file (including extension)
        :param metadata: Content metadata
        :return: True if successful
        """
        try:
            # Save content
            if isinstance(content, str):
                # Handle markdown content
                if file_path.endswith('.md'):
                    # Add markdown-specific metadata
                    metadata.context.update({
                        "format": "markdown",
                        "content_type": "markdown"
                    })
                await self._save_text(content, file_path)
            else:
                await self._save_binary(content, file_path)
            
            # Save metadata
            metadata_path = self._get_metadata_path(file_path)
            await self._save_metadata(metadata, metadata_path)
            
            return True
        except Exception as e:
            raise FileServiceError(f"Failed to save content: {str(e)}")

    async def _save_text(self, content: str, file_path: str):
        """
        Save text content to specified file path.
        
        :param content: Text content to save
        :param file_path: Path to save the file (including extension)
        """
        # Ensure we're using the correct path
        full_path = self.base_path / file_path
        # Create parent directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        # Save the content to the specified file
        async with aiofiles.open(full_path, 'w', encoding='utf-8') as f:
            await f.write(content)

    async def _save_binary(self, content: bytes, file_path: str):
        """Save binary content"""
        full_path = self.base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(full_path, 'wb') as f:
            await f.write(content)

    async def _save_metadata(self, metadata: ContentMetadata, metadata_path: str):
        """Save metadata"""
        full_path = self.base_path / metadata_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(full_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(metadata.to_dict(), indent=2))

    def _get_metadata_path(self, file_path: str) -> str:
        """
        Get metadata file path for a content file.
        Ensures metadata file is in the same directory as content file, relative to base_path.
        
        :param file_path: Path to the content file
        :return: Path to metadata file
        """
        # Convert to Path object to handle path operations
        path = Path(file_path)
        # Get the directory and filename without extension
        directory = path.parent
        filename = path.stem
        # Create metadata path in the same directory, relative to base_path
        return str(directory / f"{filename}.json")

    async def get_content_with_metadata(self, file_path: str) -> tuple[Union[str, bytes], ContentMetadata]:
        """
        Get content with its metadata.
        
        :param file_path: Path to the content file
        :return: Tuple of (content, metadata)
        """
        try:
            # Read content
            content = await self._read_content(file_path)
            
            # Read metadata
            metadata_path = self._get_metadata_path(file_path)
            metadata = await self._read_metadata(metadata_path)
            
            return content, metadata
        except Exception as e:
            raise FileServiceError(f"Failed to get content with metadata: {str(e)}")

    async def _read_content(self, file_path: str) -> Union[str, bytes]:
        """Read content file"""
        full_path = self.base_path / file_path
        if full_path.suffix in ['.txt', '.md']:
            async with aiofiles.open(full_path, 'r', encoding='utf-8') as f:
                return await f.read()
        else:
            async with aiofiles.open(full_path, 'rb') as f:
                return await f.read()

    async def _read_metadata(self, metadata_path: str) -> ContentMetadata:
        """Read metadata file"""
        full_path = self.base_path / metadata_path
        async with aiofiles.open(full_path, 'r', encoding='utf-8') as f:
            data = json.loads(await f.read())
            return ContentMetadata.from_dict(data)

    async def cache_media_analysis(self, analysis_result: Dict[str, Any], media_path: str) -> bool:
        """
        Cache media analysis results.
        
        :param analysis_result: Analysis results to cache
        :param media_path: Path to the media file
        :return: True if successful
        """
        cache_path = self.cache_path / f"{Path(media_path).stem}_analysis.json"
        try:
            async with aiofiles.open(cache_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(analysis_result, indent=2))
            return True
        except Exception as e:
            raise FileServiceError(f"Failed to cache media analysis: {str(e)}")

    async def get_cached_analysis(self, media_path: str) -> Optional[Dict[str, Any]]:
        """
        Get cached media analysis results.
        
        :param media_path: Path to the media file
        :return: Cached analysis results or None
        """
        cache_path = self.cache_path / f"{Path(media_path).stem}_analysis.json"
        try:
            async with aiofiles.open(cache_path, 'r', encoding='utf-8') as f:
                return json.loads(await f.read())
        except FileNotFoundError:
            return None
        except Exception as e:
            raise FileServiceError(f"Failed to get cached analysis: {str(e)}")

    def get_temp_file(self, prefix: str = "temp", suffix: str = "") -> Path:
        """
        Get a path for a temporary file.
        
        :param prefix: File prefix
        :param suffix: File suffix
        :return: Path to temporary file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.temp_path / f"{prefix}_{timestamp}{suffix}"

    def _html_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML content to markdown.
        
        :param html_content: HTML content to convert
        :return: Markdown content
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Convert headings
            for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                level = int(h.name[1])
                h.replace_with(f"{'#' * level} {h.get_text()}\n\n")
            
            # Convert paragraphs
            for p in soup.find_all('p'):
                p.replace_with(f"{p.get_text()}\n\n")
            
            # Convert lists
            for ul in soup.find_all('ul'):
                items = []
                for li in ul.find_all('li'):
                    items.append(f"- {li.get_text()}")
                ul.replace_with('\n'.join(items) + '\n\n')
            
            # Convert links
            for a in soup.find_all('a'):
                href = a.get('href', '')
                a.replace_with(f"[{a.get_text()}]({href})")
            
            # Convert bold and italic
            for strong in soup.find_all(['strong', 'b']):
                strong.replace_with(f"**{strong.get_text()}**")
            for em in soup.find_all(['em', 'i']):
                em.replace_with(f"*{em.get_text()}*")
            
            # Get the final text and clean it up
            text = str(soup)  # Convert BeautifulSoup object to string
            # Remove any remaining HTML tags
            text = BeautifulSoup(text, 'html.parser').get_text()
            # Remove extra whitespace
            text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
            # Ensure proper spacing between sections
            text = '\n\n'.join(para for para in text.split('\n\n') if para.strip())
            
            return text
        except Exception as e:
            logger.error(f"Error in _html_to_markdown: {str(e)}")
            raise FileServiceError(f"Failed to convert HTML to markdown: {str(e)}")

    async def save_to_markdown(self, content: str, file_path: str, metadata: ContentMetadata) -> bool:
        """
        Save content as Markdown with metadata.
        
        :param content: Content to save (can be HTML or plain text)
        :param file_path: Path to save the file
        :param metadata: Content metadata
        :return: True if successful
        """
        try:
            # Ensure markdown extension
            if not file_path.endswith('.md'):
                file_path += '.md'
            
            # Check if content is HTML
            if '<' in content and '>' in content:
                # Convert HTML to markdown
                markdown_content = self._html_to_markdown(content)
            else:
                markdown_content = content
            
            # Ensure we have a string
            if not isinstance(markdown_content, str):
                markdown_content = str(markdown_content)
            
            # Save content
            await self._save_text(markdown_content, file_path)
            
            # Save metadata
            metadata_path = self._get_metadata_path(file_path)
            await self._save_metadata(metadata, metadata_path)
            
            return True
        except Exception as e:
            logger.error(f"Error in save_to_markdown: {str(e)}")
            raise FileServiceError(f"Failed to save markdown content: {str(e)}") 