# Factory Analyzer

## Purpose

Analyzes factory reports (text, images, audio) to identify information about:

- Captured humans or traces of human presence
- Hardware repairs/issues (excluding software problems)

## Input

- ZIP file containing factory reports
- Supported file types: .txt, .png, .mp3
- Excludes "fakty" directory

## Output

JSON file with categorized filenames:

```json
{
    "people": ["file1.txt", "file2.png", ...],
    "hardware": ["file3.txt", "file4.mp3", ...]
}
```

## Core Components

### 1. FileService

Handles all file operations:

- `download_and_extract`: Downloads and extracts ZIP file

  - Returns: Path to extracted directory or None if failed
  - Used by: Main program to get directory for processing
- `process_directory`: Walks through directory and processes files

  - Returns: Dict with categorized filenames {"people": [...], "hardware": [...]}
  - Used by: Main program to get final categorization
- `process_file`: Handles individual file processing

  - Returns: Dict with boolean flags {"has_people": bool, "has_hardware": bool}
  - Used by: process_directory to categorize each file
- Uses set for efficient file extension validation

### 2. AIService

Manages AI model interactions:

- `analyze_content`: Main method for content analysis

  - Returns: Dict with boolean flags {"has_people": bool, "has_hardware": bool}
  - Used by: process_file to determine file categorization
  - Handles different content types (text, image, audio)
  - Uses appropriate models for each type
  - Validates content format and type
- `_transcribe_with_whisper`: Internal method for audio transcription

  - Returns: Transcribed text as string
  - Used by: analyze_content for audio file processing

### 3. Models Used

- Text: GPT-4 Turbo
- Images: GPT-4 Vision
- Audio: Whisper (transcription) → GPT-4 (analysis)

## Processing Flow

1. **File Processing**:

   - Downloads and extracts ZIP
   - Processes each file based on type
   - Skips unsupported files and "fakty" directory
2. **Content Analysis**:

   - Text files: Direct GPT-4 analysis
   - Images: GPT-4 Vision analysis
   - Audio: Whisper transcription → GPT-4 analysis
3. **Categorization**:

   - People: Captured humans, remains, human presence
   - Hardware: Physical repairs, malfunctions, maintenance
   - Ignores software issues and irrelevant content

## Data Flow

1. Main program calls `download_and_extract`

   - Gets directory path for processing
2. Main program calls `process_directory`

   - For each file:
     - Calls `process_file`
     - Gets categorization flags
     - Adds filename to appropriate category list
3. `process_file` calls `analyze_content`

   - For audio files:
     - Calls `_transcribe_with_whisper`
     - Gets transcribed text
   - Gets categorization flags
4. Main program saves results to JSON

## Key Features

- Async/await for efficient I/O operations
- Robust error handling
- Type-specific prompts for better accuracy
- Efficient file extension validation using sets
- Alphabetical sorting of results

## Usage

```python
python main.py
```

Outputs: `categories.json`

## Error Handling

- Validates content types and formats
- Graceful handling of API errors
- Safe default returns on failures
- Detailed error logging
