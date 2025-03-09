from block_markdown import markdown_to_html_node, extract_title
import os
import shutil


def generate_page(from_path, template_path, dest_path):
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
    )

    with open(dest_path, "w") as html_file:
        html_file.write(ouput_html)


def remove_dir_content(dir_path):
    if os.path.exists(dir_path):
        dir_items = os.listdir(dir_path)
        for item in dir_items:
            item_path = os.path.join(dir_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            else:
                remove_dir_content(item_path)
                os.removedirs(item_path)

        print(f"Cleand {dir_path}!")
    else:
        print(f"{dir_path} doesn't exist!")


def copy_source_files_to_destination(src_path, dst_path):

    os.makedirs(dst_path, exist_ok=True)

    dir_items = os.listdir(src_path)
    for item in dir_items:
        item_src_path = os.path.join(src_path, item)
        item_dst_path = os.path.join(dst_path, item)
        if os.path.isfile(item_src_path):
            print(f"Moving {item_src_path} -> {item_dst_path}")
            shutil.copy2(item_src_path, item_dst_path)
        else:
            copy_source_files_to_destination(item_src_path, item_dst_path)


def copy_static_to_public():
    source_path = "./static"
    destination_path = "./public"

    if os.path.exists(destination_path):
        remove_dir_content(destination_path)

    copy_source_files_to_destination(source_path, destination_path)


def main():
    copy_static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
