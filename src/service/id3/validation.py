import magic
from fastapi import UploadFile

from src.api.middleware.custom_exceptions.WrongFileType import WrongFileType
from src.settings.error_messages import WRONG_MME_TYPE


def check_input_file(file: UploadFile):
    # read magic number from file and specify the mime type due to security reasons
    # the content type could be set to mpeg, but the file could be a different type
    file_content_buffer = file.file.read(2048)
    file.file.seek(0)
    mime_type = magic.from_buffer(file_content_buffer, mime=True)

    if file.content_type != "audio/mpeg" or mime_type != "audio/mpeg":
        raise WrongFileType(WRONG_MME_TYPE)
