import json
import base64
from typing import Dict, Any
from openai import OpenAI
from ..utils.constants import (
    OPENAI_API_KEY, 
    MODEL_NAME, 
    ANALYZE_TEXT_PROMPT,
    ANALYZE_IMAGE_PROMPT,
    ANALYZE_AUDIO_PROMPT
)

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
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

    async def analyze_content(self, content: Any, content_type: str) -> Dict[str, bool]:
        """
        Analyzes content using OpenAI's API and returns categorization.
        Uses different models and prompts based on content type.

        Args:
            content: The actual content to analyze (can be bytes or string)
            content_type: Type of content ('image', 'text', or 'audio')

        Returns:
            Dict with boolean flags for people and hardware presence
        """
        try:
            # First validation: Check if we have a model for this content type
            # This ensures we can actually process this type of content
            # Example: 'pdf' would fail here as we don't have a model for it
            if content_type not in self.models:
                raise ValueError(f"Unsupported content type: {content_type}")
            
            # Second validation: Check if the content is in a format we can process
            # We only accept bytes (for binary data like images/audio) or strings (for text)
            # Example: passing a list or dict would fail here
            if not isinstance(content, (bytes, str)):
                raise ValueError(f"Content must be bytes or string, got {type(content)}")

            prompt = self.prompts[content_type]
            messages = []

            # Handle each content type with specific processing logic
            if content_type == 'image':
                # Images must be in bytes format for base64 encoding
                if not isinstance(content, bytes):
                    raise ValueError("Image content must be bytes")
                base64_image = base64.b64encode(content).decode('utf-8')
                messages = [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt.format(content="[Image content]")},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                    ]
                }]
                model = self.models['image']

            elif content_type == 'audio':
                # Audio must be in bytes format for transcription
                if not isinstance(content, bytes):
                    raise ValueError("Audio content must be bytes")
                transcription = await self.transcribe_audio(content)
                messages = [{"role": "user", "content": prompt.format(content=transcription)}]
                model = self.models['text']

            else:  # text
                # Text can be either bytes or string, convert bytes to string if needed
                content_str = content.decode('utf-8') if isinstance(content, bytes) else content
                messages = [{"role": "user", "content": prompt.format(content=content_str)}]
                model = self.models['text']

            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            print(result)
            return {
                "has_people": result.get("has_people", False),
                "has_hardware": result.get("has_hardware", False)
            }

        except Exception as e:
            print(f"Error analyzing content: {str(e)}")
            return {"has_people": False, "has_hardware": False}

    async def transcribe_audio(self, audio_content: bytes) -> str:
        """
        Transcribes audio content using OpenAI's Whisper model.
        
        Args:
            audio_content: Raw audio data in bytes format
            
        Returns:
            Transcribed text as string
        """
        try:
            response = await self.client.audio.transcriptions.create(
                file=("audio.mp3", audio_content),
                model=self.models['audio']
            )
            return response.text
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return "" 