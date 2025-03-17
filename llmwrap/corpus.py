import requests

def get_image(url, path):
    response = requests.get(url)

    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download image. Status code: {response.status_code}")