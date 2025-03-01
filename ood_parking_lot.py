"""
Problem: Design a parking lot system

Requirements:
1. A fixed number of parking spots available for different types of vehicles
2. Tracks parking spot availability
3. Charged according to the time the vehicle has been parked in the parking lot
4. Assigns parking spot to vehicles smartly

Follow-Up:

Reference: 
https://github.com/careercup/CtCI-6th-Edition-Python/blob/master/chapter_07/p04_parking_lot.py
https://stackoverflow.com/questions/764933/amazon-interview-question-design-an-oo-parking-lot
https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles/getting-ready-parking-lot

"""

"""
objects:
- vehicle -> Car, Bike, Bus
- parking spot -> Regular Spot/ Large Spot
- parking lot system: manages all
- assign spot strategy 

workflow:
system:
- assign spot to vehicle
- keep track of spot-vehicle mapping
- park and unpark vehicle
- calculate parking fee

vehicle:
- park
- unpark
- pay 
"""

from abc import ABC, abstractmethod

# Vehicle Interface
class Vehicle(ABC):
    def __init__(self, name, size):
        self._name = name
        self._size = size

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size

class Car(Vehicle):
    def __init__(self, name, size):
        super().__init__(name, size)

class Bike(Vehicle):
    def __init__(self, name, size):
        super().__init__(name, size)

class Truck(Vehicle):
    def __init__(self, name, size):
        super().__init__(name, size)



# Parking Spot Interface
class ParkingSpot(ABC):
    def __init__(self, size, rate, location):
        self._size = size
        self._rate = rate
        self._location = location
        self._is_available = True       

    @property
    def size(self):
        return self._size
    
    @property
    def rate(self):
        return self._rate

    @property
    def is_available(self):
        return self._is_available
    
    @property
    def location(self):
        return self._location
    
    def occupy(self):
        self._is_available = False

    def release(self):
        self._is_available = True

    def can_fit_vehicle(self, vehicle):
        return self._size >= vehicle.size
    

class RegularSpot(ParkingSpot):
    def __init__(self, size, rate):
        super().__init__(size, rate)

    
# Strategy Interface
class AssignSpotStrategy(ABC):
    @abstractmethod
    def assign_spot(self, vehicle, parking_spots, ticket) -> ParkingSpot:
        pass

class NearestSpotStrategy(AssignSpotStrategy):
    def assign_spot(self, vehicle, parking_spots, ticket) -> ParkingSpot: 
        # find the nearest spot
        entry_location = ticket.entry_location
        min_distance = float('inf')
        nearest_spot = None
        for spot in parking_spots:
            distance = abs(spot.location - entry_location)
            if distance < min_distance:
                min_distance = distance
                nearest_spot = spot
        return nearest_spot
        

# Ticket for handling mapping between vehicle and parking spot, entry and exit time
class Ticket:
    def __init__(self, vehicle, parking_spot, entry_time, entry_location):
        self._vehicle = vehicle
        self._parking_spot = parking_spot
        self._entry_time = entry_time
        self._exit_time = None
        self._entry_location = entry_location

    @property
    def vehicle(self):
        return self._vehicle
    
    @property
    def parking_spot(self):
        return self._parking_spot
    
    @property
    def entry_time(self):
        return self._entry_time
    
    @property
    def exit_time(self):
        return self._exit_time
    
    @property
    def entry_location(self):
        return self._entry_location
    
    @exit_time.setter
    def exit_time(self, time):
        self._exit_time = time

    def calculate_parking_fee(self):
        hours = self._exit_time - self._entry_time
        return self._parking_spot.rate * hours  

 
# Parking Lot System
class ParkingLotSystem:
    def __init__(self, parking_spots, assign_spot_strategy):
        self._parking_spots = parking_spots # list of parking spots
        self._assign_spot_strategy = assign_spot_strategy
        self._tickets = [] # list of tickets
        self._vehicle_to_ticket = {} # vehicle -> ticket

    def add_parking_spot(self, parking_spot):
        pass

    def remove_parking_spot(self, parking_spot):
        pass

    def park_vehicle(self, vehicle, time):
        # find a spot for the vehicle
        candidate_spots = []
        for spot in self._parking_spots:
            if spot.is_available and spot.can_fit_vehicle(vehicle):
                candidate_spots.append(spot)

        if not candidate_spots:
            return None
        
        # create a ticket
        ticket = Ticket(vehicle, spot, time)
        self._tickets.append(ticket)
        self._vehicle_to_ticket[vehicle] = ticket
        
        # assign the spot to the vehicle
        spot = self._assign_spot_strategy.assign_spot(vehicle, candidate_spots, ticket)
        spot.occupy()     

    def unpark_vehicle(self, vehicle, time):
        ticket = self._vehicle_to_ticket[vehicle]
        ticket.exit_time = time
        # release the spot
        ticket.parking_spot.release()
        del self._vehicle_to_ticket[vehicle]

    def calculate_parking_fee(self, ticket):
        return ticket.calculate_parking_fee()





