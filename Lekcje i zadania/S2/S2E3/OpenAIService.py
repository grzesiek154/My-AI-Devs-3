from typing import Optional, Dict, Any, AsyncGenerator, List, Literal
from openai import AsyncOpenAI
import aiofiles
import tempfile
import logging
import os
import json
from tiktoken import encoding_for_model


class OpenAIService:
    def __init__(self):
        self.openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.logger = logging.getLogger(__name__)
        self._tokenizer = {}
        self._IM_START = "<|im_start|>"
        self._IM_END = "<|im_end|>"
        self._IM_SEP = "<|im_sep|>"


    def _get_tokenizer(self, model_name: str):
        """Get a tokenizer for the specified model."""
        if model_name not in self._tokenizer:
            tokenizer = encoding_for_model(model_name)
            self._tokenizer[model_name] = tokenizer
        return self._tokenizer[model_name]
    
    
    def count_tokens(
        self, 
        messages: List[Dict[str, Any]], 
        model: str = 'gpt-4',
        use_chat_format: bool = True
    ) -> int:
        """
        Flexible token counting with option to use chat formatting.
        
        Args:
            messages: List of message objects
            model: The model to use for tokenization
            use_chat_format: Whether to use special chat formatting tokens
            
        Returns:
            Number of tokens
        """
        try:
            tokenizer = self._get_tokenizer(model)
            
            if not use_chat_format:
                # Simple counting without special formatting
                total_tokens = 0
                for message in messages:
                    content = message.get('content', '')
                    if isinstance(content, list):
                        text_contents = [
                            part['text'] for part in content 
                            if isinstance(part, dict) and 'text' in part
                        ]
                        content = ' '.join(text_contents)
                    
                    text = f"{message['role']} {content}"
                    total_tokens += len(tokenizer.encode(text))
                return total_tokens
                
            else:
                # Chat format with special tokens
                formatted_content = ''
                for message in messages:
                    content = message.get('content', '')
                    if isinstance(content, list):
                        text_contents = [
                            part['text'] for part in content 
                            if isinstance(part, dict) and 'text' in part
                        ]
                        content = ' '.join(text_contents)
                    
                    formatted_content += (
                        f"{self._IM_START}{message['role']}"
                        f"{self._IM_SEP}{content}{self._IM_END}"
                    )
                
                return len(tokenizer.encode(formatted_content))
                
        except Exception as e:
            print(f"Error counting tokens: {str(e)}")
            raise

    async def completion(self, messages: List[Dict[str, Any]], model: str = "gpt-4o", temperature: float = 0,
              stream: bool = False, json_mode: bool = False, max_tokens: int = 1024) -> Dict[str, Any]:
        try:
            response = await self.openai.chat.completions.create(
                model=model,
                messages=messages,
                stream=stream,
                response_format={"type": "json_object"} if json_mode else None,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response
        
        except Exception as e:
            print(f"Error in OpenAI completion: {str(e)}")
            raise

    
    async def generate_image_url(self, prompt: str, size: str = "1024x1024", model: str = "dall-e-3") -> str:
        """Generate an image using the OpenAI API."""
        try:
            response = await self.openai.images.generate(
                prompt=prompt,
                n=1,
                size=size,
                model=model,
                response_format="url"
            )
            return response.data[0].url
        
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            raise        

    async def get_completion_content(self, messages: List[Dict[str, Any]], model: str = "gpt-4o-mini", temperature: float = 0,
              stream: bool = False, json_mode: bool = False, max_tokens: int = 1024) -> Dict[str, Any]:
        try:
            response = await self.openai.chat.completions.create(
                model=model,
                messages=messages,
                stream=stream,
                response_format={"type": "json_object"} if json_mode else None,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Error in OpenAI completion: {str(e)}")
            raise

    def calculate_image_tokens(self, width: int, height: int, detail: Literal['low', 'high']) -> int:
        """
        Calculate the number of tokens required for an image based on its dimensions and detail level.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            detail: Detail level ('low' or 'high')
            
        Returns:
            Number of tokens required
        """
        try:
            token_cost = 0
            
            if detail == 'low':
                token_cost += 85
                return token_cost
                
            MAX_DIMENSION = 2048
            SCALE_SIZE = 768
            
            # Resize to fit within MAX_DIMENSION x MAX_DIMENSION
            if width > MAX_DIMENSION or height > MAX_DIMENSION:
                aspect_ratio = width / height
                if aspect_ratio > 1:
                    width = MAX_DIMENSION
                    height = round(MAX_DIMENSION / aspect_ratio)
                else:
                    height = MAX_DIMENSION
                    width = round(MAX_DIMENSION * aspect_ratio)
            
            # Scale the shortest side to SCALE_SIZE
            if width >= height and height > SCALE_SIZE:
                width = round((SCALE_SIZE / height) * width)
                height = SCALE_SIZE
            elif height > width and width > SCALE_SIZE:
                height = round((SCALE_SIZE / width) * height)
                width = SCALE_SIZE
            
            # Calculate the number of 512px squares
            num_squares = ((width + 511) // 512) * ((height + 511) // 512)
            
            # Calculate the token cost
            token_cost += (num_squares * 170) + 85
            
            return token_cost
        except Exception as e:
            print(f"Error calculating image tokens: {str(e)}")
            raise



    def transform_message_content(message: Dict) -> Dict:
        """Transform message content to the required format."""
        if isinstance(message.get('content'), str):
            return message
        
        # Handle array of content parts
        if isinstance(message.get('content'), list):
            text_content = next(
                (part.get('text') for part in message['content'] 
                if isinstance(part, dict) and 'text' in part),
                ''
            )
            return {'role': message['role'], 'content': text_content}
        
        return message
    

     