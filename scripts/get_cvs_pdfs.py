# %%
import os
import re
import requests
from bs4 import BeautifulSoup

import googledriver


# %%
# Open and read the HTML content
with open('../data_files/inputs/all_comments_manually_shown.html', 'r') as file:
    html_content = file.read()

# %%
# Find all matches of the regex in the HTML content
ids = re.findall(r'https://drive.google.com/file/d/(.*?)/view?', html_content)
ids

# %%
# Remove duplicates
unique_ids = []
for id in ids:
    if id not in unique_ids:
        unique_ids.append(id)
ids = unique_ids
ids

# %%
# Find all names of commenters
names = re.findall(r'<span dir="ltr"><span aria-hidden="true"><!---->(.*?)<!---->.', html_content)
names

# %%
# Removing duplicates
unique_names = []
for name in names:
    if name not in unique_names:
        unique_names.append(name)
names = unique_names
names

# %%
# Create the new list of URLs
# urls = [f'https://drive.google.com/u/0/uc?id={id_}&export=download' for id_ in ids]
urls = [f'https://drive.google.com/file/d/{id_}/view?usp=share_link' for id_ in ids]
urls

# %%
# Ensure the output directory exists
os.makedirs('../data_files/outputs/CVs', exist_ok=True)

# %%
# Download each file

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

# %%
for id_ in ids:
    print(id_)
    file_path = f'../data_files/outputs/CVs/{id_}.pdf'
    download_file_from_google_drive(id_, file_path)

# %%
