import requests
import json
import os


def download_file(url):
    response = requests.get(url)

    if response.status_code == 200:
        with open("downloaded_file.txt", "w") as file:
            file.write(response.text)
        print("File downloaded successfully")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def write_json_to_file(data, filename,overwrite=False):
    try:
        if os.path.exists(filename) and not overwrite:       
            print(f"File {filename} already exists")
            return False
        
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
            print(f"File {filename} written successfully")
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def get_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            print(f"File {file_path} loaded successfully")
            # print(type(file))
            # print(type(json.load(file)))
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found")
        return None
    except json.JSONDecodeError:
        print(f"File {file_path} is not a valid JSON")
        return None


if __name__ == "__main__":

    get_json_file("downloaded_file.txt")
