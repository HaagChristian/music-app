from src.api.middleware.custom_exceptions.WrongFileType import WrongFileType
from src.service.id3.validation import check_input_file
from src.settings.error_messages import WRONG_MME_TYPE
from tests.resources.audio_files import VALID_MP3_FILE, JPEG_FILE

""" Test if the input file is a valid audio file """


def test_valid_file(create_upload_file):
    upload_file = create_upload_file(filename='valid_file.mp3', content=VALID_MP3_FILE)
    assert check_input_file(file=upload_file) is None


def test_invalid_file(create_upload_file):
    upload_file = create_upload_file(filename='invalid_file.jpeg', content=JPEG_FILE)
    try:
        res = check_input_file(file=upload_file)
        print(res)
    except WrongFileType as e:
        assert type(e) == WrongFileType
        assert e.args[0] == WRONG_MME_TYPE
