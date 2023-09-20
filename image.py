import requests
from bs4 import BeautifulSoup

def fetch_image_url(query):
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    for img_tag in soup.find_all("img"):
        if 'gif' not in str(img_tag):
            img_url = img_tag.get("src")
            if img_url:
                return img_url
    return None