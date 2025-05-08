import asyncio
import json
import os
from services.file_service import FileService
from services.ai_service import AIService

async def main():
    # Configuration
    zip_url = "https://centrala.ag3nts.org/dane/pliki_z_fabryki.zip"
    extract_path = "extracted_files"
    
    # Initialize services
    ai_service = AIService()
    file_service = FileService(ai_service)
    
    # Download and extract ZIP file
    print("Downloading and extracting ZIP file...")
    extracted_dir = file_service.download_and_extract(zip_url, extract_path)
    
    if not extracted_dir:
        print("Failed to download or extract ZIP file")
        return
    
    # Process files
    print("Processing files...")
    result = await file_service.process_directory(extracted_dir)
    
    # Save results
    output_file = "categories.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to {output_file}")
    print("\nCategorized files:")
    print(f"People: {len(result['people'])} files")
    print(f"Hardware: {len(result['hardware'])} files")

if __name__ == "__main__":
    asyncio.run(main()) 