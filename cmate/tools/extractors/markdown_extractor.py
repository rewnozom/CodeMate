# /src/extractors/markdown_extractor.py
import os
import re
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def create_markdown_report(file_paths: list, extract_dir: str) -> (str, str):
    """
    Generate a Markdown report for the given file paths.
    Returns a tuple: (markdown_content, table_of_contents).
    """
    toc = "# Table of Contents\n\n"
    markdown_content = "# Project Report\n\n"
    file_lines_info = {}
    line_counter = markdown_content.count("\n") + 1

    for file_path in file_paths:
        relative_path = os.path.relpath(file_path, extract_dir)
        toc += f"- [{relative_path}](#{relative_path.replace(' ', '-').replace('.', '')})\n"
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            file_extension = Path(file_path).suffix.lstrip('.')
            start_line = line_counter
            line_counter += content.count("\n") + 5
            end_line = line_counter - 1
            file_lines_info[relative_path] = (start_line, end_line)
            markdown_content += f"## File: {relative_path}\n\n```{file_extension}\n{content}\n```\n\n"
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            continue

    toc_content = toc + "\n"
    logger.debug("Markdown report generated.")
    return markdown_content, toc_content
