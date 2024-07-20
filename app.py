import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# Function to scrape NFT images
def scrape_nft_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = [img['src'] for img in soup.find_all('img') if 'nft' in img.get('alt', '').lower()]
    return images

# Function to create a derivative image
def create_derivative(image_url, modification):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    # Example modification: convert to grayscale
    if modification == 'grayscale':
        img = img.convert('L')
    # Save and return the image
    return img

# Streamlit UI
st.title('NFT Image Scraper and Derivative Creator')

url = st.text_input('Enter NFT collection URL')
if url:
    images = scrape_nft_images(url)
    if images:
        st.write(f'Found {len(images)} images.')
        selected_image = st.selectbox('Select an image to modify', images)
        modification = st.selectbox('Select a modification', ['grayscale', 'other'])
        if st.button('Create Derivative Image'):
            derivative_image = create_derivative(selected_image, modification)
            st.image(derivative_image, caption='Derivative Image')
