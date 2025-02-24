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
"""

import random
import string

## Follow up: what if we can store multiple packages in a locker?
## Follow up: what's the optimal locker?
## Follow up: what if we want to set up a notificaiton system?

# Locker: represents an individual locker
class Locker:
    def __init__(self, locker_id, locker_size):
        self.locker_id = locker_id
        self.locker_size = locker_size
        self.is_occupied = False
        self.package = None # start with: 1 locker 1 package
    
    def occupy(self, package_id):
        self.is_occupied = True
        self.package_id = package_id

    def release(self):
        self.is_occupied = False
        self.package = None


# Package: represents a package to be placed in a locker
class Package:
    def __init__(self, package_id, package_size):
        self.package_id = package_id
        self.package_size = package_size
        self.locker = None
        self.pickup_code = None


# LockerManager: manages all lockers, handles locker allocation and release
class LockerManager:
    def __init__(self):
        self.lockers = []
        self.packages = {} # package_id -> package

    def add_locker(self, locker):
        self.lockers.append(locker) # expand the system

    def remove_locker(self, locker):
        self.lockers.remove(locker) # shrink the system

    def find_optimal_locker(self, package_size):
        for locker in self.lockers:
            if not locker.is_occupied and locker.locker_size >= package_size:
                return locker
        return None
    
    def allocate_locker(self, package):
        optimal_locker = self.find_optimal_locker(package.package_size)
        if optimal_locker:
            # set locker as occupied
            optimal_locker.occupy(package.package_id)
            # set package as having a locker
            package.locker = optimal_locker
            # generate a pickup code
            package.pickup_code = self.generate_code()
            # update the match in system
            self.packages[package.package_id] = package
            # return the allocated locker and the code
            return package.pickup_code, optimal_locker.locker_id           
        return None
    
    def release_locker(self, locker_id):
        for locker in self.lockers:
            if locker.locker_id == locker_id:
                locker.release()
                return True
        return False

    def generate_code(self):
        # generate a random code
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        

# UserInterface: handles user interaction for picking up packages
class UserInterface:
    def __init__(self, locker_manager):
        self.locker_manager = locker_manager

    def pickup_package(self, code):
        # iterate through all packages
        for package in self.locker_manager.packages.values():
            if package.pickup_code == code:
                locker_id = package.locker.locker_id
                self.locker_manager.release_locker(locker_id)
                print(f"Package {package.package_id} picked up from locker {locker_id}")
                return True
        print(f"Invalid code: {code}")
        return False

# DeliveryInterface: handles delivery personnel interaction for placing packages
class DeliveryInterface:
    def __init__(self, locker_manager):
        self.locker_manager = locker_manager

    def place_package(self, package):
        # find and allocate an optimal locker
        response = self.locker_manager.find_optimal_locker(package.package_size)
        if response:
            code, locker_id = response
            print(f"Package {package.package_id} placed in locker {locker_id}. Pickup Code: {code}")
            return True
        print("No Available Locker")
        return False
        

