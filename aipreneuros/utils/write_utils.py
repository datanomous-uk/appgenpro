import json
import os

from pathlib import Path
from pydantic import BaseModel

from aipreneuros.utils import logger

def save_document(document_class: BaseModel, filename:str, project_dir:Path) -> str:
    docs_dir = project_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    prd_path = docs_dir / filename
    content = doc2md(document_class)
    prd_path.write_text(content)
    return str(prd_path)
    
def doc2md(document_class: BaseModel) -> str:
    rsp_json = json.loads(document_class.model_dump_json())
    content = json_to_markdown(rsp_json)
    return content

def save_code(code:str, filename:str, project_dir:Path):
    if code is None or filename is None:
        error_msg = f"The code to be saved is not provided for filename: {filename}: {code}"
        logger.warning(error_msg)
        return
        # raise AssertionError(error_msg)
    project_dir.mkdir(parents=True, exist_ok=True)
    filepath = project_dir / filename
    file_dir = os.path.dirname(filepath)
    os.makedirs(file_dir, exist_ok=True)
    filepath.write_text(code)


def json_to_markdown(data, depth=2):
    """
    Convert a JSON object to Markdown with headings for keys and lists for arrays, supporting nested objects.
    Source: https://github.com/geekan/MetaGPT/blob/main/metagpt/utils/json_to_markdown.py

    Args:
        data: JSON object (dictionary) or value.
        depth (int): Current depth level for Markdown headings.

    Returns:
        str: Markdown representation of the JSON data.
    """
    markdown = ""

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                # Handle JSON arrays
                markdown += "#" * depth + f" {key}\n\n"
                items = [str(item) for item in value]
                markdown += "- " + "\n- ".join(items) + "\n\n"
            elif isinstance(value, dict):
                # Handle nested JSON objects
                markdown += "#" * depth + f" {key}\n\n"
                markdown += json_to_markdown(value, depth + 1)
            elif key == "Title":
                markdown += f"# {value}\n\n"
            else:
                # Handle other values
                markdown += "#" * depth + f" {key}\n\n{value}\n\n"
    else:
        # Handle non-dictionary JSON data
        markdown = str(data)

    return markdown