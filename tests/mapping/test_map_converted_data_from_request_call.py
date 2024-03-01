import base64
from unittest import mock
from src.service.mapping.map_data import map_converted_data_from_request_call
from src.api.myapi.music_db_models import ConversionResponse

file_type = "audio/mp3"
file_content = b"hello world"
encoded_file_data = base64.b64encode(file_content).decode('utf-8')


def test_map_converted_data_from_request_call():

    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "file_type": file_type,
        "file_data": encoded_file_data
    }

    result = map_converted_data_from_request_call(mock_response)

    assert (result, ConversionResponse)
    assert (result.file_type, file_type)
    assert (result.file_data, file_content)
