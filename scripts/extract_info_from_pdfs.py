# %%
import shutil
import os
import json
import re

from pypdf import PdfReader

# %%
# Define a regular expression for email addresses
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# %%
# Get a list of all PDF files in the folder
pdfs_base_dir = '../data_files/outputs/CVs'
pdf_files = [os.path.join(pdfs_base_dir, f) for f in os.listdir(pdfs_base_dir) if f.endswith('.pdf')]
pdf_files = sorted(pdf_files)
pdf_files

# Create a new directory for the renamed files
outputs_base_dir = '../data_files/outputs'
new_dir = os.path.join(outputs_base_dir, 'CVs_with_names')
os.makedirs(new_dir, exist_ok=True)

# %%
results = []
broken_pdfs = []

# For each PDF file
for i, pdf_file in enumerate(pdf_files):
    print(pdf_file)
    pdf_id = pdf_file.split('/')[-1].split('.')[0]

    # Open the file and create a PdfFileReader object
    with open(pdf_file, 'rb') as file:
        try:
            reader = PdfReader(file)
            # Extract the text from the first page
            text = reader.pages[0].extract_text()
        except Exception as e:
            print("can't read pdf file:\n", pdf_file)
            print("will skip it\n")
            broken_pdfs.append(pdf_file)
            continue

    # Use the regular expression to find the email address
    email = re.search(email_regex, text)
    email = email.group() if email else ''
    
    try:
        # Assume the first and last names are the first two words
        first_name, last_name = text.split()[:2]
    except Exception as e:
        print('cant get names for id:\n', pdf_id)
        print('so will replace with numbers')
        first_name, last_name = i, i
        # continue

    # Get new PDF name and replace characters that are not allowed in Windows filenames
    new_name = f"{first_name}_{last_name}_{email}_cv.pdf"
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        new_name = new_name.replace(char, '')

    # Store the results in a dictionary
    result = {
        'pdf_id': pdf_id,
        'new_pdf_name': f"{first_name}_{last_name}_{email}_cv.pdf",
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    }
    results.append(result)
    print(result)
    
    # Copy the file to a new location with the new name
    new_path = os.path.join(new_dir, new_name)
    shutil.copy2(pdf_file, new_path)
    print('will save to:', new_path)
    print()

# %%
# Write the results to a JSON file
with open(os.path.join(outputs_base_dir, "results.json"), 'w') as file:
    json.dump(results, file)

# %%
# save broken_pdfs list to txt file
# side note: these are files which couldn't be properly downloaded 
# as the google drive link wasn't set to public
with open(os.path.join(outputs_base_dir, "broken_pdfs.txt"), 'w') as file:
    for pdf in broken_pdfs:
        file.write(pdf)
        file.write('\n')

# %%