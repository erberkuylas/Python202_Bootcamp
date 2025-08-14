from book import Book
from library import Library

def main():
    library = Library()

    while True:
        print("\n=== Kütüphane Menüsü ===")
        print("1. Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        secim = input("Seçiminizi girin: ")

        if secim == "1":
            title = input("Kitap adı: ")
            author = input("Yazar adı: ")
            isbn = input("ISBN numarası (13 haneli, sadece rakam): ")
            try:
                book = Book(title, author, isbn)
                library.add_book(book)
                print("Kitap başarıyla eklendi.")
            except ValueError as e:
                print(f"Hata: {e}")

        elif secim == "2":
            isbn = input("Silmek istediğiniz kitabın ISBN numarası: ")
            try:
                library.remove_book(isbn)
                print("Kitap silindi.")
            except ValueError as e:
                print(f"Hata: {e}")

        elif secim == "3":
            print("\nKütüphanedeki Kitaplar:")
            print(library.list_books())

        elif secim == "4":
            isbn = input("Aramak istediğiniz kitabın ISBN numarası: ")
            try:
                book = library.find_book(isbn)
                print(f"Bulundu: {book}")
            except ValueError as e:
                print(f"Hata: {e}")

        elif secim == "5":
            print("Çıkış yapılıyor...")
            break

        else:
            print("Geçersiz seçim. Lütfen 1-5 arası bir değer girin.")

if __name__ == "__main__":
    main()
