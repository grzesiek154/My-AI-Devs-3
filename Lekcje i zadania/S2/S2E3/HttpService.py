import httpx
import json

class HttpService:
    def __init__(self, default_headers=None, timeout=30):
        """
        Initialize the HttpService with optional default headers and timeout.
        
        :param default_headers: Default headers for requests
        :param timeout: Default timeout for requests
        """
        self.default_headers = default_headers or {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.timeout = timeout

    async def post_json_to_endpoint(self, url, data, headers=None):
        """
        Post JSON data to a specified endpoint asynchronously.
        
        :param url: The endpoint URL
        :param data: The JSON data to send
        :param headers: Custom headers. Defaults to None
        :return: Response from the server if successful, None if request fails
        """
        headers = headers or self.default_headers
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()  # Raise an error for bad responses
                try:
                    return response.json()
                except json.JSONDecodeError:
                    print("Response is not JSON format")
                    return response.text
            except httpx.HTTPStatusError as e:
                print(f"Request failed with status code: {e.response.status_code}")
                return None
            except httpx.RequestError as e:
                print(f"Request failed: {str(e)}")
                return None

    async def process_api_request(self, url, data):
        response = await self.post_json_to_endpoint(url, data)
        
        if response is None:
            print("Request failed")
            return False
        
        # Check if the response is a dictionary (JSON)
        if isinstance(response, dict):
            if response.get('code') == 0:
                print("Operation successful", response)
                return True
            else:
                print("Operation failed:", response)
                return False
        else:
            # Handle non-JSON response
            print("Received non-JSON response:", response)
            return False

    async def get_raw_data(self, url):
        """
        Get raw data from a specified URL asynchronously.
        
        :param url: The URL to fetch data from
        :return: Raw data as text if successful, None otherwise
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                response.encoding = 'utf-8'
                try:
                    # Try to parse as JSON first
                    return json.loads(response.text)
                except json.JSONDecodeError:
                    # If not JSON, return raw text
                    return response.text
            except httpx.HTTPStatusError as e:
                print(f"Failed to fetch the response: {e.response.status_code}")
                return None
            except httpx.RequestError as e:
                print(f"Request failed: {str(e)}")
                return None
    