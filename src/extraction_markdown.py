import re


def extract_markdown_images(text):
    pattern = r'!\[([^\]]*)\]\((https?://[^\)]+)?\)'
    matches = []
    for match in re.finditer(pattern, text):
        alt_text = match.group(1)
        url = match.group(2) if match.group(2) else ''
        matches.append((alt_text, url))
    return matches


def extract_markdown_links(text):
    pattern = r'\[([^\]]*)\]\((https?://[^\)]+)?\)'
    return [(m.group(1), m.group(2) if m.group(2) else '') for m in re.finditer(pattern, text)]

