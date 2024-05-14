from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sys
sys.path.append('../')
import grpc
import os
import bookStore_pb2
import bookStore_pb2_grpc

app = Flask(__name__)
CORS(app)

grpc_channel = grpc.insecure_channel('localhost:5007')
grpc_stub = bookStore_pb2_grpc.BookStoreServiceStub(grpc_channel)

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/src/'))
app.template_folder = template_dir

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/addBook", methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        data = request.json
        book_request = bookStore_pb2.Book(
            id=data['id'],
            title=data['title'],
            author=data['author'],
            description=data['description'],
            price=data['price'],
            disc=data['disc']
        )
        response = grpc_stub.AddBook(book_request)
        return jsonify({"message": response.responseMsg})

@app.route("/allBooks")
def get_all_books():
    response = grpc_stub.GetAllBooks(bookStore_pb2.Empty())
    book_list = [{"id": book.id, "title": book.title, "author": book.author, "description": book.description, "price": book.price, "disc": book.disc} for book in response.books]
    return jsonify({"books": book_list})

@app.route("/book/<book_id>")
def get_book(book_id):
    response = grpc_stub.GetBookByID(bookStore_pb2.BookID(id=book_id))
    if response.title:
        book_data = {"id": response.id, "title": response.title, "author": response.author, "description": response.description, "price": response.price, "disc": response.disc}
        return jsonify(book_data)
    else:
        return jsonify({"message": "Book not found"}), 404
    
@app.route("/updateBook/<book_id>", methods=['PUT'])
def update_book(book_id):
    data = request.json
    book_request = bookStore_pb2.BookWithID(
        bookId=bookStore_pb2.BookID(id=book_id),
        book=bookStore_pb2.Book(
            id=book_id,
            title=data['title'],
            author=data['author'],
            description=data['description'],
            price=data['price'],
            disc=data['disc']
        )
    )
    response = grpc_stub.UpdateBook(book_request)
    return jsonify({"message": response.responseMsg})

@app.route("/deleteBook/<book_id>", methods=['DELETE'])
def delete_book(book_id):
    response = grpc_stub.DeleteBook(bookStore_pb2.BookID(id=book_id))
    return jsonify({"message": response.responseMsg})

if __name__ == '__main__':
    app.run(debug=True)
