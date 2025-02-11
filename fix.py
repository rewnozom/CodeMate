import os
import re

# Define your base project directory
BASE_DIR = "C:\\Users\\Tobia\\CodeMate\\cmate"  # Adjust as needed

# List of top-level modules that need "cmate." prefix
MODULES_TO_FIX = [
    "core", "llm", "interfaces", "storage", 
    "task_management", "utils", "validation"
]

# Regex pattern to detect absolute imports (not relative ones)
IMPORT_PATTERN = re.compile(r"^\s*(from|import)\s+(" + "|".join(MODULES_TO_FIX) + r")(\.| )")

def fix_imports_in_file(file_path):
    """Modify a Python file to prepend 'cmate.' to specified absolute imports."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    modified = False
    updated_lines = []
    
    for line in lines:
        # Skip lines that already contain "cmate."
        if "cmate." in line:
            updated_lines.append(line)
            continue

        # Skip relative imports (e.g., "from .module import X")
        if re.match(r"^\s*(from|import) +\.", line):
            updated_lines.append(line)
            continue

        # Apply the regex substitution for absolute imports
        updated_line = IMPORT_PATTERN.sub(r"\1 cmate.\2\3", line)

        if updated_line != line:
            modified = True  # Mark the file as modified

        updated_lines.append(updated_line)

    # Only overwrite the file if changes were made
    if modified:
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(updated_lines)
        print(f"Updated imports in: {file_path}")

def process_directory(directory):
    """Recursively process all Python files in a directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                fix_imports_in_file(file_path)

if __name__ == "__main__":
    process_directory(BASE_DIR)
    print("Import fixing completed!")
