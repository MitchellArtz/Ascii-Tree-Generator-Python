# ASCII Tree Generator
## Table of Contents

- [ASCII Tree Generator](#ascii-tree-generator)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command-Line Interface](#command-line-interface)
      - [**Basic Command:**](#basic-command)
      - [**Include Mode:**](#include-mode)
      - [**Exclude Mode:**](#exclude-mode)
      - [**Help Menu:**](#help-menu)
    - [In-Code Configuration](#in-code-configuration)
  - [Examples](#examples)
    - [Include Mode](#include-mode-1)
    - [Exclude Mode](#exclude-mode-1)
  - [Output Files](#output-files)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues and Solutions](#common-issues-and-solutions)
  - [License](#license)

## Overview

**ASCII Tree Generator** is a versatile Python tool that generates an ASCII representation of your directory structure. It allows you to **include or exclude specific file types** and **exclude entire folders** from the tree. The tool can be configured either through command-line arguments or by setting parameters directly within the code. Additionally, it saves the generated tree as both a Markdown (`.md`) file in the target directory and a plain text (`.txt`) file in the current working directory.

This tool is perfect for:

- **Documentation:** Easily document your project structure.
- **Visualization:** Quickly visualize complex directory hierarchies.
- **Sharing:** Share directory structures with collaborators in a readable format.

## Features

- **Command-Line Interface:** Generate directory trees directly from the terminal with customizable options.
- **In-Code Configuration:** Define default settings within the script for ease of use without command-line arguments.
- **Mutually Exclusive Modes:** Operate in either **Include-Only** mode or **Exclude-Only** mode to streamline filtering.
- **Excluded Folders:** Specify folders to exclude entirely from the tree.
- **Dual Output:** Save the directory tree as both Markdown (`.md`) and plain text (`.txt`) files.
- **Cross-Platform Compatibility:** Works seamlessly on Windows, macOS, and Linux.
- **Error Handling:** Gracefully handles permission issues and invalid paths.

## Prerequisites

- **Python 3.6 or higher** is required.
- The script utilizes only Python's standard library modules (`os`, `argparse`, `pathlib`), so no additional installations are necessary.

## Installation

1. **Clone the Repository:**
2. **Navigate to the Directory:**
3. **(Optional) Set Up a Virtual Environment:**

## Usage

You can use the ASCII Tree Generator either via the command-line interface (CLI) or by configuring parameters directly within the code.

### Command-Line Interface

Run the script with various arguments to customize its behavior.

#### **Basic Command:**

Generate a directory tree without any filters.

```bash
python directory_tree.py --path "C:/Users/Example/Documents"
```

#### **Include Mode:**

Only include files with specified extensions.

```bash
python directory_tree.py --path "C:/Users/Example/Documents" --mode include --include .py .txt --exclude-folders pyralume-env .git
```

#### **Exclude Mode:**

Exclude files with specified extensions.

```bash
python directory_tree.py --path "C:/Users/Example/Documents" --mode exclude --exclude .jpg .png --exclude-folders pyralume-env .git
```

#### **Help Menu:**

Display all available options.

```bash
python directory_tree.py --help
```

### In-Code Configuration

Set default parameters directly within the script for ease of use without command-line arguments.

1. **Open `directory_tree.py` in a Text Editor.**

2. **Configure Defaults:**

   ```python
   # === In-Code Configuration ===
   # Specify your default base path, include/exclude file extensions, and excluded folders here.
   # These defaults will be used only when command-line arguments are NOT provided.

   DEFAULT_BASE_PATH = "C:/Users/Example/Documents"  # Example default path
   DEFAULT_INCLUDE = ['.py', '.txt']                # Example: Include Python and Text files
   DEFAULT_EXCLUDE = None                           # Set to a list like ['.jpg', '.png'] for Exclude Mode
   DEFAULT_EXCLUDED_FOLDERS = ['pyralume-env', '.git']  # Example: Exclude these folders
   ```

3. **Run the Script:**

   ```bash
   python directory_tree.py
   ```

   The script will use the in-code defaults you have set.

## Examples

### Include Mode

**Command:**

```bash
python directory_tree.py --path "C:/Users/Example/Documents" --mode include --include .py .txt --exclude-folders pyralume-env .git
```

**Description:**

- **Path:** `C:/Users/Example/Documents`
- **Mode:** Include only `.py` and `.txt` files.
- **Excluded Folders:** `pyralume-env` and `.git`

**Output:**

```
Documents/
├── Project/
│   ├── main.py
│   ├── utils.py
│   └── README.md
└── notes.txt
```

### Exclude Mode

**Command:**

```bash
python directory_tree.py --path "C:/Users/Example/Documents" --mode exclude --exclude .jpg .png --exclude-folders pyralume-env .git
```

**Description:**

- **Path:** `C:/Users/Example/Documents`
- **Mode:** Exclude `.jpg` and `.png` files.
- **Excluded Folders:** `pyralume-env` and `.git`

**Output:**

```
Documents/
├── Project/
│   ├── main.py
│   ├── utils.py
│   └── README.md
└── notes.txt
```

## Output Files

Upon execution, the script generates two output files:

1. **Markdown (`.md`) File:**

   - **Location:** Saved in the **target directory** specified by the `--path` argument or `DEFAULT_BASE_PATH`.
   - **Naming Convention:** `<directory_name>_tree.md`
   - **Content:** The directory tree enclosed within triple backticks for Markdown formatting.

   **Example (`Documents_tree.md`):**

   ```markdown
   ```
   Documents/
   ├── Project/
   │   ├── main.py
   │   ├── utils.py
   │   └── README.md
   └── notes.txt
   ```
   ```

2. **Text (`.txt`) File:**

   - **Location:** Saved in the **current working directory** where the script is executed.
   - **Naming Convention:** `<directory_name>_tree.txt`
   - **Content:** The plain ASCII directory tree.

   **Example (`Documents_tree.txt`):**

   ```
   Documents/
   ├── Project/
   │   ├── main.py
   │   ├── utils.py
   │   └── README.md
   └── notes.txt
   ```

## Troubleshooting

### Common Issues and Solutions

1. **Permission Errors:**

   - **Error Message:**
     ```
     Error: [WinError 1920] The file cannot be accessed by the system: 'E:\\example\\example-py\\example-env\uf00d\\bin\\python'
     ```

   - **Cause:** The script is attempting to access a path with invalid or inaccessible files, possibly due to Unicode escape issues or corrupted virtual environments.

   - **Solutions:**
     - **Case-Insensitive Exclusion:**
       - Ensure that excluded folder names are compared in a case-insensitive manner within the script.
     - **Verify Folder Names:**
       - Inspect the directory to ensure there are no hidden or special characters in folder names.
       - **Run with Elevated Permissions:**
       - On Windows, run Command Prompt or PowerShell as an administrator.

2. **Path Not Found Errors:**

   - **Error Message:**
     ```
     Error: The path 'C:/Invalid/Path' does not exist.
     ```

   - **Solution:**
     - Verify that the provided `--path` or `DEFAULT_BASE_PATH` exists and is correct.
     - Use absolute paths to avoid ambiguity.

3. **Invalid File Extensions:**

   - **Issue:** File extensions in include/exclude lists not starting with a dot.

   - **Solution:**
     - Ensure all file extensions start with a dot (`.`), e.g., `.py` instead of `py`.

4. **Unicode or Special Character Issues:**

   - **Issue:** Folder or file names containing invalid or special Unicode characters causing parsing errors.

   - **Solution:**
     - Rename folders or files to remove special characters.
     - Ensure your system's locale settings support the characters used.

5. **Script Execution Errors:**

   - **Issue:** Syntax errors or incompatible Python versions.

   - **Solution:**
     - Double-check the script for any typographical errors.
     - Ensure you are using Python 3.6 or higher.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software as per the terms of the license.