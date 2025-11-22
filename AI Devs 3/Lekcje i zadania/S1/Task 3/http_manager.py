import requests
import json

def post_json_to_endpoint(url, data, headers=None, timeout=30):
    """
    Post JSON data to a specified endpoint.
    
    Args:
        url (str): The endpoint URL
        data (dict): The JSON data to send
        headers (dict, optional): Custom headers. Defaults to None
        timeout (int, optional): Request timeout in seconds. Defaults to 30
    
    Returns:
        dict: Response from the server if successful
        None: If request fails
    """
    try:
        # Set default headers if none provided
        if headers is None:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        
        # Make the POST request
        response = requests.post(
            url=url,
            json=data,  # automatically serializes dict to JSON
            headers=headers,
            timeout=timeout
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Try to parse response as JSON
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Response is not JSON format")
            return response.text
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        print(f"Response status code: {getattr(e.response, 'status_code', 'N/A')}")
        print(f"Response text: {getattr(e.response, 'text', 'N/A')}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def process_api_request(url, data):
    response = post_json_to_endpoint(url, data)
    
    if response is None:
        print("Request failed")
        return False
        
    if 'success' in response:
        print("Operation successful")
        return True
    else:
        print("Operation failed:", response.get('error', 'Unknown error'))
        return False