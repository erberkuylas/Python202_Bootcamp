import json
import os
from book import Book
import httpx

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

   
    def add_book(self, isbn):
        """ISBN numarasına göre kitabı OpenLibrary API'sinden alır ve kütüphaneye ekler."""
        isbn_clean = isbn.replace("-", "")
        url = f"https://openlibrary.org/isbn/{isbn_clean}.json"

        try:
            response = httpx.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            title = data.get("title", "Başlık Yok")
            authors_data = data.get("authors", [])
            authors = []

            for author in authors_data:
                key = author.get("key")
                if key:
                    try:
                        author_resp = httpx.get(f"https://openlibrary.org{key}.json", timeout=5)
                        author_resp.raise_for_status()
                        author_name = author_resp.json().get("name", "Bilinmeyen Yazar")
                        authors.append(author_name)
                    except (httpx.HTTPError, httpx.RequestError):
                        authors.append("Bilinmeyen Yazar")
                else:
                    authors.append("Bilinmeyen Yazar")

        # Eğer Book tek string author alıyorsa:
            book = Book(title, ", ".join(authors), isbn_clean)

            self.books.append(book)
            self.save_books()
            print(f"Kitap eklendi: {book}")
            return book

        except httpx.HTTPStatusError as e:
            print(f"Kitap bulunamadı (HTTP {e.response.status_code}).")
            return None
        except httpx.RequestError:
            print("Bağlantı hatası. Lütfen internetinizi kontrol edin.")
            return None
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")
            return None
            
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