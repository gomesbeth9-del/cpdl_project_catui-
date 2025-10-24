import os
import json
import re

def generate_music_data():
    """
    Scans the 'musicas' directory to find all PDF files, parses their
    title and author from the parent directory's name, and generates
    a JavaScript file with all the music data.
    """
    music_data = []
    root_dir = 'musicas'
    
    # Regex to parse "Title (Author)" format from directory names.
    dir_pattern = re.compile(r'^(.*) \((.*)\)$')

    if not os.path.isdir(root_dir):
        print(f"Error: Directory '{root_dir}' not found.")
        return

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                parent_dir_name = os.path.basename(dirpath)
                
                # Default values if parsing fails
                title = parent_dir_name
                author = "Unknown"

                match = dir_pattern.match(parent_dir_name)
                if match:
                    title = match.group(1).strip()
                    author = match.group(2).strip()

                # Create a relative path that works on the web
                full_path = os.path.join(dirpath, filename).replace(os.sep, '/')
                
                music_entry = {
                    "path": full_path,
                    "title": title,
                    "author": author,
                    "version": filename
                }
                music_data.append(music_entry)

    # Sort the data for consistent output
    music_data.sort(key=lambda x: (x['title'], x['author'], x['version']))

    # Write the data to a JavaScript file
    output_filename = 'music_data.js'
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write('const musicData = ')
        json.dump(music_data, f, ensure_ascii=False, indent=4)
        f.write(';')
    
    print(f"'{output_filename}' generated successfully with {len(music_data)} PDF entries.")

if __name__ == '__main__':
    generate_music_data()
