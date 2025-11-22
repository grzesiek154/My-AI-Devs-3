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
        
        # Check for successful status codes (2xx range)
        if 200 <= response.status_code < 300:
            try:
                return response.json()
            except json.JSONDecodeError:
                print("Response is not JSON format")
                return response.text
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def process_api_request(url, data):
    response = post_json_to_endpoint(url, data)
    
    if response is None:
        print("Request failed")
        return False
        
    if response['code'] == 0:
        print("Operation successful", response)
        return True
    else:
        print("Operation failed:", response)
        return False
    




def get_raw_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        raw_data = response.text
        return raw_data

    else:
        print("failed to fetch the reposne", response.status_code)    
