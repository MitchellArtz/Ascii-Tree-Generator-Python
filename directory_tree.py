import os
import argparse
from pathlib import Path

# === In-Code Configuration ===
# Specify your default base path, include/exclude file extensions, and excluded folders here.
# These defaults will be used only when command-line arguments are NOT provided.

DEFAULT_BASE_PATH = "C:/Users/Example/Documents"  # Example default path
DEFAULT_INCLUDE = ['.py', '.txt']                # Example: Include Python and Text files
DEFAULT_EXCLUDE = None                           # Example: Exclude JPEG and PNG images (Set to None for Include-Only Mode)
DEFAULT_EXCLUDED_FOLDERS = ['pyralume-env', '.git']  # Example: Exclude these folders

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate an ASCII tree of a directory and save it as Markdown and TXT files."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Path to the directory (use quotes if path contains spaces). If not provided, uses the in-code DEFAULT_BASE_PATH.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=['include', 'exclude'],
        required=False,
        help="Operation mode: 'include' to include only specified file types, or 'exclude' to exclude specified file types.",
    )
    parser.add_argument(
        "--include",
        nargs='*',
        default=None,
        help="List of file extensions to include (e.g., .py .txt). Used only in 'include' mode.",
    )
    parser.add_argument(
        "--exclude",
        nargs='*',
        default=None,
        help="List of file extensions to exclude (e.g., .jpg .png). Used only in 'exclude' mode.",
    )
    parser.add_argument(
        "--exclude-folders",
        nargs='*',
        default=None,
        help="List of folder names to exclude from the tree (e.g., .git __pycache__).",
    )
    return parser.parse_args()

def generate_tree(root_path, mode=None, include=None, exclude=None, excluded_folders=None):
    tree_lines = []
    root_path = Path(root_path)

    if not root_path.exists():
        raise FileNotFoundError(f"The path '{root_path}' does not exist.")
    if not root_path.is_dir():
        raise NotADirectoryError(f"The path '{root_path}' is not a directory.")

    # Prepare excluded_folders for case-insensitive comparison
    excluded_folders_lower = [folder.lower() for folder in excluded_folders] if excluded_folders else []

    def add_tree(current_path, prefix=""):
        try:
            items = sorted(current_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            tree_lines.append(f"{prefix}└── [Permission Denied]")
            return
        except OSError as e:
            tree_lines.append(f"{prefix}└── [Error: {e}]")
            return

        # Filter out excluded folders (case-insensitive)
        items = [item for item in items if not (item.is_dir() and item.name.lower() in excluded_folders_lower)]

        items_count = len(items)
        for index, item in enumerate(items):
            connector = "├── " if index < items_count - 1 else "└── "
            if item.is_dir():
                tree_lines.append(f"{prefix}{connector}{item.name}/")
                new_prefix = prefix + ("│   " if index < items_count - 1 else "    ")
                add_tree(item, new_prefix)
            else:
                ext = item.suffix.lower()
                if mode == 'include':
                    # Include only specified file types
                    if include and ext not in [e.lower() for e in include]:
                        continue
                elif mode == 'exclude':
                    # Exclude specified file types
                    if exclude and ext in [e.lower() for e in exclude]:
                        continue
                # If mode is not set, include all files
                tree_lines.append(f"{prefix}{connector}{item.name}")

    tree_lines.append(f"{root_path.name}/")
    add_tree(root_path)
    return "\n".join(tree_lines)

def save_to_markdown(tree_str, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write("```\n")
            md_file.write(tree_str)
            md_file.write("\n```")
        print(f"Markdown file saved to: {output_path}")
    except Exception as e:
        print(f"Failed to save Markdown file: {e}")

def save_to_text(tree_str, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(tree_str)
        print(f"Text file saved to: {output_path}")
    except Exception as e:
        print(f"Failed to save Text file: {e}")

def main():
    args = parse_arguments()
    try:
        # Determine the base path
        if args.path:
            base_path = args.path
        else:
            base_path = DEFAULT_BASE_PATH
            if not base_path:
                raise ValueError("No path provided via command line or in-code DEFAULT_BASE_PATH.")

        # Determine the operation mode
        mode = args.mode
        if mode is None:
            # If mode is not specified via CLI, decide based on in-code defaults
            # If DEFAULT_INCLUDE is set, default to 'include' mode
            # Else if DEFAULT_EXCLUDE is set, default to 'exclude' mode
            if DEFAULT_INCLUDE:
                mode = 'include'
            elif DEFAULT_EXCLUDE:
                mode = 'exclude'
            else:
                mode = None  # No filtering

        # Validate mode and corresponding arguments
        if mode == 'include':
            include = args.include if args.include else (DEFAULT_INCLUDE if DEFAULT_INCLUDE else None)
            exclude = None  # Ignore exclude lists in include mode
        elif mode == 'exclude':
            exclude = args.exclude if args.exclude else (DEFAULT_EXCLUDE if DEFAULT_EXCLUDE else None)
            include = None  # Ignore include lists in exclude mode
        else:
            include = None
            exclude = None

        # Handle excluded folders
        if args.exclude_folders:
            excluded_folders = args.exclude_folders
        else:
            excluded_folders = DEFAULT_EXCLUDED_FOLDERS if DEFAULT_EXCLUDED_FOLDERS else []

        tree = generate_tree(base_path, mode=mode, include=include, exclude=exclude, excluded_folders=excluded_folders)
        print(tree)

        # Define the output Markdown file path in the target directory
        root = Path(base_path)
        md_filename = f"{root.name}_tree.md"
        md_path = root / md_filename
        save_to_markdown(tree, md_path)

        # Define the output TXT file path in the current working directory
        cwd = Path.cwd()
        txt_filename = f"{root.name}_tree.txt"
        txt_path = cwd / txt_filename
        save_to_text(tree, txt_path)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
