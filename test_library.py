import pytest
from library import Library
import httpx

# --------------------------
# test_add_book_success
# --------------------------
def test_add_book_success(monkeypatch, tmp_path):
    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self._json_data = json_data
            self.status_code = status_code
        def json(self):
            return self._json_data
        def raise_for_status(self):
            if self.status_code != 200:
                raise httpx.HTTPStatusError("HTTP Error", request=None, response=self)

    def mock_get(url, timeout=5):
        if "isbn" in url:
            return MockResponse({
                "title": "Test Book",
                "authors": [{"key": "/authors/OL12345A"}]
            })
        elif "/authors/" in url:
            return MockResponse({"name": "Test Author"})
        return MockResponse({}, 404)

    monkeypatch.setattr("httpx.get", mock_get)

    libfile = tmp_path / "test_library.json"
    lib = Library(filename=str(libfile))
    # Library'nin kabul edeceği geçerli ISBN
    result = lib.add_book("9780385472579")  # 13 haneli ISBN
    assert result is not None
    assert len(lib.books) == 1
    assert lib.books[0].title == "Test Book"
    assert lib.books[0].author == "Test Author"  # Burayı düzelttik

# --------------------------
# test_add_book_not_found
# --------------------------
def test_add_book_not_found(monkeypatch, tmp_path):
    class MockResponse:
        def __init__(self, status_code=404):
            self.status_code = status_code
        def json(self):
            return {}
        def raise_for_status(self):
            if self.status_code != 200:
                raise httpx.HTTPStatusError("Not Found", request=None, response=self)

    def mock_get(url, timeout=5):
        return MockResponse(404)

    monkeypatch.setattr("httpx.get", mock_get)

    libfile = tmp_path / "test_library.json"
    lib = Library(filename=str(libfile))
    result = lib.add_book("9780451526538")  # 13 haneli ISBN
    assert result is None
    assert len(lib.books) == 0

# --------------------------
# test_add_book_api_error
# --------------------------
def test_add_book_api_error(monkeypatch, tmp_path):
    def mock_get(url, timeout=5):
        raise httpx.RequestError("Bağlantı hatası", request=None)

    monkeypatch.setattr("httpx.get", mock_get)

    libfile = tmp_path / "test_library.json"
    lib = Library(filename=str(libfile))
    result = lib.add_book("9780451526538")  # 13 haneli ISBN
    assert result is None
    assert len(lib.books) == 0
