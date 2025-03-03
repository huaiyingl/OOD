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


class ParkingLot:
    def __init__(self, num_regular_spots, num_large_spots):
        self.spots = self.gen_spots(num_regular_spots, num_large_spots)
        self.vehicle_to_spot = {}
    
    def park_vehicle(self, vehicle: Vehicle):
        spot_id = self.find_spot(vehicle)
        if spot_id is None:
            # Lot is full
            return None
        self.spots[spot_id].park(vehicle)
        self.vehicle_to_spot[vehicle] = spot_id
        return spot_id
    
    def find_spot(self, vehicle: Vehicle):
        pass
    
    def get_fee(self, start_time: float, end_time: float, parking_spot: ParkingSpot):
        pass

    def unpark_vehicle(self, vehicle: Vehicle):
        spot_id = self.vehicle_to_spot[vehicle]
        parking_start_time = self.spots[spot_id].unpark(vehicle)
        fee = self.get_fee(parking_start_time, time.time(), self.spots[spot_id])
        del self.vehicle_to_spot[vehicle]
        return fee
        

class ParkingSpot:
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.vehicle = None
        self.parking_start_time = None
    
    def can_park(self, vehicle: Vehicle):
        pass
        
    def park(self, vehicle: Vehicle):
        self.vehicle = vehicle
        self.parking_start_time = time.time()
    
    def unpark(self, vehicle: Vehicle):
        pass
        

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

import time
from typing import Optional
import heapq


# Vehicle base class and Car class
class Vehicle:
    def __init__(self, name, size):
        self._name = name
        self._size = size


class Car(Vehicle):
    def __init__(self, name, size):
        super().__init__(name, size)



# Parking Spot base lass and RegularSpot class
class ParkingSpot:
    def __init__(self, size, rate):
        self._size = size
        self._rate = rate
        self._is_available = True
        self._vehicle = None   
        self._parking_start_time = None 

    def can_park_vehicle(self, vehicle: Vehicle) -> bool:
        return self._is_available and self._size >= vehicle.size
    
    def park(self, vehicle: Vehicle) -> bool:
        if not self.can_park_vehicle(vehicle):
            return False
        self._is_available = False
        self._vehicle = vehicle
        self._parking_start_time = time.time()
        return True

    def unpark(self) -> float:
        """
        Unpark the vehicle and calculate the parking fee
        """
        if not self._vehicle:
            return 0.0
            
        time_spent = time.time() - self._parking_start_time
        fee = self._rate * time_spent
        
        self._is_available = True
        self._vehicle = None
        self._parking_start_time = None
        
        return fee

class RegularSpot(ParkingSpot):
    def __init__(self, size, rate):
        super().__init__(size, rate)



 
# Parking Lot System
class ParkingLot:
    def __init__(self):
        self._parking_spots = []  # list of parking spots
        self._vehicle_to_spot = {}  # vehicle -> spot

    def add_parking_spot(self, parking_spot: ParkingSpot):
        pass

    def remove_parking_spot(self, parking_spot: ParkingSpot):
        pass

    def find_optimal_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        # strategy: find the smallest available spot that can fit the vehicle
        candidate_spots = []
        for spot in self._parking_spots:
            if spot.can_park_vehicle(vehicle):
                heapq.heappush(candidate_spots, (spot.size, spot))
        if candidate_spots:
            return heapq.heappop(candidate_spots)[1]
        return None

    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        spot = self.find_optimal_spot(vehicle)
        if spot:
            if spot.park(vehicle):
                self._vehicle_to_spot[vehicle] = spot
                return spot
        return None

    def unpark_vehicle(self, vehicle: Vehicle) -> float:
        """
        Unpark the vehicle and calculate the parking fee
        """
        if vehicle not in self._vehicle_to_spot:
            return 0.0
            
        spot = self._vehicle_to_spot[vehicle]
        fee = spot.unpark()
        del self._vehicle_to_spot[vehicle]
        return fee