import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = "gpt-4-turbo-preview"

# Analysis prompts for different content types
ANALYZE_TEXT_PROMPT = """
You are analyzing a text document from a factory report. Look for specific information about:
1. People (captured humans or traces of captured humans presence)
2. Hardware repairs or issues (excluding software-related problems)

Text content to analyze:
{content}

Respond in JSON format with boolean values:
{{
    "has_people": true/false,
    "has_hardware": true/false
}}

Only mark as true if there is explicit information about:
- has_people: captured humans, human remains, or clear evidence of captured humans presence
- has_hardware: specific hardware repairs, malfunctions, or maintenance issues

Ignore software-related issues and general technical reports unless they specifically mention hardware problems.
"""

ANALYZE_IMAGE_PROMPT = """
You are analyzing an image from a factory report. Look for visual evidence of:
1. People (captured humans, human remains, or clear traces of captured humans presence)
2. Hardware repairs or issues (physical damage, repairs, or maintenance work)

Image content to analyze:
[Image content]

Respond in JSON format with boolean values:
{{
    "has_people": true/false,
    "has_hardware": true/false
}}

Only mark as true if you can clearly see:
- has_people: actual humans, human remains, or undeniable evidence of captured human presence
- has_hardware: physical damage, repair work, or maintenance activities on machinery/equipment

Ignore software interfaces, screens, or general technical equipment unless they show physical damage or repair work.
"""

ANALYZE_AUDIO_PROMPT = """
You are analyzing an audio recording from a factory report. Listen for mentions of:
1. People (captured humans or traces of captured humans presence)
2. Hardware repairs or issues (excluding software-related problems)

Transcribed audio content:
{content}

Respond in JSON format with boolean values:
{{
    "has_people": true/false,
    "has_hardware": true/false
}}

Only mark as true if there are explicit mentions of:
- has_people: captured humans, human remains, or clear evidence of captured humans presence
- has_hardware: specific hardware repairs, malfunctions, or maintenance issues

Ignore software-related issues and general technical reports unless they specifically mention hardware problems.
"""

# File type configurations
SUPPORTED_EXTENSIONS = {
    '.txt': 'text',
    '.png': 'image',
    '.mp3': 'audio'
}

# Error messages
ERROR_MESSAGES = {
    'invalid_file_type': 'Unsupported file type',
    'file_not_found': 'File not found',
    'processing_error': 'Error processing file',
    'api_error': 'Error communicating with OpenAI API'
}