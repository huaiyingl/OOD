"""
reference: https://leetcode.com/discuss/interview-question/system-design/233869/Design-Amazon-Locker-system

Problem Statement:
Designing an Amazon Locker system involves multiple components, including user interaction for package pickup, delivery personnel interaction for package drop-off, and an optimal locker allocation mechanism. 
Here’s a breakdown of the requirements and a high-level design for each component:

Requirements Analysis:
- User Interaction:
    - Users should receive a code to open a locker.
    - Users should be able to open the locker using the code and pick up their package.
- Delivery Personnel Interaction:
    - Delivery personnel should be able to find an optimal locker for a package.
    - Delivery personnel should be able to place the package in the locker and mark it as occupied.

High-Level Design
Components
- Locker System:
    - Manages all lockers, their statuses (occupied/free), and packages.
- User Interface:
    - For users to enter the code and open the locker.
    - For delivery personnel to find and allocate lockers.
- Backend System:
    - Manages locker allocation, code generation, and validation.
- Database:
    - Stores locker information, package details, user codes, and statuses.

This design covers the basic functionalities of the Amazon Locker system, including optimal locker allocation, code-based package pickup, and management of locker states. 
It can be extended further by adding more features such as notifications, detailed access control, and a more complex locker size management system.


Design Pattern:
- Factory Pattern:
    - Used to find the optimal locker 
- Singleton Pattern:
    - Used to manage the locker manager as a singleton

"""

import random
import string

## Follow up: what if we can store multiple packages in a locker?
## Follow up: what's the optimal locker strategy?
## Follow up: what if we want to set up a notificaiton system?
## Quesitions: pass in object or id?
## Question: How to handle errors and print messages?

# Locker: represents an individual locker
class Locker:
    def __init__(self, locker_id, locker_size):
        self.locker_id = locker_id
        self.locker_size = locker_size
        self.is_occupied = False
        self.package_id = None 

    def occupy(self, package_id):
        if self.is_occupied:
            return False
        self.is_occupied = True
        self.package_id = package_id
        return True

    def release(self):
        if not self.is_occupied:
            return False
        self.is_occupied = False
        self.package_id = None
        return True


# Package: represents a package to be placed in a locker
class Package:
    def __init__(self, package_id, package_size):
        self.package_id = package_id
        self.package_size = package_size
        self.locker_id = None
        self.pickup_code = None


# LockerManager: manages all lockers, handles locker allocation and release
class LockerManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LockerManager, cls).__new__(cls)
            cls._instance.lockers = {} # locker_id -> locker
            cls._instance.packages = {} # package_id -> package
        return cls._instance
    
    def add_locker(self, locker):
        pass

    def remove_locker(self, locker):
        pass
    

    # TODO: core logic, might be extended to include more criteria
    def find_optimal_locker(self, package):
        candidates = []
        for locker in self.lockers:
            if not locker.is_occupied and locker.locker_size >= package.package_size:
                candidates.append(locker)
        if not candidates:
            return None
        return min(candidates, key = lambda x: x.locker_size - package.package_size)

    
    # TODO: core logic
    def allocate_locker(self, package):
        if package.package_id in self.packages:
            return None

        optimal_locker = self.find_optimal_locker(package)
        if optimal_locker is None:
            return None
        
        optimal_locker.occupy(package.package_id) 
        package.locker_id = optimal_locker.locker_id
        package.pickup_code = self.generate_code()
        self.packages[package.package_id] = package

        return package.pickup_code, optimal_locker.locker_id
    
    # TODO: core logic
    def release_locker(self, pickup_code):
        for package_id, package in self.packages.items():
            if package.pickup_code == pickup_code:
                locker = self.lockers[package.locker_id]
                locker.release()
                del self.packages[package_id]
                return True, package_id, package.locker_id
        return False, None, None

    def generate_code(self):
        # generate a random code for each package
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        

# UserInterface: handles user interaction for picking up packages
class UserInterface:
    def __init__(self, locker_manager):
        self.locker_manager = locker_manager

    def pickup_package(self, pickup_code):
        result, package_id, locker_id = self.locker_manager.release_locker(pickup_code)
        if result:
            return True
        else:
            return False
        

# DeliveryInterface: handles delivery personnel interaction for placing packages
class DeliveryInterface:
    def __init__(self, locker_manager):
        self.locker_manager = locker_manager

    def place_package(self, package):
        # allocate locker for a package
        result = self.locker_manager.allocate_locker(package)
        if result:
            pickup_code, locker_id = result
            return True, pickup_code, locker_id
        else:
            return False, None, None
        

