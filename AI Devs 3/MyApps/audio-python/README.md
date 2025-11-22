# Audio Processing and Transcription Application

## Project Overview

A FastAPI-based application that processes audio files, transcribes them using OpenAI's Whisper model, and performs analysis on the transcribed text using GPT models. The application includes conversation tracking and monitoring through Langfuse integration.

## Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key
- Langfuse account
- FastAPI

### Environment Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure API keys in environment variables:
   ```env
   OPENAI_API_KEY=your_key_here
   LANGFUSE_PUBLIC_KEY=your_key_here
   LANGFUSE_SECRET_KEY=your_key_here
   ```
4. Run server: `python app.py`

## Architecture

### Services Layer

1. **OpenAIService**
   - Handles OpenAI API interactions
   - Manages audio transcription (Whisper)
   - Processes chat completions (GPT)

2. **AssistantService**
   - Orchestrates service interactions
   - Manages temporary file handling
   - Coordinates conversation flow

3. **LangfuseService**
   - Handles conversation monitoring
   - Tracks API usage and performance
   - Manages analytics data

4. **HttpService**
   - Manages external API communications
   - Handles both JSON and non-JSON responses

### API Endpoints

- `/api/chat`: Chat interactions endpoint
- `/api/transcribe`: Audio transcription endpoint

## Usage Examples

### Audio Transcription
```python
audio_data = read_file("audio.m4a", "rb")
transcription = await assistant_service.transcribe_audio(audio_data)
```

### Chat Interaction
```python
response = await assistant_service.getLLMAnswer(
    {"messages": messages}, 
    conversation_id
)
```

## Project Structure
```
audio-python/
├── app.py                 # Main application file
├── services/             # Service modules
│   ├── OpenAIService.py
│   ├── AssistantService.py
│   ├── LangfuseService.py
│   └── HttpService.py
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Technical Notes

### Key Features
- Asynchronous API calls
- Temporary file management for audio processing
- Conversation context maintenance
- Error handling and logging
- External API integration

### Dependencies
```
fastapi
python-dotenv
openai
langfuse
httpx
python-multipart
```

## Common Operations

### Audio Processing
1. Upload audio file
2. Process through Whisper
3. Save transcription

### Chat Processing
1. Send messages
2. Process through GPT
3. Track conversation

### API Communication
1. Send HTTP requests
2. Process responses
3. Handle errors

## Troubleshooting

Common issues and their solutions:
- File encoding issues
- API rate limiting
- Temporary file cleanup
- Error handling strategies
