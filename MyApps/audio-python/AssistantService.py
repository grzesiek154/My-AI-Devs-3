from typing import Dict, Any, List, Optional
from services.OpenAiService import OpenAiService
from .LangfuseService import LangfuseService
import uuid
import tempfile
from pathlib import Path
import logging
import os


class AssistantService:
    def __init__(self, openai_service: OpenAiService, langfuse_service: LangfuseService):
        self.openai_service = openai_service
        self.langfuse_service = langfuse_service
        self.logger = logging.getLogger(__name__)

    async def getLLMAnswer(self, request: Dict[str, Any], conversation_id: str) -> str:
        # Create trace with the same parameters as in app.py
        messages = request.get("messages", [])
        trace = self.langfuse_service.create_trace({
            "id": str(uuid.uuid4()),
            "name": messages[-1].get("content", "")[:45] if messages else "",
            "session_id": conversation_id
        })
        
        try:
            # Create generation for this specific response
            generation = self.langfuse_service.create_generation(trace, "Answer", {"messages": messages})

            # Get completion from OpenAI
            completion = await self.openai_service.completion(request)
            
            # Log successful completion with usage statistics
            self.langfuse_service.finalize_generation(
                generation,
                completion.choices[0].message,
                completion.model,
                {
                    "promptTokens": completion.usage.prompt_tokens,
                    "completionTokens": completion.usage.completion_tokens,
                    "totalTokens": completion.usage.total_tokens
                }
            )

            # Finalize trace with success status
            await self.langfuse_service.finalize_trace(
                trace,
                request,
                {"status": "success"}
            )

            return completion.choices[0].message.content

        except Exception as e:
            # Finalize trace with error status

            await self.langfuse_service.finalize_generation(
                generation,
                str(e),
                "gpt-3.5-turbo",
                status="error"
            )
            await self.langfuse_service.finalize_trace(
                trace,
                request,
                {"error": str(e)}
            )
            raise

    async def transcribe_audio(self, audio_data: bytes) -> str:
        temp_path = None
        try:
            # Create a temporary file for audio data
            temp_path = self.create_temp_file(audio_data)

            # Use OpenAiService to transcribe the audio
            transcription = await self.openai_service.transcribe(temp_path)

            return transcription

        except Exception as e:
            self.logger.error(f"Error in transcription: {str(e)}") 
            raise

        finally:
            # Ensure the temporary file is deleted
            if temp_path and temp_path.exists():
                try:
                    os.unlink(temp_path)
                except Exception as e:
                    self.logger.error(f"Error deleting temporary file: {str(e)}")



    def create_temp_file(self, audio_data: bytes) -> Path:
        try:
            with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as temp_file:
                temp_file.write(audio_data)
                return Path(temp_file.name)
        except Exception as e:
            self.logger.error(f"Error creating temporary file: {str(e)}")
            raise

