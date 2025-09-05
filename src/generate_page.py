import os
from markdown_to_html import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown content
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Read template content
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Convert markdown to HTML node
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract title from markdown
    try:
        title = extract_title(markdown_content)
    except ValueError:
        title = "Untitled"

    # Replace placeholders in template
    filled_content = template_content.replace("{{ Title }}", title)
    filled_content = filled_content.replace("{{ Content }}", html_content)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write filled content to destination path
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(filled_content)

    print(f"Page generated at {dest_path}")
