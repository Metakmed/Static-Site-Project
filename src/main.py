import os
import re
import shutil
import sys
from pathlib import Path

from final import markdown_to_html_node


def validate_paths(source: Path | str, destination: Path | str) -> None:
    source = Path(source).resolve()
    destination = Path(destination).resolve()

    if not source.exists():
        raise FileNotFoundError(f"Source does not exist: {source}")
    if source == destination:
        raise ValueError("Source and destination must be different")
    if source.is_relative_to(destination):
        raise ValueError("Source cannot be inside destination")
    if destination.is_relative_to(source):
        raise ValueError("Destination cannot be inside source")

def update_public(source: Path | str, destination: Path | str)-> None:

    if not os.path.exists(source):
        raise FileNotFoundError("File not Found")

    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    for file in os.listdir(source):
        file_path = os.path.join(source, file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, destination)

        elif os.path.isdir(file_path):
            path_to_nested_directory_destination = os.path.join(destination, file)
            update_public(file_path, path_to_nested_directory_destination)

def extract_title(markdown_content: str) -> str:
    title = re.findall(r"(^#\ .+)", markdown_content)
    if title:
        result: str = title[0].lstrip("#").strip()
        return result
    raise ValueError("No title found")


def generate_page_recursive(source_path, template_path, destination_path):
    print(f"\nGenerating a page from '{source_path}' to '{destination_path}' using '{template_path}'\n")
    split_source_path = os.path.split(source_path)
    source_dir = os.path.dirname(source_path)
    print(f"Source Directory: {source_dir}\n")

    if os.path.isdir(source_path):
        print(f"Current source path leads to a directory labeled '{split_source_path[-1]}'\n")
        print(f"Starting a search at '{split_source_path[-1]}'\n")

        for entry in os.listdir(source_path):
            print(f"Current position in search for '{source_path}' is '{entry}'\n")

            new_path = os.path.join(source_path, entry)
            print(f"Does {new_path} point to a file or a directory\n")

            if os.path.isfile(new_path):
                print(f"'{entry}' is a file\n")

                nested_destination_dir_path = os.path.join(destination_path, "index.html")
                nested_source_dir_path = os.path.join(source_path, entry)

                print(f"Updating location of destination file to {nested_destination_dir_path}\n")
                print(f"Updating location of source file to {nested_source_dir_path}\n")

                generate_page_recursive(nested_source_dir_path, template_path, nested_destination_dir_path)

            else:
                print(f"'{entry}' is a directory\n")

                nested_destination_dir_path = os.path.join(destination_path, entry)
                nested_source_dir_path = os.path.join(source_path, entry)

                print(f"Updating location of destination file to '{nested_destination_dir_path}'\n")
                print(f"Updating location of source file to '{nested_source_dir_path}'\n")

                generate_page_recursive(nested_source_dir_path, template_path, nested_destination_dir_path)

    else:
        print(f"Current source path leads to a file: {split_source_path[-1]}\n")

        destination_file = os.path.split(destination_path)

        with open(source_path) as source, open(template_path) as template:
            markdown_content = source.read()
            template_content = template.read()

        html_node = markdown_to_html_node(markdown_content)
        html_content = html_node.to_html()
        page_title = extract_title(markdown_content)
        updated_template = template_content.replace("{{ Title }}", page_title).replace("{{ Content }}", html_content).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

        if os.path.exists(destination_file[0]):
            print(f"\nThe following directories exist: '{destination_file[0]}'\n")
            with open(destination_path, "w") as destination:
                destination.write(updated_template)
                print(f"File made at {destination_path}\n\n")
        else:
            os.makedirs(destination_file[0])
            print(f"\nMaking the following directories: '{destination_file[0]}'\n")
            with open(destination_path, "w") as destination:
                destination.write(updated_template)
                print(f"File made at {destination_path}\n\n")


def main():
    project_root = Path(__file__).resolve().parent.parent
    path_to_public = project_root / "public"
    path_to_static = project_root / "static"
    validate_paths(path_to_static, path_to_public)
    update_public(path_to_static, path_to_public)
    destination_path = "docs"
    source_path = "content"
    template_path = "template.html"
    generate_page_recursive(source_path, template_path, destination_path)


if __name__ == "__main__":
    if sys.argv[1]:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    main()
