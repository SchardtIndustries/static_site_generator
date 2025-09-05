import unittest
from extract_title import extract_title

def test_extract_title():
    # Test 1: Basic H1 header
    md1 = "# Hello"
    result1 = extract_title(md1)
    assert result1 == "Hello", f"Expected 'Hello', got '{result1}'"

    # Test 2: Header with leading/trailing spaces
    md2 = "  #   Welcome to the site   "
    result2 = extract_title(md2)
    assert result2 == "Welcome to the site", f"Expected 'Welcome to the site', got '{result2}'"

    # Test 3: Multiple lines, header among other text
    md3 = """
    Some intro text
    
    # My Title
    
    More text
    """
    result3 = extract_title(md3)
    assert result3 == "My Title", f"Expected 'My Title', got '{result3}'"

    # Test 4: No header - should raise ValueError
    md4 = "This markdown has no header"
    try:
        extract_title(md4)
        assert False, "Expected ValueError for missing header"
    except ValueError as e:
        assert str(e) == "No H1 header (# ...) found in the markdown."

    # Test 5: Header not starting with '# ' (e.g., '##' or '#')
    md5 = "## Subheader\n# Actual Header"
    result5 = extract_title(md5)
    assert result5 == "Actual Header", f"Expected 'Actual Header', got '{result5}'"

    print("All tests passed!")

# Run the tests
test_extract_title()
