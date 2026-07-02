"""
File Manager Utilities
"""

from pathlib import Path
import pandas as pd


def create_directory(directory_path):
    """
    Create directory if it does not exist.
    """
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def file_exists(file_path):
    """
    Check whether a file exists.
    """
    return Path(file_path).exists()


def read_csv(file_path):
    """
    Read CSV file and return DataFrame.
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def write_csv(df, file_path):
    """
    Save DataFrame to CSV.
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path, index=False)
        print(f"File saved successfully: {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")


def get_file_size(file_path):
    """
    Get file size in bytes.
    """
    try:
        return Path(file_path).stat().st_size
    except Exception:
        return 0


def list_files(directory_path):
    """
    List all files in a directory.
    """
    try:
        return [file.name for file in Path(directory_path).iterdir() if file.is_file()]
    except Exception:
        return []


def delete_file(file_path):
    """
    Delete a file if it exists.
    """
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")
