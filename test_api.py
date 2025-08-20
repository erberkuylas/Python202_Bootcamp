from fastapi.testclient import TestClient
from api import app
from unittest.mock import patch

client = TestClient(app)

def mock_add_book(self, isbn_value):
    class MockBook:
        def __init__(self, isbn):
            self.title = "Test Book"
            self.author = "Test Author"
            self.isbn = isbn
    book = MockBook(isbn_value)
    self.books.append(book)
    return book

def mock_remove_book(self, isbn_value):
    return True  # Silme her zaman başarılı

@patch("library.Library.add_book", new=mock_add_book)
@patch("library.Library.remove_book", new=mock_remove_book)
def test_add_and_delete_book():
    isbn_data = {"isbn": "9780385472579"}

    # POST testi
    response = client.post("/books", json=isbn_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"

    # DELETE testi
    response = client.delete(f"/books/{isbn_data['isbn']}")
    assert response.status_code == 200
    json_data = response.json()
    assert "detail" in json_data
    assert json_data["detail"] == f"{isbn_data['isbn']} numaralı kitap silindi."
