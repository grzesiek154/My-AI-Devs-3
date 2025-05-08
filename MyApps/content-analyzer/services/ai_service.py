import json
import base64
import os
from typing import Dict, Any
from openai import AsyncOpenAI
from utils.constants import OPENAI_API_KEY, ANALYZE_IMAGE_PROMPT, ANALYZE_TEXT_PROMPT, ANALYZE_AUDIO_PROMPT
from pathlib import Path
import asyncio
from PIL import Image
import io

class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        # Define models for different content types
        self.models = {
            'image': 'gpt-4-vision-preview',
            'text': 'gpt-4-turbo-preview',
            'audio': 'whisper-1'  # For audio transcription
        }
        # Define prompts for different content types
        self.prompts = {
            'image': ANALYZE_IMAGE_PROMPT,
            'text': ANALYZE_TEXT_PROMPT,
            'audio': ANALYZE_AUDIO_PROMPT
        }

    async def analyze_content(self, content: Any, content_type: str, file_path: str) -> Dict[str, Any]:
        """
        Analyze content and return detailed analysis results.
        
        Args:
            content: The content to analyze
            content_type: Type of content ('image', 'audio', 'text')
            file_path: Path to the file being analyzed
            
        Returns:
            Dictionary containing detailed analysis results
        """
        try:
            # First validation: Check if we have a model for this content type
            if content_type not in self.models:
                raise ValueError(f"Unsupported content type: {content_type}")

            # Get actual content and filename from content object
            content_data = getattr(content, 'content', content)
            filename = getattr(content, 'name', None)
            
            # Second validation: Check if the content is in a format we can process
            if not isinstance(content_data, (bytes, str)):
                raise ValueError(f"Content must be bytes or string, got {type(content_data)}")
            
            messages = []
            prompt = self.prompts[content_type]

            if content_type == 'image':
                # Always resize high-resolution images to reduce token count
                content_data = self._resize_image(content_data)
                
                base64_image = base64.b64encode(content_data).decode('utf-8')
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt.format(content=base64_image)
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"  # Changed to image/png
                                }
                            }
                        ]
                    }
                ]
                model = self.models['image']
            elif content_type == 'audio':
                # Audio must be in bytes format for transcription
                if not isinstance(content_data, bytes):
                    raise ValueError("Audio content must be bytes")
                # Use actual filename or default to 'audio.mp3'
                filename = filename or 'audio.mp3'
                transcription = await self.transcribe_audio(content_data, filename)
                messages = [{"role": "user", "content": prompt.format(content=transcription)}]
                model = self.models['text']
            else:  # text
                # Text can be either bytes or string, convert bytes to string if needed
                content_str = content_data.decode('utf-8') if isinstance(content_data, bytes) else content_data
                messages = [{"role": "user", "content": prompt.format(content=content_str)}]
                model = self.models['text']
            
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            
            return {
                'file_path': file_path,
                'content_type': content_type,
                'description': result.get('description', ''),
                'has_people': result.get('has_people', False),
                'has_hardware': result.get('has_hardware', False)
            }
            
        except Exception as e:
            print(f"Error analyzing content: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            print(f"Content type: {content_type}")
            print(f"Content length: {len(content_data) if content_data else 0}")
            if hasattr(e, 'response'):
                print(f"API Response: {e.response}")
            return {
                'file_path': file_path,
                'content_type': content_type,
                'error': str(e),
                'has_people': False,
                'has_hardware': False
            }

    def _resize_image(self, image_data: bytes, max_dimension: int = 1024) -> bytes:
        """
        Resizes an image to reduce its dimensions while maintaining aspect ratio.
        Handles PNG images with transparency and different color modes.
        
        Args:
            image_data: Original image data in bytes
            max_dimension: Maximum dimension (width or height) in pixels
            
        Returns:
            Resized image data in bytes
        """
        try:
            # Open image from bytes
            img = Image.open(io.BytesIO(image_data))
            
            # Print original dimensions and format
            print(f"Original image dimensions: {img.size}")
            print(f"Original image mode: {img.mode}")
            
            # Calculate new dimensions while maintaining aspect ratio
            ratio = min(max_dimension / max(img.size), 1.0)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            
            # Handle transparency and color modes
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                # Convert to RGBA to preserve transparency
                img = img.convert('RGBA')
                # Create a white background
                background = Image.new('RGBA', new_size, (255, 255, 255, 255))
                # Resize the image
                resized = img.resize(new_size, Image.Resampling.LANCZOS)
                # Composite the resized image onto the white background
                img = Image.alpha_composite(background, resized)
            else:
                # For non-transparent images, just resize
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Print new dimensions
            print(f"Resized image dimensions: {img.size}")
            
            # Convert back to bytes
            output = io.BytesIO()
            # Save as PNG to preserve quality and transparency
            img.save(output, format='PNG')
            return output.getvalue()
        except Exception as e:
            print(f"Error resizing image: {str(e)}")
            return image_data  # Return original if resize fails

    async def transcribe_audio(self, audio_content: bytes, filename: str) -> str:
        """
        Transcribes audio content using OpenAI's Whisper model.
        
        Args:
            audio_content: The audio data in bytes
            filename: Name of the audio file including extension
            
        Returns:
            Transcribed text
        """
        try:
            # Check if the audio content is empty
            if not audio_content:
                raise ValueError("Audio content is empty")

            # Make async API call for transcription
            transcription = await self.client.audio.transcriptions.create(
                file=(filename, audio_content),
                language="pl",
                model=self.models['audio']
            )
            return transcription.text

        except Exception as e:
            error_msg = str(e)
            if "Unrecognized file format" in error_msg:
                print("Error: Unsupported audio format. Please use one of: flac, m4a, mp3, mp4, mpeg, mpga, oga, ogg, wav, webm")
            else:
                print(f"Error in transcription: {error_msg}")
            raise



