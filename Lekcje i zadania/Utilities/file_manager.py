import requests
import json

def download_file(url):
    response = requests.get(url)

    if response.status_code == 200:
        with open("downloaded_file.txt", "w") as file:
            file.write(response.text)
        print("File downloaded successfully")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def get_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

if __name__ == "__main__":

    test_url = "https://example.com/test.txt"
    download_file(test_url)
