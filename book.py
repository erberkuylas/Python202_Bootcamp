class Book:
    def __init__(self, title: str, author: str, isbn: str) -> None:
        isbn_clean = isbn.replace("-", "")  # Tireleri kaldır
        if not self.is_valid_isbn(isbn_clean):
            raise ValueError(f"Geçersiz ISBN: {isbn}")
        self.title = title
        self.author = author
        self.isbn = isbn_clean

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

    @staticmethod
    def is_valid_isbn(isbn: str) -> bool:
        return isbn.isdigit() and len(isbn) == 13

    @staticmethod
    def format_isbn(isbn: str) -> str:
        isbn_clean = isbn.replace("-", "")
        return f"{isbn_clean[0:3]}-{isbn_clean[3]}-{isbn_clean[4:7]}-{isbn_clean[7:12]}-{isbn_clean[12]}"
