from tempfile import TemporaryFile
import os


def cleanup(temp_file: TemporaryFile, temp_file_path: str):
    """Delete tempfile after response is sent."""

    temp_file.close()
    os.remove(temp_file_path)  # delete the temporary file --> necessary because of the delete=False parameter