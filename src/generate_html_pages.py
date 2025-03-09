from block_markdown import markdown_to_html_node, extract_title
import os

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generateing page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as content_file:
        markdown_text = content_file.read()

    with open(template_path) as template_file:
        template_text = template_file.read()

    node = markdown_to_html_node(markdown_text)
    content_html = node.to_html()
    title = extract_title(markdown_text)

    ouput_html = template_text.replace("{{ Title }}", title).replace(
        "{{ Content }}", content_html
    ).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    des_dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_path):
        os.makedirs(des_dir_path, exist_ok=True)
    with open(dest_path, "w") as html_file:
        html_file.write(ouput_html)


def generate_pages_recursively(dir_path, template_path, dest_dir_path, basepath):

    items = os.listdir(dir_path)

    for item in items:
        item_path = os.path.join(dir_path, item)
        if os.path.basename(item).endswith('.md'):
            item_dest_path = os.path.join(dest_dir_path, item.replace('.md', ".html"))
            generate_page(item_path, template_path, item_dest_path, basepath)
        if os.path.isdir(item_path):
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            generate_pages_recursively(item_path, template_path, new_dest_dir_path, basepath)

