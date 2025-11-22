from typing import Optional, Dict, Any, AsyncGenerator, List
import os
from openai import AsyncOpenAI
import aiofiles
import tempfile
from pathlib import Path
import logging


OPENAI_API_KEY_AI_DEVS_3=os.getenv("OPENAI_API_KEY_AI_DEVS_3")

class OpenAIService:
    def __init__(self):
        self.openai = AsyncOpenAI(api_key=OPENAI_API_KEY_AI_DEVS_3)
        self.logger = logging.getLogger(__name__)


    async def completion(self, config: Dict[str, Any]) -> Dict[str, Any]:
    
        try:
            messages = config.get("messages", [])
            model = config.get("model", "gpt-4")
            temperature = config.get("temperature", 0)
            max_tokens = config.get("max_tokens", 4096)

            chat_completion = await self.openai.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens

            )

            return chat_completion
        
        except Exception as e:
                print(f"Error in OpenAI completion: {str(e)}")
                raise 



    async def transcribe(self, file_path: Path) -> str:
        try:
            # Make async API call for transcription
            transcription = await self.openai.audio.transcriptions.create(
                file=file_path,
                language="pl",
                model="whisper-1"
            )

            return transcription.text

        except Exception as e:
            self.logger.error(f"Error in transcription: {str(e)}")
            raise
         
         