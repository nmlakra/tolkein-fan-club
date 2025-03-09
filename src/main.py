from generate_html_pages import generate_pages_recursively
import os
import shutil
from sys import argv

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


def main(basepath):
    static_source_path = "static"
    content_source_path = "content"
    destination_path = "docs"
    template_path = "template.html"

    if os.path.exists(destination_path):
        remove_dir_content(destination_path)

    copy_source_files_to_destination(static_source_path, destination_path)
    generate_pages_recursively(content_source_path, template_path, destination_path, basepath)


if __name__ == "__main__":
    basepath = "/"
    if len(argv) > 1:
        basepath = argv[1]
    main(basepath)
