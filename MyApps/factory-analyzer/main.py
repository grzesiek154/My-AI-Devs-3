import asyncio
import sys
from pathlib import Path
from services.ai_service import AIService
from services.file_service import FileService

async def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <command> <directory_path>")
        print("Commands:")
        print("  analyze    - Analyze files and save results")
        print("  categorize - Categorize files based on analysis")
        print("  process    - Analyze and categorize files")
        sys.exit(1)

    command = sys.argv[1]
    directory = sys.argv[2]

    if not Path(directory).exists():
        print(f"Error: Directory '{directory}' does not exist")
        sys.exit(1)

    try:
        # Initialize services
        ai_service = AIService()
        file_service = FileService(ai_service)

        if command == "analyze":
            # Analyze files only
            print(f"Analyzing files in directory: {directory}")
            analyzed_files = await file_service.analyze_files(directory)
            
            print("\nAnalysis Results:")
            print("=" * 50)
            for file_path, file, analysis_result in analyzed_files:
                print(f"\nFile: {file}")
                print(f"Content Type: {analysis_result.get('content_type', 'unknown')}")
                print(f"Description: {analysis_result.get('description', 'No description available')}")
                if 'error' in analysis_result:
                    print(f"Error: {analysis_result['error']}")
            
            print("\nDetailed analysis files have been saved in the 'analysis_results' directory.")

        elif command == "categorize":
            # First analyze files if needed
            print(f"Analyzing files in directory: {directory}")
            analyzed_files = await file_service.analyze_files(directory)
            
            # Then categorize
            print("\nCategorizing files...")
            result = await file_service.categorize_files(analyzed_files)
            
            print("\nCategorization Results:")
            print("=" * 50)
            
            print("\nFiles with people:")
            print("-" * 20)
            for file in result["people"]:
                print(f"  - {file}")
            
            print("\nFiles with hardware:")
            print("-" * 20)
            for file in result["hardware"]:
                print(f"  - {file}")
            
            print("\nCategorization results have been saved to 'categories.json'")

        elif command == "process":
            # Process all (analyze and categorize)
            print(f"Processing directory: {directory}")
            result = await file_service.process_directory(directory)
            
            print("\nResults:")
            print("=" * 50)
            
            print("\nFiles with people:")
            print("-" * 20)
            for file in result["people"]:
                print(f"  - {file}")
            
            print("\nFiles with hardware:")
            print("-" * 20)
            for file in result["hardware"]:
                print(f"  - {file}")
            
            print("\nAnalysis files have been saved in the 'analysis_results' directory.")
            print("Categorization results have been saved to 'categories.json'")

        else:
            print("Invalid command. Use 'analyze', 'categorize', or 'process'")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 