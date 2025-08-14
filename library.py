import json
import os
from book import Book

class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        """JSON dosyasından kitapları yükler."""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = [Book(**item) for item in data]
        else:
            self.books = []

    def save_books(self):
        """Kitap listesini JSON dosyasına kaydeder."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([book.__dict__ for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, book: Book):
        if any(b.isbn == book.isbn for b in self.books):
            raise ValueError(f"ISBN {book.isbn} zaten mevcut!")
        self.books.append(book)
        self.save_books()
        return "Kitap eklendi."
    def remove_book(self, isbn):
        isbn_clean = isbn.replace("-", "")
        for book in self.books:
            if book.isbn == isbn_clean:
             self.books.remove(book)
             self.save_books()
             return "Kitap silindi."
        return "Kitap bulunamadı."

    def list_books(self) -> str:
        if not self.books:
            return "Kütüphane boş."
        return "\n".join(str(book) for book in self.books)

    def find_book(self, isbn: str) -> Book:
        for book in self.books:
            if book.isbn == isbn:
                return book
        raise ValueError(f"ISBN {isbn} numaralı kitap bulunamadı.")
