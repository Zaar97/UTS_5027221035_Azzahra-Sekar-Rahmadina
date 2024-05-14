import grpc
import sys
# Adjust the import paths to where your generated Python gRPC files are located
import bookStore_pb2
import bookStore_pb2_grpc

def create_book(stub):
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    description = input("Enter book description: ")
    price = float(input("Enter book price: "))
    discount = int(input("Enter book discount: "))

    book = bookStore_pb2.Book(
        title=title,
        author=author,
        description=description,
        price=price,
        disc=discount
    )
    response = stub.AddBook(book)
    print("AddBook Response:", response.responseMsg)

def get_all_books(stub):
    all_books = stub.GetAllBooks(bookStore_pb2.Empty())
    print("GetAllBooks Response:")
    for book in all_books.books:
        print(f"Title: {book.title}, Author: {book.author}, Description: {book.description}, Price: {book.price}, Discount: {book.disc}")

def get_book(stub):
    book_id = input("Enter book ID: ")
    book = stub.GetBookByID(bookStore_pb2.BookID(id=book_id))
    print("GetBookByID Response:")
    print(f"Title: {book.title}, Author: {book.author}, Description: {book.description}, Price: {book.price}, Discount: {book.disc}")

def update_book(stub):
    book_id = input("Enter book ID to update: ")
    title = input("Enter updated book title: ")
    author = input("Enter updated book author: ")
    description = input("Enter updated book description: ")
    price = float(input("Enter updated book price: "))
    discount = int(input("Enter updated book discount: "))

    book = bookStore_pb2.Book(
        title=title,
        author=author,
        description=description,
        price=price,
        disc=discount
    )
    book_with_id = bookStore_pb2.BookWithID(
        bookId=bookStore_pb2.BookID(id=book_id),
        book=book
    )
    response = stub.UpdateBook(book_with_id)
    print("UpdateBook Response:", response.responseMsg)

def delete_book(stub):
    book_id = input("Enter book ID to delete: ")
    response = stub.DeleteBook(bookStore_pb2.BookID(id=book_id))
    print("DeleteBook Response:", response.responseMsg)

def run():
    channel = grpc.insecure_channel('localhost:5007')
    stub = bookStore_pb2_grpc.BookStoreServiceStub(channel)

    while True:
        print("\n1. Add Book\n2. Get All Books\n3. Get Book\n4. Update Book\n5. Delete Book\n6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_book(stub)
        elif choice == '2':
            get_all_books(stub)
        elif choice == '3':
            get_book(stub)
        elif choice == '4':
            update_book(stub)
        elif choice == '5':
            delete_book(stub)
        elif choice == '6':
            break
        else:
            print("Invalid choice! Please enter a valid option.")

if __name__ == '__main__':
    run()
