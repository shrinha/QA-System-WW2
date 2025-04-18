import requests
import time
import os
import re
from bs4 import BeautifulSoup

# Set up output directory
output_dir = 'wiki_sections'
os.makedirs(output_dir, exist_ok=True)

# First request to get section list
section_response = requests.get(
    'https://en.wikipedia.org/w/api.php',
    params={
        'action': 'parse',
        'page': 'World War II',
        'format': 'json',
        'prop': 'sections'
    }
).json()

sections = section_response['parse']['sections']

# Fetch and save each section's content
for sec in sections:
    try:
        # Get section text
        text_response = requests.get(
            'https://en.wikipedia.org/w/api.php',
            params={
                'action': 'parse',
                'page': 'World War II',
                'section': sec['index'],
                'format': 'json',
                'prop': 'text'
            }
        ).json()
        
        # Extract and clean HTML content
        html_content = text_response['parse']['text']['*']
        soup = BeautifulSoup(html_content, 'html.parser')
        clean_text = soup.get_text(separator='\n').strip()
        
        # Create safe filename
        filename = re.sub(r'[\\/*?"<>|:]', '', sec['line']) + '.txt'
        filepath = os.path.join(output_dir, filename)
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(clean_text)
            
        print(f"Saved: {filename}")
        time.sleep(0.5)  # Be kind to Wikipedia's servers
        
    except Exception as e:
        print(f"Error processing section {sec['index']}: {str(e)}")
