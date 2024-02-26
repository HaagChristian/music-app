import magic
from fastapi import UploadFile

from src.api.middleware.custom_exceptions.WrongFileType import WrongFileType
from src.settings.error_messages import WRONG_MME_TYPE


def check_input_file(file: UploadFile):
    """
        Read magic number from file and specify the mime type due to security reasons
        The content type could be set to mpeg, but the file could be a different type
    """

    accepted_mime_types = ["audio/mpeg", "audio/mp3", "application/octet-stream"]  # octet stream is a fallback
    file_content_buffer = file.file.read(2048)
    file.file.seek(0)
    mime_type = magic.from_buffer(file_content_buffer, mime=True)

    if file.content_type not in accepted_mime_types or mime_type not in accepted_mime_types:
        raise WrongFileType(WRONG_MME_TYPE)
