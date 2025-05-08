from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from io import BytesIO
from OpenAIService import OpenAIService
from ImageProcessingService import ImageProcessingService
from HttpService import HttpService
import asyncio



app = FastAPI()



class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    conversation_id: Optional[str] = None

openai_service = OpenAIService()
image_processing_service = ImageProcessingService()
http_service = HttpService()



async def main():
    """
    Main method to demonstrate and test ImageProcessingService functionality.
    """
    system_prompt = """You are an expert cartographer specializing in Polish cities and their urban layouts. Your primary task is to analyze map fragments and identify Polish cities based on the presence of key features, especially breadbaskets and fortresses.

Key Identification Criteria:
1. **Breadbasket and Fortresses**:
   - Focus on identifying cities known for their agricultural significance (breadbasket) and historical fortifications (fortresses).
   - Look for signs of large agricultural areas and defensive structures.

2. **Street Names Analysis**:
   - Identify characteristic street names that might indicate historical or regional significance.
   - Look for patterns unique to specific cities.

3. **Landmarks and Points of Interest**:
   - Identify key landmarks such as churches, stations, markets, and squares.
   - Look for universities, parks, or major institutions that might indicate a city's identity.

4. **Urban Layout**:
   - Analyze the street grid pattern (medieval, planned, radial, etc.).
   - Look for characteristic features like ring roads and main arteries.

5. **Regional Context**:
   - Consider the style of street names and regional variations.
   - Look for district names that might indicate the region.
   - Use your knowledge of Polish urban development.

**Exclusion Criteria**:
- Do not consider the following cities: Kraków, Warsaw, Gdańsk, Wrocław, Łódź, Poznań.

Output Format:
1. City Name: [Name of the identified city]
2. Confidence Level: [High/Medium/Low]
3. Key Identifiers: [List 2-3 main features that led to this identification]
4. Alternative Possibilities: [If confidence is not high, list other possible cities]
5. Provide a chain of thought and reasoning process.

Remember:
- Always provide a specific city name, even if confidence is low.
- Explain your reasoning based on visible map features.
- Consider historical context of urban development.
- If uncertain, explain why and list alternatives.
- Always prioritize cities with breadbaskets and fortresses in your analysis.
- Attempt to identify the city based on the collective information from all images.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]
    
    try:
        imageProcessingService = ImageProcessingService()
        await imageProcessingService.process_image(messages, "image2.jpg")
        # await imageProcessingService.process_images(messages)
    except Exception as e:
        print(f"Error in main: {str(e)}")



if __name__ == "__main__":
    asyncio.run(main()) 