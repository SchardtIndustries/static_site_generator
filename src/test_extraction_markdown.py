import unittest
import re
from extraction_markdown import extract_markdown_images, extract_markdown_links

import re

def extract_markdown_images(text):
    # Updated regex to capture empty alt text and URLs
    pattern = r'!\[([^\]]*)\]\((https?://[^\)]*)?\)'
    matches = []
    for match in re.finditer(pattern, text):
        alt_text = match.group(1)
        url = match.group(2) if match.group(2) else ''
        matches.append((alt_text, url))
    return matches

def extract_markdown_links(text):
    # Updated regex to capture empty link URLs if any
    pattern = r'\[([^\]]*)\]\((https?://[^\)]*)?\)'
    return [(m.group(1), m.group(2) if m.group(2) else '') for m in re.finditer(pattern, text)]

# Testing functions with updated test cases
def test_extract_markdown_images():
    text1 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    result1 = extract_markdown_images(text1)
    assert result1 == [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], f"Test 1 failed: {result1}"

    text2 = "No images here!"
    result2 = extract_markdown_images(text2)
    assert result2 == [], f"Test 2 failed: {result2}"

    # Edge case with empty alt and URL
    text3 = "Edge case ![]() with empty alt and URL"
    result3 = extract_markdown_images(text3)
    assert result3 == [("", "")], f"Test 3 failed: {result3}"

    # Multiple images with alt text
    text4 = "Multiple images: ![alt1](https://example.com/1.png) and ![alt2](https://example.com/2.png)"
    result4 = extract_markdown_images(text4)
    assert result4 == [("alt1", "https://example.com/1.png"), ("alt2", "https://example.com/2.png")], f"Test 4 failed: {result4}"

    print("All tests for extract_markdown_images passed!")

def test_extract_markdown_links():
    text1 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    result1 = extract_markdown_links(text1)
    assert result1 == [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], f"Test 1 failed: {result1}"

    text2 = "No links here!"
    result2 = extract_markdown_links(text2)
    assert result2 == [], f"Test 2 failed: {result2}"

    # Edge case with missing URL
    text3 = "Edge case [empty]() with missing URL"
    result3 = extract_markdown_links(text3)
    # Since URL is missing, it should be captured as empty string
    assert result3 == [("empty", "")], f"Test 3 failed: {result3}"

    # Multiple links with different text
    text4 = "Multiple links: [one](https://one.com), [two](https://two.com)"
    result4 = extract_markdown_links(text4)
    assert result4 == [("one", "https://one.com"), ("two", "https://two.com")], f"Test 4 failed: {result4}"

    print("All tests for extract_markdown_links passed!")

# Run the tests
test_extract_markdown_images()
test_extract_markdown_links()
