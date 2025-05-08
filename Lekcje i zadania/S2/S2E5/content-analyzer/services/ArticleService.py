import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from models.ContentMetadata import ContentMetadata
from services.AIService import AIService
from services.FileService import FileService
from services.HttpService import HttpService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArticleService:
    def __init__(self, ai_service: AIService, file_service: FileService, http_service: HttpService):
        """
        Initialize the ArticleService with required services.
        
        :param ai_service: AIService instance for content analysis
        :param file_service: FileService instance for file operations
        :param http_service: HttpService instance for fetching content
        """
        self.ai_service = ai_service
        self.file_service = file_service
        self.http_service = http_service

    async def process_article(self, url: str) -> Dict[str, Any]:
        """
        Process an article from a URL, creating a comprehensive markdown description.
        
        :param url: URL of the article to process
        :return: Dictionary containing processing results
        """
        try:
            # Fetch content from URL
            content = await self.http_service.get_text(url)
            
            # Create metadata
            metadata = ContentMetadata(
                url=url,
                content_type="article",
                timestamp=datetime.now().isoformat(),
                source="web"
            )
            
            # Save raw content
            await self.file_service.save_content(content, "article.txt", metadata)
            
            # Process text content
            text_analysis = await self.ai_service.process_text(content)
            
            # Process any images in the content
            image_analyses = []
            for img_url in self._extract_image_urls(content):
                try:
                    # Download and resize image
                    img_data = await self.http_service.get_binary(img_url)
                    img_path = await self.file_service.save_binary(img_data, f"images/{Path(img_url).name}")
                    resized_path = await self.file_service.save_resized_image(img_path)
                    
                    # Analyze image
                    img_analysis = await self.ai_service.process_image(resized_path, text_analysis)
                    image_analyses.append(img_analysis)
                    
                except Exception as e:
                    logger.error(f"Error processing image {img_url}: {str(e)}")
            
            # Create unified analysis
            unified_analysis = await self.ai_service.create_unified_analysis(
                text_analysis=text_analysis,
                image_analyses=image_analyses
            )
            
            # Save markdown description
            await self.file_service.save_to_markdown(
                unified_analysis,
                "article.md",
                metadata
            )
            
            return {
                "status": "success",
                "text_analysis": text_analysis,
                "image_analyses": image_analyses,
                "unified_analysis": unified_analysis
            }
            
        except Exception as e:
            logger.error(f"Error processing article: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def _extract_image_urls(self, content: str) -> List[str]:
        """
        Extract image URLs from content.
        
        :param content: Content to extract URLs from
        :return: List of image URLs
        """
        try:
            soup = BeautifulSoup(content, 'html.parser')
            return [img['src'] for img in soup.find_all('img') if img.get('src')]
        except Exception as e:
            logger.error(f"Error extracting image URLs: {str(e)}")
            return []

    def _update_context(self, content_type: str, content: any):
        """
        Update the context stack with new content.
        
        :param content_type: Type of content (text, image, audio, etc.)
        :param content: The content to add to context
        """
        self.context_stack.append({
            'type': content_type,
            'content': content
        })

    def get_context(self) -> List[Dict]:
        """
        Get the current context stack.
        
        :return: List of context items
        """
        return self.context_stack 