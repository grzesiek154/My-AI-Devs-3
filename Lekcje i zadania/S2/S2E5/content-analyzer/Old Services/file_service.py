import os
import json
import asyncio
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from .ai_service import AIService
from utils.constants import SUPPORTED_EXTENSIONS, ERROR_MESSAGES

class FileService:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        self.analysis_dir = "analysis_results"
        self.supported_extensions = set(SUPPORTED_EXTENSIONS.keys())

    async def save_analysis_result(self, file_path: str, analysis_result: Dict) -> None:
        """
        Save the analysis result to a separate .txt file in the analysis_results directory.
        
        Args:
            file_path: Path to the original file
            analysis_result: Dictionary containing the analysis results
        """
        # Create analysis directory if it doesn't exist
        analysis_path = Path(self.analysis_dir)
        analysis_path.mkdir(exist_ok=True)
        
        # Create a filename based on the original file
        original_filename = Path(file_path).stem
        analysis_filename = f"{original_filename}_analysis.txt"
        analysis_file_path = analysis_path / analysis_filename
        
        # Format the analysis result for text file
        analysis_text = f"File: {file_path}\n"
        analysis_text += f"Content Type: {analysis_result.get('content_type', 'unknown')}\n"
        analysis_text += f"Description: {analysis_result.get('description', 'No description available')}\n"
        if 'error' in analysis_result:
            analysis_text += f"Error: {analysis_result['error']}\n"
        
        # Save the analysis result as text
        with open(analysis_file_path, 'w', encoding='utf-8') as f:
            f.write(analysis_text)

    async def analyze_files(self, directory: str) -> List[Tuple[str, str, Dict]]:
        """
        Analyze all files in the directory and save their analysis results.
        
        Args:
            directory: Path to the directory to process
            
        Returns:
            List of tuples containing (file_path, filename, analysis_result)
        """
        analyzed_files = []
        
        try:
            # Collect all files to process
            files_to_process = []
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    if file_ext not in self.supported_extensions:
                        continue
                        
                    files_to_process.append((file_path, file))
            
            # Process files concurrently
            tasks = [self.process_file(file_path) for file_path, _ in files_to_process]
            analysis_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and save analysis
            for (file_path, file), analysis_result in zip(files_to_process, analysis_results):
                if isinstance(analysis_result, Exception):
                    print(f"Error processing {file}: {str(analysis_result)}")
                    continue
                
                # Save analysis result to separate file
                await self.save_analysis_result(file_path, analysis_result)
                analyzed_files.append((file_path, file, analysis_result))
            
            return analyzed_files
            
        except Exception as e:
            print(f"Error analyzing files: {str(e)}")
            return analyzed_files

    async def categorize_files(self, analyzed_files: List[Tuple[str, str, Dict]]) -> Dict[str, List[str]]:
        """
        Categorize files based on their analysis results.
        
        Args:
            analyzed_files: List of tuples containing (file_path, filename, analysis_result)
            
        Returns:
            Dictionary containing lists of filenames for each category
        """
        result = {
            "people": [],
            "hardware": []
        }
        
        try:
            # Categorize files based on analysis results
            for _, file, analysis_result in analyzed_files:
                if analysis_result.get("has_people", False):
                    result["people"].append(file)
                if analysis_result.get("has_hardware", False):
                    result["hardware"].append(file)
            
            # Sort filenames alphabetically
            result["people"].sort()
            result["hardware"].sort()
            
            # Save final categorization to JSON
            with open("categories.json", 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            return result
            
        except Exception as e:
            print(f"Error categorizing files: {str(e)}")
            return result

    async def process_directory(self, directory: str) -> Dict[str, List[str]]:
        """
        Process all files in the directory, analyze them, and categorize the results.
        
        Args:
            directory: Path to the directory to process
            
        Returns:
            Dictionary containing lists of filenames for each category
        """
        # First analyze all files
        analyzed_files = await self.analyze_files(directory)
        
        # Then categorize the analyzed files
        return await self.categorize_files(analyzed_files)

    async def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a single file and return its analysis result.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Dictionary containing the analysis result
        """
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Get file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Determine content type
            if file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                content_type = 'image'
            elif file_ext in ['.mp3', '.wav', '.ogg']:
                content_type = 'audio'
            elif file_ext in ['.txt', '.md']:
                content_type = 'text'
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
            
            # Analyze content
            return await self.ai_service.analyze_content(content, content_type, file_path)
            
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return {"has_people": False, "has_hardware": False}      