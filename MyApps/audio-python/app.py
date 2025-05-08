from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from io import BytesIO
from services.OpenAiService import OpenAiService  # Note the matching case
from services.AssistantService import AssistantService
from services.LangfuseService import LangfuseService
# from dotenv import load_dotenv



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Only allows requests from this specific origin
    allow_credentials=True,                    # Allows credentials (cookies, authorization headers) to be included in requests
    allow_methods=["GET", "POST"],            # Only allows GET and POST HTTP methods
    allow_headers=["*"],                      # Allows all headers in requests
)



class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    conversation_id: Optional[str] = None

openai_service = OpenAiService()
langfuse_service = LangfuseService()
assistant_service = AssistantService(openai_service, langfuse_service)


@app.post("/api/chat")
async def chatWithLLM(request: ChatRequest):
    conversation_id = request.conversation_id or str(uuid.uuid4())

    system_message = {
        "role": "system",
        "content": "You are a helpful assistant ready to support in any kind of matter, you always start the conversation with funny 'hello' message"
    }

    try: 
        messages = [system_message] + [msg.model_dump() for msg in request.messages]
        response = await assistant_service.getLLMAnswer(
            {"messages": messages}, 
            conversation_id
        )
        return response

    except Exception as e:
        print(f"Error in chat processing: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request")
    

@app.post("/api/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        transcription = await assistant_service.transcribe_audio(contents)
        return transcription
    
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during transcription")
    
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000) 