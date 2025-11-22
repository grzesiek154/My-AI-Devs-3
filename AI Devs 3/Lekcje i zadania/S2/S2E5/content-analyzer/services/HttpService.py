import httpx
import json
import logging
from typing import Optional, Union, Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HttpServiceError(Exception):
    """Base exception for HttpService errors"""
    pass

class HttpService:
    def __init__(self, default_headers: Optional[Dict[str, str]] = None, timeout: int = 30, max_retries: int = 3):
        """
        Initialize the HttpService with optional default headers, timeout, and retry settings.
        
        :param default_headers: Default headers for requests
        :param timeout: Default timeout for requests in seconds
        :param max_retries: Maximum number of retry attempts
        """
        self.default_headers = default_headers or {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.timeout = timeout
        self.max_retries = max_retries

    async def _make_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        Make an HTTP request with retry logic.
        
        :param method: HTTP method (GET, POST, etc.)
        :param url: Target URL
        :param kwargs: Additional arguments for the request
        :return: Response object
        :raises HttpServiceError: If request fails after all retries
        """
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.request(method, url, **kwargs)
                    response.raise_for_status()
                    return response
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code} for {url}: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise HttpServiceError(f"HTTP request failed after {self.max_retries} attempts: {str(e)}")
            except httpx.RequestError as e:
                logger.error(f"Request error for {url}: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise HttpServiceError(f"Request failed after {self.max_retries} attempts: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error for {url}: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise HttpServiceError(f"Unexpected error after {self.max_retries} attempts: {str(e)}")

    async def get_html(self, url: str) -> BeautifulSoup:
        """
        Fetch and parse HTML content from a URL.
        
        :param url: URL to fetch
        :return: BeautifulSoup object with parsed HTML
        :raises HttpServiceError: If request or parsing fails
        """
        try:
            response = await self._make_request('GET', url, headers={'Accept': 'text/html'})
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            raise HttpServiceError(f"Failed to fetch or parse HTML from {url}: {str(e)}")

    async def get_binary(self, url: str) -> bytes:
        """
        Fetch binary data from a URL.
        
        :param url: URL to fetch
        :return: Binary data
        :raises HttpServiceError: If request fails
        """
        try:
            response = await self._make_request('GET', url, headers={'Accept': '*/*'})
            return response.content
        except Exception as e:
            raise HttpServiceError(f"Failed to fetch binary data from {url}: {str(e)}")

    async def post_json(self, url: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Any], str]:
        """
        Post JSON data to a specified endpoint.
        
        :param url: The endpoint URL
        :param data: The JSON data to send
        :param headers: Custom headers
        :return: Response data (JSON or text)
        :raises HttpServiceError: If request fails
        """
        headers = headers or self.default_headers
        try:
            response = await self._make_request('POST', url, json=data, headers=headers)
            try:
                return response.json()
            except json.JSONDecodeError:
                logger.warning(f"Response from {url} is not JSON format")
                return response.text
        except Exception as e:
            raise HttpServiceError(f"Failed to post JSON to {url}: {str(e)}")

    def is_valid_url(self, url: str) -> bool:
        """
        Check if a URL is valid.
        
        :param url: URL to validate
        :return: True if URL is valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    async def process_api_request(self, url: str, data: Dict[str, Any]) -> bool:
        """
        Process an API request and check its response.
        
        :param url: The endpoint URL
        :param data: The data to send
        :return: True if request was successful, False otherwise
        :raises HttpServiceError: If request fails
        """
        try:
            response = await self.post_json(url, data)
            
            if isinstance(response, dict):
                if response.get('code') == 0:
                    logger.info(f"API request successful: {response}")
                    return True
                else:
                    logger.warning(f"API request failed: {response}")
                    return False
            else:
                logger.warning(f"Received non-JSON response: {response}")
                return False
                
        except HttpServiceError as e:
            logger.error(f"API request failed: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during API request: {str(e)}")
            return False

    async def get_text(self, url: str) -> str:
        """
        Fetch and extract text content from a URL.
        
        :param url: URL to fetch
        :return: Extracted text content
        :raises HttpServiceError: If request fails
        """
        try:
            # First try to get plain text
            response = await self._make_request('GET', url, headers={'Accept': 'text/plain'})
            content = response.text
            
            # If content looks like HTML, parse it
            if '<html' in content.lower() or '<body' in content.lower():
                soup = BeautifulSoup(content, 'html.parser')
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                # Get text
                content = soup.get_text()
                # Clean up whitespace
                content = '\n'.join(line.strip() for line in content.splitlines() if line.strip())
            
            return content
        except Exception as e:
            raise HttpServiceError(f"Failed to fetch text from {url}: {str(e)}")
    