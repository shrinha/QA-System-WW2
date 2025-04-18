import os
import re

def clear_brackets_in_file(filepath):
    try:
        # Pattern to match square brackets and any text inside them (including nested)
        bracket_pattern = re.compile(r'\[[^][]*(?:\[[^][]*]+\][^][]*)*\]')
        
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove all instances of [] and text inside
        cleaned_content = bracket_pattern.sub('', content)
        
        # Find the position of first '^' and remove everything from there to end
        caret_pos = cleaned_content.find('^')
        if caret_pos != -1:
            cleaned_content = cleaned_content[:caret_pos]

        # Clean up whitespace and format as proper paragraph
        cleaned_content = re.sub(r'\n+', ' ', cleaned_content)  # Replace newlines with spaces
        cleaned_content = re.sub(r'\s{2,}', ' ', cleaned_content)  # Remove multiple spaces
        cleaned_content = cleaned_content.strip()  # Trim leading/trailing spaces

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)
            
        return True
    
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        return False

# Process all .txt files in wiki_sections directory
wiki_dir = './wiki_sections'

if not os.path.exists(wiki_dir):
    print(f"Error: Directory '{wiki_dir}' not found. Please create it first.")
else:
    processed_count = 0
    for filename in os.listdir(wiki_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(wiki_dir, filename)
            if clear_brackets_in_file(file_path):
                print(f"Processed: {filename}")
                processed_count += 1
                
    print(f"\nProcessing complete. {processed_count} files cleaned.")
