"""
Problem: Design a Library Management System

Requirements:
support below features:
- Borrow Book
- Return Book

Reference:
https://leetcode.com/discuss/interview-question/485566/amazon-onsite-ood-design-library-book-management-system
https://leetcode.com/discuss/interview-question/object-oriented-design/1333797/Design-a-Library-Management-System

objects:
- Book
- Member
- Library

Library is the central coordinator of all operations
Book only manages its internal state
Member is primarily a data container

workflows:
- user borrow book
- user return book

Follow up:
- book reservation?


"""

from enum import Enum

class BookStatus(Enum):
    AVAILABLE = 1
    BORROWED = 0
    RESERVED = -1
    

class Book:
    def __init__(self, title, author, book_id):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._status = BookStatus.AVAILABLE
        self._current_borrower = None

    def mark_borrowed(self, borrower):
        """Mark book as borrowed."""
        self._current_borrower = borrower
        self._status = BookStatus.BORROWED
        
    def mark_returned(self):
        """Mark book as returned."""
        self._current_borrower = None
        self._status = BookStatus.AVAILABLE
        
    @property
    def status(self):
        return self._status
        
    @property
    def current_borrower(self):
        return self._current_borrower
        

class Member:
    def __init__(self, name):
        self._name = name
        self._member_id = None
        self._borrowed_books = []

    def register(self, member_id):
        """Register this member with an ID."""
        self._member_id = member_id

    def add_book(self, book):
        self._borrowed_books.append(book)
        
    def remove_book(self, book):
        if book in self._borrowed_books:
            self._borrowed_books.remove(book)
            return True
        return False

    def list_books(self):
        return self._borrowed_books


class Library:
    def __init__(self):
        self._books = []
        self._members = []
        self._next_book_id = 1
        
    def add_book(self, title, author):
        book = Book(title, author, self._next_book_id)
        self._books.append(book)
        self._next_book_id += 1
        return book
    
    def remove_book(self, book_id):
        for book in self._books[:]:
            if book._book_id == book_id:
                self._books.remove(book)
                return True
        return False

    def get_available_books(self):
        return [book for book in self._books if book.status == BookStatus.AVAILABLE]
    
    def register_member(self, name):
        """Register a new member with the library."""
        member = Member(name)
        member_id = self._generate_member_id()
        member.register(member_id)
        self._members.append(member)
        return member

    def _generate_member_id(self):
        return len(self._members) + 1
    
    def borrow_book(self, member, book):
        """Process a book borrowing request from a member."""
        if member not in self._members or book not in self._books:
            return False
            
        if book.status == BookStatus.AVAILABLE:
            member.add_book(book)
            book.mark_borrowed(member)
            return True
        return False

    def return_book(self, member, book):
        """Process a book return from a member."""
        if member not in self._members or book not in self._books:
            return False
            
        if book.status == BookStatus.BORROWED and book.current_borrower == member:
            member.remove_book(book)
            book.mark_returned()
            return True
        return False