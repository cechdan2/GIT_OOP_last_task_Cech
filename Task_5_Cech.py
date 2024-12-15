from typing import List
"""
    vvvv      YOUR SOLUTION      vvvv
"""


class Person:

    def __init__(self, name: str, surname: str, age: int) -> None:
        self.name = name
        self.surname = surname
        self.age = age
        self._vehicle_count = 0
    def __eq__(self, other: 'Person') -> bool:
        return self.name == other.name and self.surname == other.surname and self.age == other.age


    def get_vehicle_count(self) -> int:
        return self._vehicle_count

    def increase_vehicle_count(self) -> None:
        self._vehicle_count += 1

    def decrease_vehicle_count(self) -> None:
        self._vehicle_count -= 1


class Vehicle:

    def __init__(self, registration_plate: str, creation_date: str, owner: Person) -> None:
        self.registration_plate = registration_plate
        self.creation_date = creation_date
        self.owner = owner

    def __eq__(self, other: 'Vehicle') -> bool:
        return self.registration_plate == other.registration_plate

    def get_registration_plate(self):
        return self.registration_plate

    def get_owner(self):
        return self.owner

    def change_owner(self, new_owner) -> None:
        self.owner.decrease_vehicle_count()
        self.owner = new_owner
        self.owner.increase_vehicle_count()

class Register:

    def __init__(self) -> None:
        self.vehicles = []
        self.owners = []

    def insert_vehicle(self, vehicle: Vehicle) -> int:
        if vehicle in self.vehicles:
            return 0
        else:
            self.vehicles.append(vehicle)
            owner = vehicle.get_owner()
            owner.increase_vehicle_count()
            if owner not in self.owners:
                self.owners.append(owner)
            return 1


    def update_vehicle_owner(self, registration_plate: str, new_owner: Person) -> int:
        for vehicle in self.vehicles:
            if vehicle.get_registration_plate() == registration_plate:
                if vehicle.get_owner() == new_owner:
                    return 0
                else:
                    old_owner = vehicle.get_owner()
                    vehicle.change_owner(new_owner)
                    if old_owner.get_vehicle_count() == 0:
                        self.owners.remove(old_owner)
                    if new_owner not in self.owners:
                        self.owners.append(new_owner)
                    return 1
        return 0

    def delete_vehicle(self, registration_plate: str) -> int:
        for vehicle in self.vehicles:
            if vehicle.get_registration_plate() == registration_plate:
                owner = vehicle.get_owner()
                self.vehicles.remove(vehicle)
                owner.decrease_vehicle_count()
                if owner.get_vehicle_count() == 0:
                    self.owners.remove(owner)
                return 1
        return 0


    def list_vehicles(self) -> List[Vehicle]:
        return self.vehicles

    def list_owners(self) -> List[Person]:
        return self.owners

    def list_vehicle_by_owner(self, owner: Person) -> List[Vehicle]:
        vehicles_by_owner = []
        for vehicle in self.vehicles:
            if vehicle.get_owner() == owner:
                vehicles_by_owner.append(vehicle)
        return vehicles_by_owner


"""
    ^^^^      YOUR SOLUTION      ^^^^
#################################################################
    vvvv TESTS FOR YOUR SOLUTION vvvv
"""


register = Register()

person1 = Person("John", "Doe", 20)
person2 = Person("Alice", "Doe", 22)

car1 = Vehicle("abc0", "20221122", person1)
car2 = Vehicle("abc1", "20221123", person1)
car3 = Vehicle("abc0", "20221122", person1)
car4 = Vehicle("xyz", "20221124", person2)

# car1 = Vehicle("abc", "20221122", person1)

# test insertion
assert register.insert_vehicle(car1) == 1
assert register.insert_vehicle(car2) == 1
assert register.insert_vehicle(car3) == 0
assert register.insert_vehicle(car4) == 1
assert register.list_vehicles() == [Vehicle("abc0", "20221122", person1), Vehicle("abc1", "20221123", person1), Vehicle("xyz", "20221124", person2)]
assert register.list_owners() == [Person("John", "Doe", 20), Person("Alice", "Doe", 22)] and register.list_owners()[0].get_vehicle_count() == 2 and register.list_owners()[1].get_vehicle_count() == 1

# test update
assert register.update_vehicle_owner("abc1", person1) == 0
assert register.update_vehicle_owner("not in register", person1) == 0
assert register.update_vehicle_owner("abc1", person2) == 1
assert register.list_vehicles() == [Vehicle("abc0", "20221122", person1), Vehicle("abc1", "20221123", person2), Vehicle("xyz", "20221124", person2)]
assert register.list_owners() == [Person("John", "Doe", 20), Person("Alice", "Doe", 22)] and register.list_owners()[0].get_vehicle_count() == 1 and register.list_owners()[1].get_vehicle_count() == 2
assert register.update_vehicle_owner("abc0", person2) == 1
assert register.list_vehicles() == [Vehicle("abc0", "20221122", person2), Vehicle("abc1", "20221123", person2), Vehicle("xyz", "20221124", person2)]
assert register.list_owners() == [Person("Alice", "Doe", 22)] and register.list_owners()[0].get_vehicle_count() == 3

# test delete
assert register.delete_vehicle("not in register") == 0
assert register.delete_vehicle("abc0") == 1
assert register.delete_vehicle("abc1") == 1
assert register.delete_vehicle("xyz") == 1
assert register.list_vehicles() == []
assert register.list_owners() == []

# test lists
car1 = Vehicle("abc0", "20221122", person1)
car2 = Vehicle("abc1", "20221123", person1)
car3 = Vehicle("abc0", "20221122", person1)
car4 = Vehicle("xyz", "20221124", person2)

register.insert_vehicle(car1)
register.insert_vehicle(car2)
register.insert_vehicle(car3)
register.insert_vehicle(car4)

assert register.list_vehicles() == [Vehicle("abc0", "20221122", person1), Vehicle("abc1", "20221123", person1), Vehicle("xyz", "20221124", person2)]
assert register.list_owners() == [Person("John", "Doe", 20), Person("Alice", "Doe", 22)]
assert register.list_vehicle_by_owner(person1) == [Vehicle("abc0", "20221122", person1), Vehicle("abc1", "20221123", person1)]