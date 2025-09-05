def extract_title(markdown):
    # Split the markdown into lines
    lines = markdown.strip().splitlines()
    
    for line in lines:
        # Check if the line starts with a single '#' followed by a space
        if line.startswith('# '):
            # Return the header text after removing '#' and whitespace
            return line[2:].strip()
    # If no h1 header found, raise an exception
    raise ValueError("No H1 header (# ...) found in the markdown.")
