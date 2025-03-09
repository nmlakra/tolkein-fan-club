import os
from block_markdown import markdown_to_html_node, extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generateing page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as content_file:
        markdown_text = content_file.read()

    with open(template_path) as template_file:
        template_text = template_file.read()

    node = markdown_to_html_node(markdown_text)
    content_html = node.to_html()
    title = extract_title(markdown_text)

    template_text.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    dest_dir_path = dest_path.split("/")[:-1]
    os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_dir_path, "w") as html_file:
        html_file.write(template_text)
