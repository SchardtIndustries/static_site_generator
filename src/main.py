from textnode import TextType, TextNode
from recursive_copy import copy_dir_clean
from generate_recursive import generate_pages_recursive

def main():
    copy_dir_clean("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
