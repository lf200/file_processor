import os
from mcp.server.fastmcp import FastMCP
from typing import List

# 创建一个 MCP 服务器实例，名称为 "file_processor"
mcp = FastMCP("file_processor")


@mcp.tool()
def read_file_content(file_path: str) -> str:
    """
    Reads and returns the content of a file.

    Args:
        file_path: The path to the file to be read.

    Returns:
        The content of the file as a string, or an error message if the file does not exist.
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' not found."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


@mcp.tool()
def write_file(file_path: str, content: str) -> str:
    """
    Writes content to a new file or overwrites an existing one.

    Args:
        file_path: The path to the file to be written.
        content: The string content to write to the file.

    Returns:
        A success message or an error message.
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote content to '{file_path}'."
    except Exception as e:
        return f"Error writing to file: {str(e)}"


@mcp.tool()
def find_text_in_file(file_path: str, search_string: str) -> List[str]:
    """
    Searches for a string in a file and returns a list of all matching lines.

    Args:
        file_path: The path to the file to be searched.
        search_string: The string to search for.

    Returns:
        A list of lines containing the search string, or an error message.
    """
    if not os.path.exists(file_path):
        return [f"Error: File '{file_path}' not found."]

    matching_lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if search_string in line:
                    matching_lines.append(line.strip())

        if not matching_lines:
            return [f"No matches found for '{search_string}' in '{file_path}'."]

        return matching_lines
    except Exception as e:
        return [f"Error searching file: {str(e)}"]


if __name__ == "__main__":
    print("File Processor MCP server started. Waiting for Cursor to connect...")
    mcp.run(transport="sse")