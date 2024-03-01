import os
import tempfile
from tempfile import TemporaryFile

from starlette.background import BackgroundTask
from starlette.responses import FileResponse


def create_and_return_file(file):
    """
    Create a temporary file and return it as a FileResponse.
    """
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(file.FILE_DATA)
        return FileResponse(temp_file_path,
                            background=BackgroundTask(cleanup, temp_file_path=temp_file_path, temp_file=temp_file))


def cleanup(temp_file: TemporaryFile, temp_file_path: str):
    """
    Delete tempfile after response is sent.
    """
    temp_file.close()
    os.remove(temp_file_path)  # delete the temporary file --> necessary because of the delete=False parameter
