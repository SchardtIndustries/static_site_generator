import os
from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Starting recursive page generation from '{dir_path_content}' to '{dest_dir_path}' using template '{template_path}'")
    
    for root, dirs, files in os.walk(dir_path_content):
        # Determine relative path from the content root
        rel_path = os.path.relpath(root, dir_path_content)
        target_dir = os.path.join(dest_dir_path, rel_path)

        # Create the target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)

        for filename in files:
            if filename.endswith('.md'):
                source_md_path = os.path.join(root, filename)
                # Change extension to .html
                dest_html_filename = os.path.splitext(filename)[0] + '.html'
                dest_html_path = os.path.join(target_dir, dest_html_filename)

                # Generate page
                generate_page(source_md_path, template_path, dest_html_path)

# Example usage:
# generate_pages_recursive('static', 'template.html', 'public')
