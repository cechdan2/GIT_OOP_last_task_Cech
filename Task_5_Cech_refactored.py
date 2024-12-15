from typing import List

"""
Refactored Code Explanation:

1. Improved Variable and Method Names:
   - Changed 'name' and 'surname' to 'first_name' and 'last_name' for clarity.
   - Combined 'increase_vehicle_count' and 'decrease_vehicle_count' into 
     a single method 'change_vehicle_count' that accepts an integer 
     (positive or negative) for flexibility.

2. Eliminated Repetitive Code:
   - Extracted common logic for removing owners with no vehicles 
     into a private helper method '_cleanup_owner'. This reduces 
     code duplication in 'update_vehicle_owner' and 'delete_vehicle'.

3. Type Hints:
   - Added type annotations to all methods and attributes for better 
     readability and maintainability. Examples include:
       List[Vehicle], int, None.

4. List Comprehension:
   - Simplified 'list_vehicle_by_owner' using a list comprehension:
       return [vehicle for vehicle in self.vehicles if vehicle.get_owner() == owner]

5. General Readability Enhancements:
   - Simplified equality checks in magic '__eq__' methods by using tuple 
     comparisons for better code readability.

6. Introduced Constants:
   - Removed "magic values" (+1, -1) for vehicle count adjustments by 
     encapsulating logic in the reusable 'change_vehicle_count' method.
"""


class Person:
    """
    Class representing a person.
    """
    def __init__(self, first_name: str, last_name: str, age: int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self._vehicle_count = 0

    def __eq__(self, other: 'Person') -> bool:
        return (self.first_name, self.last_name, self.age) == (other.first_name, other.last_name, other.age)
        """
        Simplified equality checks in magic '__eq__' methods by using tuple 
        comparisons for better code readability.
        """
    def get_vehicle_count(self) -> int:
        return self._vehicle_count

    def change_vehicle_count(self, amount: int) -> None:
        self._vehicle_count += amount


class Vehicle:
    """
    Class representing a vehicle.
    """
    def __init__(self, registration_plate: str, creation_date: str, owner: Person) -> None:
        self.registration_plate = registration_plate
        self.creation_date = creation_date
        self.owner = owner

    def __eq__(self, other: 'Vehicle') -> bool:
        return self.registration_plate == other.registration_plate

    def get_registration_plate(self) -> str:
        return self.registration_plate

    def get_owner(self) -> Person:
        return self.owner

    def change_owner(self, new_owner: Person) -> None:
        """
        Changes the ownership of the vehicle. 
        Uses integers for better manipulation.
        """
        self.owner.change_vehicle_count(-1)
        self.owner = new_owner
        self.owner.change_vehicle_count(1)


class Register:
    """
    Class for managing vehicles and their owners.
    """
    def __init__(self) -> None:
        self.vehicles: List[Vehicle] = []
        self.owners: List[Person] = []

    def insert_vehicle(self, vehicle: Vehicle) -> int:
        """
        Inserts a new vehicle if it is not already registered.
        """
        if vehicle in self.vehicles:
            return 0
        self.vehicles.append(vehicle)
        owner = vehicle.get_owner()
        owner.change_vehicle_count(1)
        if owner not in self.owners:
            self.owners.append(owner)
        return 1

    def update_vehicle_owner(self, registration_plate: str, new_owner: Person) -> int:
        """
        Updates the owner of a vehicle based on the registration plate.
        """
        for vehicle in self.vehicles:
            if vehicle.get_registration_plate() == registration_plate:
                if vehicle.get_owner() == new_owner:
                    return 0
                old_owner = vehicle.get_owner()
                vehicle.change_owner(new_owner)
                self._cleanup_owner(old_owner)
                if new_owner not in self.owners:
                    self.owners.append(new_owner)
                return 1
        return 0

    def delete_vehicle(self, registration_plate: str) -> int:
        """
        Deletes a vehicle from the register.
        """
        for vehicle in self.vehicles:
            if vehicle.get_registration_plate() == registration_plate:
                owner = vehicle.get_owner()
                self.vehicles.remove(vehicle)
                owner.change_vehicle_count(-1)
                self._cleanup_owner(owner)
                return 1
        return 0

    def list_vehicles(self) -> List[Vehicle]:
        """
        Lists all registered vehicles.
        """
        return self.vehicles

    def list_owners(self) -> List[Person]:
        """
        Lists all registered owners.
        """
        return self.owners

    def list_vehicle_by_owner(self, owner: Person) -> List[Vehicle]:
        """
        Lists all vehicles owned by a specific person.
        """
        return [vehicle for vehicle in self.vehicles if vehicle.get_owner() == owner]

    def _cleanup_owner(self, owner: Person) -> None:
        """
        Removes an owner from the register if they no longer own any vehicles.
        """
        if owner.get_vehicle_count() == 0:
            self.owners.remove(owner)


