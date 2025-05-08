import logging
import json
import base64
from typing import Dict, Any, Optional, Tuple
from openai import AsyncOpenAI
from pathlib import Path
from PIL import Image
import io
from services.FileService import FileService
from services.ArticleService import ArticleService
from models.ContentMetadata import ContentMetadata

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, file_service: FileService, article_service: ArticleService):
        """
        Initialize the AIService.
        
        :param file_service: FileService instance for file operations
        :param article_service: ArticleService instance for article processing
        """
        self.client = AsyncOpenAI()
        self.file_service = file_service
        self.article_service = article_service
        
        # Define models for different content types
        self.models = {
            'image': 'gpt-4-vision-preview',
            'text': 'gpt-4-turbo-preview',
            'audio': 'whisper-1'
        }
        
        # Token limits for different content types
        self.token_limits = {
            'image': 4096,  # GPT-4 Vision token limit
            'text': 128000,  # GPT-4 Turbo token limit
            'audio': 25 * 1024 * 1024  # Whisper file size limit (25MB)
        }

    async def analyze_article(self, article_url: str) -> str:
        """
        Analyze the entire article, including text, images, and audio.
        
        :param article_url: URL of the article to analyze
        :return: Path to the analyzed markdown file
        """
        try:
            logger.info(f"Starting analysis of article: {article_url}")
            
            # Process the article to get the markdown file
            markdown_path = await self.article_service.process_article(article_url)
            logger.info(f"Article processed and saved to: {markdown_path}")
            
            # Read the markdown content
            content, metadata = await self.file_service.get_content_with_metadata(markdown_path)
            logger.info(f"Read markdown content, length: {len(content)}")
            
            # Analyze the content using GPT-4
            analysis = await self._analyze_with_gpt4(content)
            logger.info("Content analyzed successfully")
            
            # Create enhanced markdown with analysis
            enhanced_content = self._create_enhanced_markdown(content, analysis)
            
            # Save the enhanced markdown
            enhanced_path = "analyzed/enhanced_article.md"
            enhanced_metadata = ContentMetadata(
                source_url=article_url,
                content_type="analyzed_article",
                context={
                    "original_path": markdown_path,
                    "analysis_summary": analysis.get('summary', ''),
                    "content_types": metadata.context.get('content_types', [])
                }
            )
            
            await self.file_service.save_to_markdown(
                content=enhanced_content,
                file_path=enhanced_path,
                metadata=enhanced_metadata
            )
            
            logger.info(f"Enhanced article saved to: {enhanced_path}")
            return enhanced_path
            
        except Exception as e:
            logger.error(f"Error analyzing article: {str(e)}")
            raise

    async def _analyze_with_gpt4(self, content: str) -> Dict[str, Any]:
        """
        Analyze content using GPT-4.
        
        :param content: Content to analyze
        :return: Analysis results
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are an expert content analyzer. Your task is to analyze the provided content 
                    and extract key information, maintaining context between different content types (text, images, audio).
                    Focus on understanding the relationships between different elements and their significance."""
                },
                {
                    "role": "user",
                    "content": f"""Please analyze the following content and provide:
                    1. A summary of the main points
                    2. Key relationships between different content types
                    3. Important context that connects different elements
                    4. Any significant details that might be relevant for answering questions
                    
                    Content:
                    {content}"""
                }
            ]
            
            response = await self.client.chat.completions.create(
                model=self.models['text'],
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error in GPT-4 analysis: {str(e)}")
            raise

    def _create_enhanced_markdown(self, original_content: str, analysis: Dict[str, Any]) -> str:
        """
        Create enhanced markdown with analysis results.
        
        :param original_content: Original markdown content
        :param analysis: Analysis results
        :return: Enhanced markdown content
        """
        enhanced_content = [
            "# Enhanced Article Analysis\n\n",
            "## Original Content\n\n",
            original_content,
            "\n\n## Analysis Results\n\n",
            "### Summary\n",
            analysis.get('summary', 'No summary available'),
            "\n\n### Key Relationships\n",
            analysis.get('relationships', 'No relationships identified'),
            "\n\n### Important Context\n",
            analysis.get('context', 'No context identified'),
            "\n\n### Significant Details\n",
            analysis.get('details', 'No significant details identified')
        ]
        
        return ''.join(enhanced_content)

    async def answer_questions(self, questions_url: str, analyzed_article_path: str) -> Dict[str, str]:
        """
        Answer questions based on the analyzed article.
        
        :param questions_url: URL of the questions
        :param analyzed_article_path: Path to the analyzed article
        :return: Dictionary of answers
        """
        try:
            # Get questions
            questions_content = await self.file_service.read_text(questions_url)
            logger.info("Questions retrieved")
            
            # Get analyzed article content
            article_content, _ = await self.file_service.get_content_with_metadata(analyzed_article_path)
            logger.info("Analyzed article retrieved")
            
            # Prepare messages for GPT-4
            messages = [
                {
                    "role": "system",
                    "content": """You are an expert at answering questions based on provided content.
                    Provide concise, accurate answers based on the analyzed article.
                    Format your response as a JSON object with question IDs as keys and answers as values."""
                },
                {
                    "role": "user",
                    "content": f"""Please answer the following questions based on the analyzed article.
                    Questions:
                    {questions_content}
                    
                    Analyzed Article:
                    {article_content}
                    
                    Provide your answers in JSON format with question IDs as keys and answers as values."""
                }
            ]
            
            response = await self.client.chat.completions.create(
                model=self.models['text'],
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error answering questions: {str(e)}")
            raise

    async def process_text(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process text content using GPT-4.
        
        :param text: Text content to process
        :param context: Optional context from other content types
        :return: Analysis results
        """
        try:
            # Check token usage
            estimated_tokens = len(text) // 4  # Rough estimation
            if estimated_tokens > self.token_limits['text']:
                logger.warning(f"Text content exceeds token limit. Truncating to {self.token_limits['text']} tokens.")
                text = text[:self.token_limits['text'] * 4]  # Truncate to limit
            
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert at analyzing text content. Provide detailed analysis focusing on key points and context."
                },
                {
                    "role": "user",
                    "content": f"""Analyze the following text content:
                    {text}
                    
                    Context from other content: {context if context else 'None'}
                    
                    Provide analysis in JSON format with:
                    - summary: Main points
                    - key_ideas: Important concepts
                    - context_notes: How this relates to other content
                    - potential_questions: Questions this content might help answer"""
                }
            ]
            
            response = await self.client.chat.completions.create(
                model=self.models['text'],
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            raise

    async def process_image(self, image_path: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process image content using GPT-4 Vision.
        
        :param image_path: Path to the image file
        :param context: Optional context from other content types
        :return: Analysis results
        """
        try:
            # Read and resize image if needed
            image_data = await self.file_service.read_binary(image_path)
            resized_image = await self.file_service.resize_image(image_data)
            
            # Convert to base64
            base64_image = base64.b64encode(resized_image).decode('utf-8')
            
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert at analyzing visual content. Provide detailed analysis focusing on visual elements and their significance."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Analyze this image in the context of the article.
                            Context from other content: {context if context else 'None'}
                            
                            Provide analysis in JSON format with:
                            - description: Detailed visual description
                            - key_elements: Important visual elements
                            - significance: How this relates to the article
                            """
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
            
            response = await self.client.chat.completions.create(
                model=self.models['image'],
                messages=messages,
                max_tokens=self.token_limits['image'],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise

    async def process_audio(self, audio_path: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process audio content using Whisper.
        
        :param audio_path: Path to the audio file
        :param context: Optional context from other content types
        :return: Analysis results
        """
        try:
            # Read audio file
            audio_data = await self.file_service.read_binary(audio_path)
            
            # Check file size
            if len(audio_data) > self.token_limits['audio']:
                raise ValueError(f"Audio file exceeds size limit of {self.token_limits['audio']} bytes")
            
            # Transcribe audio
            transcription = await self.client.audio.transcriptions.create(
                file=("audio.mp3", audio_data),
                model=self.models['audio'],
                language="pl"  # Assuming Polish language
            )
            
            # Process transcription with GPT-4
            return await self.process_text(transcription.text, context)
            
        except Exception as e:
            logger.error(f"Error processing audio: {str(e)}")
            raise

    async def create_unified_analysis(self, 
                                    text_analysis: Dict[str, Any],
                                    image_analyses: Dict[str, Dict[str, Any]],
                                    audio_analyses: Dict[str, Dict[str, Any]]) -> str:
        """
        Create a unified markdown analysis combining all content types.
        
        :param text_analysis: Text analysis results
        :param image_analyses: Dictionary of image analyses
        :param audio_analyses: Dictionary of audio analyses
        :return: Markdown content
        """
        try:
            markdown_content = [
                "# Unified Article Analysis\n\n",
                "## Text Analysis\n\n",
                f"### Summary\n{text_analysis.get('summary', 'No summary available')}\n\n",
                f"### Key Ideas\n{text_analysis.get('key_ideas', 'No key ideas identified')}\n\n",
                
                "## Image Analysis\n\n"
            ]
            
            # Add image analyses
            for img_path, analysis in image_analyses.items():
                markdown_content.extend([
                    f"### Image: {Path(img_path).name}\n\n",
                    f"Description: {analysis.get('description', 'No description available')}\n\n",
                    f"Key Elements: {analysis.get('key_elements', 'No key elements identified')}\n\n",
                    f"Significance: {analysis.get('significance', 'No significance identified')}\n\n"
                ])
            
            # Add audio analyses
            markdown_content.append("## Audio Analysis\n\n")
            for audio_path, analysis in audio_analyses.items():
                markdown_content.extend([
                    f"### Audio: {Path(audio_path).name}\n\n",
                    f"Summary: {analysis.get('summary', 'No summary available')}\n\n",
                    f"Key Points: {analysis.get('key_ideas', 'No key points identified')}\n\n"
                ])
            
            # Add potential questions
            markdown_content.extend([
                "## Potential Questions\n\n",
                "### From Text\n",
                text_analysis.get('potential_questions', 'No questions identified'),
                "\n\n### From Images\n"
            ])
            
            for analysis in image_analyses.values():
                markdown_content.append(f"{analysis.get('potential_questions', 'No questions identified')}\n\n")
            
            return ''.join(markdown_content)
        except Exception as e:
            logger.error(f"Error creating unified analysis: {str(e)}")
            return "# Error creating unified analysis\n\nAn error occurred while creating the unified analysis." 