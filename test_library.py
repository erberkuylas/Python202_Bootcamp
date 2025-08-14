import json
import pytest
from library import Library
from book import Book

@pytest.fixture(autouse=True)
def clear_json():
    """Her testten önce library.json dosyasını temizler."""
    with open("library.json", "w", encoding="utf-8") as f:
        json.dump([], f)

def test_add_book():
    lib = Library()
    book = Book("Test Kitap", "Yazar", "9783161484100")  # 13 haneli ISBN
    result = lib.add_book(book)
    assert result == "Kitap eklendi."
    assert len(lib.books) == 1

def test_remove_book():
    lib = Library()
    book = Book("Test Kitap", "Yazar", "9783161484100")  # 13 haneli ISBN
    lib.add_book(book)
    result = lib.remove_book("9783161484100")
    assert result == "Kitap silindi."
    assert len(lib.books) == 0

def test_list_books_empty():
    lib = Library()
    assert lib.list_books() == "Kütüphane boş."

def test_list_books_with_items():
    lib = Library()
    book = Book("Test Kitap", "Yazar", "9783161484101")  # 13 haneli, farklı ISBN
    lib.add_book(book)
    output = lib.list_books()
    assert "Test Kitap" in output
