import shutil
import os
import sys

from config import WORKING_DIR
from common import markdown_to_html_node, extract_title


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    dirs = os.listdir(dir_path_content)

    print(f"current file in dir {dir_path_content}: {dirs}")

    for f in dirs:
        if os.path.isfile(os.path.join(dir_path_content, f)):
            if f.endswith(".md"):
                html_file_name = f[0:len(f) - 3] + ".html"
                generate_page(os.path.join(dir_path_content, f), template_path, os.path.join(
                    dest_dir_path, html_file_name), base_path)
        if os.path.isdir(os.path.join(dir_path_content, f)):
            generate_page_recursive(os.path.join(
                dir_path_content, f), template_path, os.path.join(dest_dir_path, f), base_path)


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {
          dest_path} using {template_path}")
    from_content = None
    template_content = None

    with open(from_path) as f:
        from_content = f.read()

    with open(template_path) as f:
        template_content = f.read()

    html = markdown_to_html_node(from_content)
    content = html.to_html()
    content = content.replace("href=\"/", f"href=\"{base_path}")
    content = content.replace("src=\"/", f"src=\"{base_path}")
    title = extract_title(from_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ CSS }}", base_path + "index.css")
    template_content = template_content.replace(
        "{{ Content }}", content)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path.replace(
            os.path.basename(dest_path), ""), exist_ok=True)

    with open(dest_path, mode="w") as f:
        f.write(template_content)


def handle_delete_error():
    print("failed to delete destination dir")
    os.exit(1)


def main():
    base_path = None

    if len(sys.argv) == 2:
        base_path = sys.argv[1]
    else:
        base_path = "/"

    dist = os.path.join(WORKING_DIR, "docs")
    src = os.path.join(WORKING_DIR, "static")

    print(f"dist is {dist}")
    print(f"src is {src}")

    if not os.path.exists(src):
        print("cannot find static directory")
        sys.exit(1)

    if os.path.exists(dist):
        print(f"found path: {dist}")
        print(f"started to delete contents of {dist}")
        shutil.rmtree(path=dist, ignore_errors=False,
                      onerror=handle_delete_error)

    print(f"making empty dir: {dist}")
    os.mkdir(dist)
    print(f"started copying from {src} to {dist}")
    shutil.copytree(src, dist, dirs_exist_ok=True)
    print("finished copying contents")

    content_path_dir = os.path.join(WORKING_DIR, "content/")
    template_path = os.path.join(WORKING_DIR, "template.html")
    output_path_dir = os.path.join(WORKING_DIR, "docs/")

    generate_page_recursive(content_path_dir, template_path, output_path_dir, base_path)


if __name__ == "__main__":
    main()
