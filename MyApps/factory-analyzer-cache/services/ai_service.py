import json
import base64
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from utils.constants import OPENAI_API_KEY
from pathlib import Path
import asyncio
from PIL import Image
import io
from datetime import datetime
from .cache_service import CacheService
from ..models.content_description import ContentDescription

class AIService:
    def __init__(self, cache_service: CacheService):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.cache_service = cache_service
        
        # Define models for different content types
        self.models = {
            'image': 'gpt-4-vision-preview',
            'text': 'gpt-4-turbo-preview',
            'audio': 'whisper-1'  # For audio transcription
        }
        
        # Define prompts for description generation
        self.description_prompts = {
            'image': "Describe in detail what you see in this image. Focus on people, objects, and the overall scene.",
            'text': "Summarize the content of this text, focusing on key points and main ideas.",
            'audio': "Transcribe and summarize the content of this audio, focusing on key points and main ideas."
        }
        
        # Define prompts for categorization
        self.categorization_prompt = """
        Based on the following descriptions, categorize whether the content contains:
        1. People (has_people)
        2. Hardware/equipment (has_hardware)
        
        Return a JSON object with boolean values for each category.
        
        Descriptions:
        {descriptions}
        """

    def _resize_image(self, image_data: bytes, max_dimension: int = 1024) -> bytes:
        """Resize image to reduce dimensions while maintaining aspect ratio."""
        try:
            img = Image.open(io.BytesIO(image_data))
            ratio = min(max_dimension / max(img.size), 1.0)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            output = io.BytesIO()
            img.save(output, format='PNG')
            return output.getvalue()
        except Exception as e:
            print(f"Error resizing image: {str(e)}")
            return image_data

    async def _generate_description(self, content: Any, content_type: str, file_path: str) -> str:
        """
        Generate a description of the content using LLM.
        
        Args:
            content: Content to describe
            content_type: Type of content (image, audio, text)
            file_path: Path to the file
            
        Returns:
            Generated description
        """
        try:
            messages = []
            prompt = self.description_prompts[content_type]

            if content_type == 'image':
                content_data = self._resize_image(content)
                base64_image = base64.b64encode(content_data).decode('utf-8')
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            elif content_type == 'audio':
                transcription = await self._transcribe_audio(content, file_path)
                messages = [{"role": "user", "content": prompt + "\n\n" + transcription}]
            else:  # text
                content_str = content.decode('utf-8') if isinstance(content, bytes) else content
                messages = [{"role": "user", "content": prompt + "\n\n" + content_str}]

            response = await self.client.chat.completions.create(
                model=self.models[content_type],
                messages=messages
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating description: {str(e)}")
            raise

    async def _transcribe_audio(self, audio_content: bytes, filename: str) -> str:
        """Transcribe audio content using Whisper."""
        try:
            transcription = await self.client.audio.transcriptions.create(
                file=(filename, audio_content),
                language="pl",
                model=self.models['audio']
            )
            return transcription.text
        except Exception as e:
            print(f"Error in transcription: {str(e)}")
            raise

    async def analyze_content(self, content: Any, content_type: str, file_path: str) -> Dict[str, bool]:
        """
        Analyze content using a two-step process:
        1. Generate or retrieve description
        2. Categorize based on description
        
        Args:
            content: Content to analyze
            content_type: Type of content
            file_path: Path to the file
            
        Returns:
            Dictionary with categorization results
        """
        try:
            # Step 1: Get or generate description
            cached_desc = self.cache_service.get_description(file_path)
            if cached_desc:
                description = cached_desc.description
            else:
                description = await self._generate_description(content, content_type, file_path)
                # Save new description to cache
                new_desc = ContentDescription(
                    file_path=file_path,
                    content_type=content_type,
                    description=description,
                    created_at=datetime.now(),
                    last_used=datetime.now()
                )
                self.cache_service.save_description(new_desc)

            # Step 2: Categorize based on description
            messages = [{
                "role": "user",
                "content": self.categorization_prompt.format(descriptions=description)
            }]

            response = await self.client.chat.completions.create(
                model=self.models['text'],
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return {
                "has_people": result.get("has_people", False),
                "has_hardware": result.get("has_hardware", False)
            }

        except Exception as e:
            print(f"Error analyzing content: {str(e)}")
            return {"has_people": False, "has_hardware": False} 