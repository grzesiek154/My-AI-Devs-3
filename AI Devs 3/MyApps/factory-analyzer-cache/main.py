import asyncio
import sys
from pathlib import Path
from services.cache_service import CacheService
from services.ai_service import AIService
from services.file_service import FileService

async def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]
    if not Path(directory).exists():
        print(f"Error: Directory '{directory}' does not exist")
        sys.exit(1)

    try:
        # Initialize services
        cache_service = CacheService()
        ai_service = AIService(cache_service)
        file_service = FileService(ai_service, cache_service)

        # Process directory
        print(f"Processing directory: {directory}")
        result = await file_service.process_directory(directory)

        # Print results
        print("\nResults:")
        print("Files with people:")
        for file in result["people"]:
            print(f"  - {file}")
        
        print("\nFiles with hardware:")
        for file in result["hardware"]:
            print(f"  - {file}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 