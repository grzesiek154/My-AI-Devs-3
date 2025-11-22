import os
import base64
from pathlib import Path
from typing import Dict, List, Any
from OpenAIService import OpenAIService
from PIL import Image  # Add to requirements.txt: Pillow
from io import BytesIO
import glob
import asyncio



class ImageProcessingService:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.images_path = Path(__file__).parent / "images/mapa"
        

    async def process_image(self, messages: List[Dict[str, Any]], file: str) -> Dict[str, str | int]:
        print(self.images_path)
        try:
            with Image.open(self.images_path / file) as image:
                original_size = image.size
                print(f"Original image size: {original_size}")
                
                # Use the balanced optimization settings
                base64_image, size_kb, (width, height) = self.optimize_image_for_llm(
                    image,
                    max_size=(768, 768),  # Balanced size for maps
                    quality=100  # Good quality for text readability
                )
                
                print(f"Optimized image size: {width}x{height}")
                print(f"Optimized file size: {size_kb:.1f}KB")

            # Create messages with the optimized image
            messages_combined = [message for message in messages] + [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Analyze this map fragment and identify the Polish city it represents?"
                        }
                    ]
                }
            ]

            # Calculate tokens
            text_tokens = self.openai_service.count_tokens(messages_combined)
            image_tokens = self.openai_service.calculate_image_tokens(
                width=width,
                height=height,
                detail="high"
            )
            
            estimated_tokens = text_tokens + image_tokens

            print(f"Processing {file}:")
            print(f"  - Estimated text tokens: {text_tokens}")
            print(f"  - Estimated image tokens: {image_tokens}")
            print(f"  - Total estimated tokens: {estimated_tokens}")

            # Get completion from OpenAI
            chat_completion = await self.openai_service.completion(messages_combined)
            response = chat_completion.choices[0].message.content or ''
            actual_tokens = chat_completion.usage.total_tokens

            print(f"  - Actual tokens used: {actual_tokens}")
            print(f"  - Response: {response}")
            
            return {
                "file": file,
                "response": response,
                "estimated_tokens": estimated_tokens,
                "actual_tokens": actual_tokens,
                "image_tokens": image_tokens
            }   
        
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            raise

    async def process_images(self, messages: List[Dict[str, Any]]) -> None:
        # Get the list of image files
        image_files_path = [image_path for image_path in glob.glob(os.path.join(self.images_path, '*.jpg'))]

        # Limit to processing 4 images
        tasks = []
        for file_path in image_files_path[:4]:  # Adjust the slice to process only 4 images
            tasks.append(self.process_image_for_combination(os.path.basename(file_path)))

        # Run all tasks concurrently and gather results
        image_data_list = await asyncio.gather(*tasks)

        # Combine image data into a single message
        combined_content = [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_data['base64_image']}",
                    "detail": "high"
                }
            }
            for image_data in image_data_list
        ]

        # Add a text prompt to the combined message
        combined_content.append({
            "type": "text",
            "text": "Analyze these map fragments and identify the Polish city they represent collectively."
        })

        # Create a single message with all images
        messages_combined = [message for message in messages] + [
            {
                "role": "user",
                "content": combined_content
            }
        ]

        print("Combined Content:", combined_content)
        print("Messages Combined:", messages_combined)

        # Get completion from OpenAI
        chat_completion = await self.openai_service.completion(messages_combined)
        response = chat_completion.choices[0].message.content or ''

        print(f"Combined response: {response}")

    def process_image_for_combination(self, file: str) -> Dict[str, Any]:
        with Image.open(self.images_path / file) as image:
            # Use the balanced optimization settings
            base64_image, size_kb, (width, height) = self.optimize_image_for_llm(
                image,
                max_size=(768, 768),  # Balanced size for maps
                quality=80  # Good quality for text readability
            )
            
            return {
                "base64_image": base64_image,
                "width": width,
                "height": height
            }

    def optimize_image_for_llm(self, image: Image.Image, max_size: tuple[int, int] = (768, 768), quality: int = 100):
        """
        Optimizes image while maintaining map readability
        """
        width, height = image.size
        aspect_ratio = width / height
        
        # Calculate new size maintaining aspect ratio
        if width > height:
            new_size = (max_size[0], int(max_size[0] / aspect_ratio))
        else:
            new_size = (int(max_size[1] * aspect_ratio), max_size[1])
        
        # Use LANCZOS resampling which is better for text readability
        image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # STEP 2: Convert image to simple RGB format
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        # STEP 3: Compress image to JPEG
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=quality, optimize=True)
        
        # STEP 4: Convert to base64 for API
        image_bytes = buffer.getvalue()
        base64_string = base64.b64encode(image_bytes).decode('utf-8')
        size_kb = len(image_bytes) / 1024
        
        return base64_string, size_kb, image.size

    
