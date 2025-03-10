"""
Problem Statement
Design a book reservation system that allows users to reserve books and search for books in a library's inventory.

Requirements
1. The system should allow users to reserve books
2. The system should allow users to search for books
3. The system should handle cases where multiple users want to reserve the same book with limited inventory

Follow-up Questions
1. How would you handle a scenario where 3 users want to reserve the same book, but there are only 2 copies in inventory?
2. How would you extend the system to handle different types of resources beyond books (e.g., CDs, movies)?
3. How would you improve the architecture by:
   - Abstracting resources into a common class
   - Adding a manager class to handle business logic
   - Making the Library class serve as an interface layer

"""
from typing import Optional
from collections import deque
class Resource:
    def __init__(self, title, resource_id, quantity=1):
        self.title = title
        self.resource_id = resource_id
        self.quantity = quantity
        self.reserved_count = 0
        self.waiting_queue = deque()
        
    def reserve(self, user):
        if self.reserved_count < self.quantity:
            self.reserved_count += 1
            return True
        else:
            self.waiting_queue.append(user)
            return False
    
    def release(self, user) -> Optional[User]:
        if self.reserved_count > 0:
            self.reserved_count -= 1
            
            if self.waiting_queue:
                next_user = self.waiting_queue.popleft()
                self.reserved_count += 1
                return next_user
        return None
    
    def is_available(self):
        return self.reserved_count < self.quantity
    


# Specific resource types inherit from Resource
class Book(Resource):
    def __init__(self, title, author, isbn, quantity=1):
        super().__init__(title, isbn, quantity)
        self.author = author
        self.isbn = self.resource_id

class CD(Resource):
    pass

class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.reserved_resources = []



# New ResourceManager class to handle business logic
class ResourceManager:
    def __init__(self):
        self.resources = []
        self.users = []
    
    def add_resource(self, resource):
        self.resources.append(resource)
        return True
    
    def add_user(self, user):
        self.users.append(user)
        return True
    
    def get_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    
    def search_resource(self, resource_id):
        for resource in self.resources:
            if resource.resource_id == resource_id:
                return resource
        return None
    
    def reserve_resource(self, resource_id, user_id):
        resource = self.search_resource(resource_id)
        user = self.get_user(user_id)
        
        if not resource or not user:
            return False
        
        if resource.reserve(user):
            user.reserved_resources.append(resource)
            return True
        else:
            return False
    
    def release_resource(self, resource_id, user_id):
        resource = self.search_resource(resource_id)
        user = self.get_user(user_id)
        
        if not resource or not user or resource not in user.reserved_resources:
            return False
        
        user.reserved_resources.remove(resource)
        next_user = resource.release(user)

        if next_user:
            next_user.reserved_resources.append(resource)
        return True


# Library class as interface layer(Facade Pattern, Encapsulation)
class Library:
    def __init__(self):
        self.manager = ResourceManager()
    
    # Resource management interfaces
    def add_resource(self, resource):
        return self.manager.add_resource(resource)
    
    def add_user(self, user):
        return self.manager.add_user(user)
    
    # Search interfaces
    def search_resource(self, resource_id):
        return self.manager.search_resource(resource_id)
    
    # Reservation interfaces
    def reserve_resource(self, resource_id, user_id):
        return self.manager.reserve_resource(resource_id, user_id)
    
    def release_resource(self, resource_id, user_id):
        return self.manager.release_resource(resource_id, user_id)
        