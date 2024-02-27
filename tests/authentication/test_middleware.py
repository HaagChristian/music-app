from main import auth_validate


class MockRequest:
    def __init__(self, path, headers=None):
        self.url = MockUrl(path)
        self.headers = headers if headers else {}


class MockUrl:
    def __init__(self, path):
        self.path = path


response_object = {
    'status': 'fail',
    'message': 'Provide a valid auth token.'
}


def test_auth_validate_with_valid_token(monkeypatch):
    request = MockRequest('/id3service')
    result = auth_validate(request)
    assert result == response_object


def test_auth_validate_with_missing_token(monkeypatch):
    request = MockRequest('/id3service')
    request.headers = {"authorization": None}
    result = auth_validate(request)
    assert result == response_object


def test_auth_validate_with_invalid_token(monkeypatch):
    request = MockRequest('/id3service')
    request.headers = {"authorization": "Bearer invalid_token"}

    result = auth_validate(request)
    assert result == response_object


def test_auth_validate_with_other_paths(monkeypatch):
    paths = ['/data/search', '/data/change-metadata', '/user/me']
    for path in paths:
        request = MockRequest(path)
        result = auth_validate(request)
        assert result == response_object


def test_auth_validate_with_unknown_path(monkeypatch):
    request = MockRequest('/other/path')
    result = auth_validate(request)
    assert result is None
