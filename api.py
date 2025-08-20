from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from library import Library

app = FastAPI()
library = Library(filename="library.json")  # veriyi json dosyasında saklayacağız

# Pydantic modelleri
class ISBNRequest(BaseModel):
    isbn: str

class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str

# GET /books
@app.get("/books", response_model=list[BookResponse])
def get_books():
    return [BookResponse(title=b.title, author=b.author, isbn=b.isbn) for b in library.books]

# POST /books
@app.post("/books", response_model=BookResponse)
def add_book(request: ISBNRequest):
    result = library.add_book(request.isbn)
    if result is None:
        raise HTTPException(status_code=400, detail=f"Kitap eklenemedi: {request.isbn}")
    return BookResponse(title=result.title, author=result.author, isbn=result.isbn)

# DELETE /books/{isbn}
@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    success = library.remove_book(isbn)
    if not success:
        raise HTTPException(status_code=404, detail=f"Kitap bulunamadı: {isbn}")
    return {"detail": f"{isbn} numaralı kitap silindi."}

