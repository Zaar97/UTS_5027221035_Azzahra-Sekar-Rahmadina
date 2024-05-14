import grpc
import sys
sys.path.append('../')
import logging
from concurrent import futures
import pymongo
import bookStore_pb2
import bookStore_pb2_grpc

class BookStoreService(bookStore_pb2_grpc.BookStoreServiceServicer):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["bookStorePackage"]
        self.collection = self.db["BookList"]
        logging.info("Connected to MongoDB")

    def AddBook(self, request, context):
        logging.info("Received AddBook request: %s", request)
        book_data = {
            "id": request.id,
            "title": request.title,
            "author": request.author,
            "description": request.description,
            "price": request.price,
            "disc": request.disc
        }
        self.collection.insert_one(book_data)
        return bookStore_pb2.Response(responseMsg="Book added successfully")

    def GetAllBooks(self, request, context):
        logging.info("Received GetAllBooks request")
        book_list = []
        for book_data in self.collection.find():
            book = bookStore_pb2.Book(
                id=book_data["id"],
                title=book_data["title"],
                author=book_data["author"],
                description=book_data["description"],
                price=book_data["price"],
                disc=book_data["disc"]
            )
            book_list.append(book)
        return bookStore_pb2.Books(books=book_list)

    def GetBookByID(self, request, context):
        logging.info("Received GetBookByID request for book ID: %s", request.id)
        book_data = self.collection.find_one({"id": request.id})
        if book_data:
            book = bookStore_pb2.Book(
                id=book_data["id"],
                title=book_data["title"],
                author=book_data["author"],
                description=book_data["description"],
                price=book_data["price"],
                disc=book_data["disc"]
            )
            return book
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Book not found")
            return bookStore_pb2.Book()
        
    def UpdateBook(self, request, context):
        logging.info("Received UpdateBook request for book ID: %s", request.bookId.id)
        book_data = self.collection.find_one({"id": request.bookId.id})
        if book_data:
            updated_book_data = {
                "id": request.book.id,
                "title": request.book.title,
                "author": request.book.author,
                "description": request.book.description,
                "price": request.book.price,
                "disc": request.book.disc
            }
            self.collection.update_one({"id": request.bookId.id}, {"$set": updated_book_data})
            return bookStore_pb2.Response(responseMsg="Book updated successfully")
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Book not found")
            return bookStore_pb2.Response(responseMsg="Book not found")

    def DeleteBook(self, request, context):
        logging.info("Received DeleteBook request for book ID: %s", request.id)
        result = self.collection.delete_one({"id": request.id})
        if result.deleted_count > 0:
            return bookStore_pb2.Response(responseMsg="Book deleted successfully")
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Book not found")
            return bookStore_pb2.Response(responseMsg="Book not found")

def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookStore_pb2_grpc.add_BookStoreServiceServicer_to_server(BookStoreService(), server)
    server.add_insecure_port('[::]:5007')
    server.start()
    logging.info("Listening on port 5007")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
