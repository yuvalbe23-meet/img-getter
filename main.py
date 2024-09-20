import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# Define the search term and number of images to download
search_query = "grizzly bear"
num_images = 50
folder_name = "grizzly_bear_images"

# Create the folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Function to get image URLs from Bing search
def get_bing_image_urls(query, num_images):
    search_url = f"https://www.bing.com/images/search?q={query}&form=HDRSC2&first=1&tsc=ImageBasicHover"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(search_url, headers=headers)
    
    # Parse the HTML page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find image elements
    images = soup.find_all('a', class_='iusc', limit=num_images)
    
    # Extract image URLs
    image_urls = []
    for img in images:
        m = img.get('m')
        if m:
            # Extract the image URL from the 'm' attribute which contains JSON data
            img_url = eval(m)['murl']  # 'murl' contains the image URL
            if img_url.startswith('http'):
                image_urls.append(img_url)
    
    return image_urls

# Function to download images
def download_image(url, folder, img_num):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        img = Image.open(BytesIO(response.content))
        img.save(os.path.join(folder, f"grizzly_bear_{img_num}.png"))
        print(f"Downloaded: grizzly_bear_{img_num}.png")
    except Exception as e:
        print(f"Error downloading image {img_num}: {e}")

# Scrape image URLs from Bing
image_urls = get_bing_image_urls(search_query, num_images)

# Download the images
for i, url in enumerate(image_urls):
    download_image(url, folder_name, i + 1)
