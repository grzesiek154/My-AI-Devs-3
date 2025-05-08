| Directory/Example                        | Purpose                        | Key Features                                                                                             | Related Tools/Technologies      |
| ---------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------------------------------- | ------------------------------- |
| `captions`                             | Image description generation   | - Works with VLM (Vision-Language Models)                                                                | Vision-Language Models          |
| `read`                                 | Text to audio conversion       | - Converts lesson content to audio`<br>`- Maintains original speaking style                            | ElevenLabs                      |
| `demo` and `demo_2`                  | Audio generation examples      | - Contains recordings generated with ElevenLabs                                                          | ElevenLabs                      |
| `mindmap`                              | Voice to mind map conversion   | - Basic implementation of "conversation with mind map"`<br>`- Converts voice notes to visual mind maps | markmap-cli                     |
| `audio`                                | Interface for audio processing | - Voice interaction system                                                                               | -                               |
| `audio-map` and `audio-map-frontend` | New version of audio interface | - "Talking with mind map" functionality`<br>`- Real-time processing                                    | Whisper Turbo, ElevenLabs Turbo |
| `notes`                                | Context-aware note processing  | - Contains sample messages`<br>`- Handles different note types`<br>`- Context-aware formatting       | -                               |
| `linear` (from S01E02)                 | Context handling               | - Category description management`<br>`- Ambiguity resolution`<br>`- Clear category definitions      | -                               |

# Next Steps

## 1. Add Money to OpenAI Account
- [ ] Log in to OpenAI platform
- [ ] Add payment method
- [ ] Verify billing information
- [ ] Check API key access

## 2. Test AIService
- [ ] Test text processing
  - [ ] Verify token limits
  - [ ] Check context handling
  - [ ] Validate analysis output
- [ ] Test image processing
  - [ ] Verify image resizing
  - [ ] Check Vision API integration
  - [ ] Validate image analysis
- [ ] Test audio processing
  - [ ] Verify Whisper integration
  - [ ] Check transcription quality
  - [ ] Validate audio analysis

## 3. Test ArticleService
- [ ] Test article fetching
  - [ ] Verify HTML parsing
  - [ ] Check content extraction
  - [ ] Validate metadata handling
- [ ] Test content processing
  - [ ] Verify text analysis
  - [ ] Check image processing
  - [ ] Validate unified analysis
- [ ] Test markdown generation
  - [ ] Verify formatting
  - [ ] Check content structure
  - [ ] Validate metadata inclusion

## Testing Checklist
- [ ] Set up test environment
- [ ] Create test cases
- [ ] Run individual service tests
- [ ] Run integration tests
- [ ] Verify error handling
- [ ] Check logging
- [ ] Validate output formats
