import tempfile

from fastapi import UploadFile

from src.database.musicDB.db_crud import update_file_and_metadata


def get_file_bytes(file: UploadFile) -> bytes:
    # get file bytes
    file.file.seek(0)
    file_data = file.file.read()

    return file_data


def file_helper_with_temp_file(db, res, metadata_db, filename):
    file_content = res.content
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(file_content)
        temp_file.seek(0)
        upload_file = UploadFile(temp_file, filename=filename)
        update_file_and_metadata(db=db, file=get_file_bytes(file=upload_file), metadata=metadata_db)
