
from starlette.responses import HTMLResponse
from typing import Union , Optional
import uvicorn
from fastapi import FastAPI
import uuid

class AirportSystem:
    __admin_list = []
    __reservation_list = []	
    __flight_list = []
    __flight_instance_list = []
    __aircraft_list = []
    __payment_method_list = []
    __airport_list = []

    def get_reservation_list_for_show():
        reservations = []
        for reservation in AirportSystem.__reservation_list:
            reservations.append(reservation.convert_to_json())
        return reservations

    def get_reservation_list():
        return AirportSystem.__reservation_list

    def check_in(booking_reference, name, flight_instance_order = False):
        passenger = AirportSystem.check_passenger(booking_reference, name)
        reservation = AirportSystem.find_reservation(booking_reference)
        if not reservation:
            return "Reservation not found"
        if not passenger:
            return "Passenger not found"
        
        result = AirportSystem.create_boarding_pass(reservation, passenger, flight_instance_order)
        return result
    
    def create_airport(airport):
        AirportSystem.__airport_list.append(airport)
        return airport
    
    def get_airport_list():
        return AirportSystem.__airport_list

    def create_reservation():
        reservation = Reservation()
        AirportSystem.__reservation_list.append(reservation)
        return reservation.convert_to_json()
    
    def find_reservation(booking_reference):
        for reservation in AirportSystem.__reservation_list:
            print(reservation.booking_reference, booking_reference)
            if reservation.booking_reference == booking_reference:
                return reservation
            
    def check_passenger(booking_reference, name):
        for passenger in AirportSystem.find_reservation(booking_reference).passengers:
            if passenger.name == name:
                return passenger

    def create_boarding_pass(reservation, passenger, flight_instance_order = False):
        if reservation.paid_status == False:
            return "Reservation is not paid yet."
        reservation.boarding_pass = BoardingPass(reservation, passenger, flight_instance_order)
        return BoardingPass(reservation, passenger, flight_instance_order).convert_to_json()
    
    def get_flight_instance_list():
        flight_instances = []
        for flight_instance in AirportSystem.__flight_instance_list:
            flight_instances.append(flight_instance.convert_to_json())
        return flight_instances
    
    def get_flight_instance(froml, to, date_depart, depart_time, arrive_time):
        for flight_instance in AirportSystem.__flight_instance_list:
            if flight_instance.froml.name.upper() == froml.upper() and flight_instance.to.name.upper() == to.upper() and flight_instance.date == date_depart and flight_instance.time_departure == depart_time and flight_instance.time_arrival == arrive_time:
                return flight_instance
            
        return "No flight_instance found"
    
    def check_flight_instance_matches(froml, to, date_depart, date_return = None):
        departing_flight_instance = []
        returning_flight_instance = []

        #find flight_instance with the same from/to locations and date
        for flight_instance in AirportSystem.__flight_instance_list:
            if flight_instance.froml.name.upper() == froml.upper() and flight_instance.to.name.upper() == to.upper() and flight_instance.date == date_depart:
                departing_flight_instance.append(flight_instance)

        #find flight_instance with the same from/to locations and date but reversed (return flight)
        if date_return != None:
            for flight_instance in AirportSystem.__flight_instance_list:
                if flight_instance.froml.name.upper() == to.upper() and flight_instance.to.name.upper() == froml.upper() and flight_instance.date == date_return:
                    returning_flight_instance.append(flight_instance)

        # departing_flight_matches = AirportSystem.get_detail_of_flight(departing_flight_instance)
        # returning_flight_matches = AirportSystem.get_detail_of_flight(returning_flight_instance)
        # return (departing_flight_matches, returning_flight_matches)
        return (departing_flight_instance, returning_flight_instance)
    
    def get_detail_of_flight(flight_instance_list):
            all_detail = []
            
            for flight_instance in flight_instance_list:
                  sub_detail = {"from":flight_instance.froml.name , "to":flight_instance.to.name,
                                "flight_instance_number":flight_instance.flight_number, "time_departure":flight_instance.time_departure,
                                "time_arrival":flight_instance.time_arrival,"aircraft":flight_instance.aircraft.aircraft_number,
                                "depart":flight_instance.date}
                  all_detail.append(sub_detail)
        
            return all_detail  
    
    # def choose_flight_instance(booking_reference, froml, to, date_depart, depart_time, arrive_time, name, order):
    #     flight_instance = None
    #     flight_instance_matches = AirportSystem.check_flight_instance_matches(froml, to, date_depart)
        
    #     if not flight_instance_matches:
    #         return "No matches found"
        
    #     for f in flight_instance_matches[0]:
    #         if f.time_departure == depart_time and f.time_arrival == arrive_time:
    #           flight_instance = f
              
    #     if not flight_instance:
    #         return "No flight_instance found"
        
    #     reservation = AirportSystem.find_reservation(booking_reference)
        
    #     if len(reservation.flight_instances) <= order:
    #         reservation.flight_instances = [order, flight_instance]
    #     for flight_pair in reservation.flight_instances:
    #         if flight_pair[0] == order:
    #             flight_pair[1] = flight_instance
    #     reservation.sort_order()
            
    #     #reservation.flight_instances = flight_instance #adding (using @property setter)
    #     return reservation.convert_to_json() #for swagger checking: remove later
    
    # def check_flight_seat(flight_seat):
    #     flight_seats = []
    #     for seat in flight_seat:
    #         flight_seats.append(seat.convert_to_json())        
    #     return flight_seats

    # def choose_flight_seat(booking_reference : str, name : str, seat_number : str, flight_instance_order: int):
    #     reservation = AirportSystem.find_reservation(booking_reference)
    #     passenger = AirportSystem.check_passenger(booking_reference, name)
    #     flight_instance = reservation.flight_instances[flight_instance_order]
    #     new_flight_seat = flight_instance.get_flight_seat_from_seat_num(seat_number)

    #     old_seat = flight_instance.get_flight_seat_from_seat_num(passenger.seat[flight_instance_order].seat_number)
        
    #     if old_seat:
    #         old_seat.occupied = False
    #         passenger.seat.remove(old_seat)
        
    #     reservation.sort_order()
    #     return passenger
    
    def show_reservation(booking_reference) :
        reservation = AirportSystem.find_reservation(booking_reference)
        reservation_detail = {"booking_reference": reservation.booking_reference,
                              "passengers": []}
        
        for passenger in reservation.passengers:
            passenger_detail = {
                "title": passenger.title,
                "name": passenger.name,
                "birthday": passenger.birthday,
                "phone_number": passenger.phone_number,
                "email": passenger.email,
                "flight_instances": [flight_i_pair[1].convert_to_json() for flight_i_pair in reservation.flight_instances],
                "seat":[flight_seat_pair[1].convert_to_json() for flight_seat_pair in passenger.flight_seats],
                "extra_services": [
                    {
                        "service_name": service.__class__.__name__,
                        **({"weight": service.bag_weight} if hasattr(service, "bag_weight") else {}),
                        "price_per_unit" : service.price_per_unit if hasattr(service, "price_per_unit") else None,
                    }
                    for service in passenger.extra_services
                ]
            }

            reservation_detail["passengers"].append(passenger_detail)
            
        reservation_detail["total_cost"] = reservation.calculate_total_cost()
        reservation_detail["paid_status"] = reservation.paid_status

        return reservation_detail
            
    def get_admin_list():
        admins = []
        for admin in AirportSystem.__admin_list:
            admins.append(admin.convert_to_json())
        return admins
        
    def create_admin(title, first_name, middle_name, last_name, birth_date, phone_number, email):
        new_admin = Admin(title, first_name, middle_name, last_name, birth_date, phone_number, email)
        AirportSystem.__admin_list.append(new_admin)
        return new_admin

    def check_admin(name):
        for admin in AirportSystem.__admin_list:
            if admin.name == name:
                return admin
            
    def get_flight_list():
        flights = []
        for flight in AirportSystem.__flight_list:
            flights.append(flight.convert_to_json())
        return AirportSystem.__flight_list

    def create_flight_instance(name , flight_number , aircraft_number , time_departure , time_arrival , date , cost):
        result = "Flight Instance created successfully"
        admin = AirportSystem.check_admin(name)
        if not admin:
            result = "Not an Admin"
        flight = AirportSystem.check_flight_from_flight_number(flight_number)
        if not flight:
            result = "Flight not found"
        
        aircraft = AirportSystem.check_aircraft_from_aircraft_number(aircraft_number)
        flight_instance = FlightInstance(flight.froml, flight.to, flight.flight_number, time_departure, time_arrival, aircraft, date, cost)
        AirportSystem.__flight_instance_list.append(flight_instance)
        result = flight_instance.convert_to_json() #return for checking in swagger

        return result

    def create_flight(froml, to, flight_number):
        new_flight = Flight(froml, to, flight_number)
        AirportSystem.__flight_list.append(new_flight)
        return new_flight

    def get_aircraft_list():
        aircrafts = []
        for aircraft in AirportSystem.__aircraft_list:
            aircrafts.append(aircraft.convert_to_json())
        return aircrafts
    
    def seat_data():
        seats_data = []
        for c in range(1,10):
            for r in range(0,6):
                alphabets = "ABCDEF"
                seat_id = f"{alphabets[r]}{c}"
                seat_category = Category("normal_seat",0)
                if r <= 2:
                    seat_category = Category("premium_seat",500)
                if r <= 4:
                    seat_category = Category("happy_seat",200)
                seats_data.append(Seats(seat_id, seat_category))
        return seats_data
    
    def create_aircraft(*aircraft_numbers):
        for aircraft_number in aircraft_numbers:
            aircraft = Aircraft(AirportSystem.seat_data(), aircraft_number)
            print(aircraft)
            AirportSystem.__aircraft_list.append(aircraft)
        return aircraft

    def check_flight_from_flight_number(flight_number):
        for flight in AirportSystem.__flight_list:
            if flight.flight_number == flight_number:
                return flight
            
    def check_aircraft_from_aircraft_number(aircraft_number):
        for aircraft in AirportSystem.__aircraft_list:
            if aircraft.aircraft_number == aircraft_number:
                return aircraft
            
class Reservation:
    def __init__(self):
        self.__flight_instances = []
        self.__passengers = []
        generated_uuid = str(uuid.uuid4()).split("-")
        self.__booking_reference = generated_uuid[1] + generated_uuid[2]
        self.__total_cost = 0
        self.__boarding_pass = []
        self.__additional_fees = 0
        self.__paid_status = False

    def calculate_total_cost(self):
        self.__total_cost = 0
        for flight_instance in self.flight_instances:
            self.__total_cost += flight_instance[1].cost * len(self.passengers)

        for passenger in self.passengers:
            for f_seat in passenger.flight_seats :
                self.__total_cost += f_seat[1].seat_category.seat_price
                
            for service in passenger.extra_services:
                if isinstance(service, Insurance):
                    self.__total_cost += service.price_per_unit
                elif isinstance(service, Baggage):
                    self.__total_cost += service.get_total_cost()
        
        self.__total_cost += self.__additional_fees
        
        return self.__total_cost

    def create_passenger(self, title, first_name, middle_name, last_name, birthday, phone_number, email):
        new_passenger = Passenger(title, first_name, middle_name, last_name, birthday, phone_number, email)
        self.__passengers.append(new_passenger)
        self.calculate_total_cost()
        return self.convert_to_json()
    
    def choose_flight_instance(self, froml, to, date_depart, depart_time, arrive_time, flight_instance_order):
        flight_instance = AirportSystem.get_flight_instance(froml, to, date_depart, depart_time, arrive_time)
              
        if not flight_instance:
            return "No flight_instance found"
        
        #replace case
        for pair in self.__flight_instances:
            if pair[0] == flight_instance_order:
                pair[1] = flight_instance
                self.sort_order()
                self.calculate_total_cost()
                return self.convert_to_json()
        
        #add case
        self.__flight_instances.append([flight_instance_order, flight_instance])
        self.sort_order()
        self.calculate_total_cost()
            
        #reservation.flight_instances = flight_instance #adding (using @property setter)
        return self.convert_to_json() #for swagger checking: remove later
    
    def select_flight_seat(self, name, seat_number, flight_instance_order):
        result = None
        passenger = self.search_passenger(name)
        
        if flight_instance_order >= len(self.__flight_instances):
            result = "No flight_instance found"
            return result
        
        flight_instance = self.__flight_instances[flight_instance_order][1]
        new_flight_seat = flight_instance.get_flight_seat_from_seat_num(seat_number)
        
        if not passenger:
            result = "Passenger not found"
        elif not new_flight_seat:
            result = "No seat found"
        elif new_flight_seat.occupied:
            result = "Seat is occupied"
        
        for seat in passenger.flight_seats:
            if seat[0] == flight_instance_order:
                seat[1].occupied = False
                seat[1] = new_flight_seat
                new_flight_seat.occupied = True
                self.sort_order()
                self.calculate_total_cost()
                result = self.convert_to_json()
                return result
        
        new_flight_seat.occupied = True
        passenger.flight_seats.append([flight_instance_order, new_flight_seat])
        self.sort_order()
        self.calculate_total_cost()
        result = self.convert_to_json()
        return result
    
    def search_passenger(self, name):
        for passenger in self.__passengers:
            if passenger.name == name:
                return passenger
    
    def sort_order(self):
        for passenger in self.__passengers:
            passenger.flight_seats.sort(key=lambda x: x[0])
        self.__flight_instances.sort(key=lambda x: x[0])
    

    def valid_for_payment(self):
        seat_check = all(len(passenger.flight_seats) == len(self.flight_instances) for passenger in self.__passengers)
        return seat_check and self.__total_cost > 0 and self.__paid_status == False and len(self.__passengers) > 0 and len(self.__flight_instances) > 0
    
    @property
    def additional_fee(self):
        return self.__additional_fees
    
    @additional_fee.setter
    def additional_fee(self, fee):
        self.__additional_fees = fee        
            
    @property 
    def total_cost(self) :
        return self.__total_cost
    
    @property
    def paid_status(self) :
        return self.__paid_status
    
    @paid_status.setter
    def paid_status(self, status) :
        self.__paid_status = status

    @property
    def booking_reference(self):
        return self.__booking_reference

    @property
    def passengers(self):
        return self.__passengers
    
    @passengers.setter
    def passengers(self, passenger):
        self.__passengers.append(passenger)
    
    @property
    def boarding_pass(self):
        return self.__boarding_pass

    @boarding_pass.setter
    def boarding_pass(self, boarding_pass):
        self.__boarding_pass.append(boarding_pass)

    @property
    def flight_instances(self):
        return self.__flight_instances
    
    @flight_instances.setter
    def flight_instances(self, flight):
        self.__flight_instances.append(flight)

    def convert_to_json(self):
        flight_instances = []
        for flight_instance in self.__flight_instances:
            flight_instances.append((flight_instance[0], flight_instance[1].convert_to_json()))
        return {"flight_instance" : flight_instances,
                "passenger" : self.__passengers,
                "booking_reference" : self.__booking_reference,
                "total_cost" : self.__total_cost,
                "boarding_pass" : self.__boarding_pass}


class User:
    def __init__(self, title, first_name, middle_name, last_name, birthday, phone_number, email):
        self.__title = title
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__last_name = last_name
        self.__birthday = birthday
        self.__phone_number = phone_number
        self.__email = email

    @property
    def phone_number(self) :
        return self.__phone_number
    
    @property
    def email(self) :
        return self.__email

    @property
    def birthday(self) :
        return self.__birthday
        
    @property
    def first_name(self):
        return self.__first_name
    
    @property
    def middle_name(self):
        return self.__middle_name

    @property
    def last_name(self):
        return self.__last_name
    
    @property
    def title(self):
        return self.__title
    
    @property
    def name(self):
        if self.__middle_name:
            return self.__first_name + " " + self.__middle_name + " " + self.__last_name
        return self.__first_name + " " + self.__last_name

    def convert_to_json(self):
        return {"title" : self.__title,
                "name" : self.name,
                "birthday" : self.__birthday,
                "phone_number" : self.__phone_number,
                "email" : self.__email}

class Passenger(User):
    def __init__(self, title, first_name, middle_name, last_name, birthday, phone_number, email):
        super().__init__(title, first_name, middle_name, last_name, birthday, phone_number, email)
        self.__flight_seats = []
        self.__extra_services = []
        
    @property
    def flight_seats(self):
        return self.__flight_seats
    
    @flight_seats.setter
    def flight_seats(self, flight_seat_order):
        self.__flight_seats.append(flight_seat_order)
        return "Success"

    @property
    def extra_services(self):
        return self.__extra_services

    @extra_services.setter
    def extra_services(self, service):
        self.__extra_services.append(service)
        return self.__extra_services

    def add_extra_service(self, baggage_kilo, insurance):
        self.__extra_services = []
        result = None
        if baggage_kilo:
            self.extra_services = Baggage(100, baggage_kilo)
            result = self.extra_services
        if Insurance:
            self.extra_services = Insurance(200)
            result = self.extra_services
        return result

    def convert_to_json(self):
        return {"title" : self.title,
                "name" : self.name,
                "birthday" : self.birthday,
                "phone_number" : self.phone_number,
                "email" : self.email,
                "seat" : self.__flight_seats,
                "extra_services" : self.__extra_services}

class Admin(User):
    pass
    
class BoardingPass:
    def __init__(self, reservation, passenger, returnl = 0):
        self.__flight_seat_number = passenger.flight_seats[returnl][1]
        self.__flight_number = reservation.flight_instances[returnl][1]
        self.__passenger_title = passenger.title
        self.__passenger_name = passenger.name
        self.__aircraft_number = reservation.flight_instances[returnl][1].aircraft.aircraft_number
        self.__booking_reference = reservation.booking_reference
        self.__departure_date = reservation.flight_instances[returnl][1].date
        self.__boarding_time = reservation.flight_instances[returnl][1].boarding_time
        self.__from = reservation.flight_instances[returnl][1].froml
        self.__to = reservation.flight_instances[returnl][1].to

    def convert_to_json(self):
        return {"flight_seat_number" : self.__flight_seat_number.seat_number ,
                "flight_number" : self.__flight_number.flight_number,
                "title" : self.__passenger_title,
                "name" : self.__passenger_name,
                "aircraft_number" : self.__aircraft_number,
                "booking_reference" : self.__booking_reference,
                "departure_time" : self.__departure_date,
                "boarding_time" : self.__boarding_time,
                "from" : self.__from,
                "to" : self.__to}

class Flight:
    def __init__(self, froml, to, flight_number):
        self.__from = froml
        self.__to = to
        self.__flight_number = flight_number

    @property
    def flight_number(self):
        return self.__flight_number  
      
    @property
    def froml(self):
        return self.__from
    
    @property
    def to(self):
        return self.__to

    def convert_to_json(self):
        return {"from" : self.__from,
                "to" : self.__to, 
                "flight_number" : self.__flight_number}

class FlightInstance(Flight):
    def __init__(self, froml, to, flight_number, time_departure, time_arrival, aircraft, date, cost):
        super().__init__(froml, to, flight_number)
        self.__flight_seats = []
        for seat in aircraft.seats:
            self.__flight_seats.append(SeatFlight(seat))
        self.__time_departure = time_departure
        self.__time_arrival = time_arrival
        self.__aircraft = aircraft
        self.__date = date
        self.__cost = int(cost)
        
    def see_flight_seats(self):
        return [f_seat.convert_to_json() for f_seat in self.__flight_seats]
    
    @property
    def date(self):
        return self.__date
    
    @property
    def boarding_time(self):
        return self.__time_departure + " - " + self.__time_arrival
    
    @property
    def aircraft(self):
        return self.__aircraft
    
    @property
    def time_departure(self):
        return self.__time_departure
    
    @property
    def time_arrival(self):
        return self.__time_arrival
    
    @property
    def flight_seats(self):
        return self.__flight_seats
    
    @property
    def cost(self):
        return self.__cost

    def convert_to_json(self):
        return {"from" : self.froml,
                "to" : self.to, 
                "flight_number" : self.flight_number,
                "time_daparture" : self.__time_departure,
                "time_arrival" : self.__time_arrival,
                "date" : self.__date,
                "aircraft_number" : self.__aircraft.aircraft_number,
                "cost" : self.__cost}

    def get_flight_seat_from_seat_num(self, seat_num):
        for flight_seat in self.__flight_seats:
            if flight_seat.seat_number == seat_num:
                return flight_seat
    
class Aircraft:
    def __init__(self, seats, aircraft_number):
        self.__seats = seats
        self.__aircraft_number = aircraft_number

    @property
    def aircraft_number(self):
        return self.__aircraft_number
    
    @property
    def seats(self):
        return self.__seats

    def convert_to_json(self):
        return {"seats_count" : len(self.__seats) ,
                "aircraft_number" : self.__aircraft_number}

class Airport:
    def __init__(self, name, short_name):
            self.__name = name
            self.__short_name = short_name
    @property
    def name(self):
            return self.__name
    
class Seats:
    def __init__(self, seat_number, seat_category):
        self.__seat_number = seat_number
        self.__seat_category = seat_category

    @property
    def seat_number(self):
        return self.__seat_number
    
    @property
    def seat_category(self):
        return self.__seat_category


class SeatFlight(Seats):
    def __init__(self, seat, occupied = False):
        super().__init__(seat.seat_number, seat.seat_category)
        self.__occupied = occupied
    
    @property
    def occupied(self):
        return self.__occupied
    
    @occupied.setter
    def occupied(self, occupied):
        self.__occupied = occupied
        return "Success"

    def convert_to_json(self):
        return {"seat_number" : self.seat_number,
                "seat_category" : self.seat_category,
                "seat_occupied" : self.__occupied}

class Category:
    def __init__(self, name, price_per_unit):
        self.__name = name
        self.__price = int(price_per_unit)

    @property
    def seat_price(self) :
        return self.__price
    
class Payment:
    def __init__(self, paid_time):
        self.__paid_time = paid_time
        self.__payment_fee = 0
        
    @property
    def payment_fee(self):
        return self.__payment_fee
    
    @payment_fee.setter
    def payment_fee(self, fee):
        self.__payment_fee = fee
        
    def pay(self, reservation) :
        reservation.additional_fee += self.payment_fee
        if reservation.total_cost <= 0 :
            return "Invalid Cost"
        if not reservation.valid_for_payment():
            return "Invalid for Payment"
        reservation.paid_status = True
        return reservation.paid_status
        
class CreditCard(Payment):
    def __init__(self, paid_time, card_number, cardholder_name, expiry_date, cvv):
        super().__init__(paid_time)
        self.__card_number = card_number
        self.__cardholder_name = cardholder_name
        self.__expiry_date = expiry_date
        self.__cvv = cvv
        self.payment_fee = 240

class Qr(Payment):
    def __init__(self, paid_time):
       super().__init__(paid_time)
       
       
class Service:
    def __init__(self, price_per_unit):
        self.__price_per_unit = float(price_per_unit)

    @property
    def price_per_unit(self) :
        return self.__price_per_unit
    

class Insurance(Service):
    def __init__(self, price_per_unit):
        super().__init__(price_per_unit)
    
class Baggage(Service):
    def __init__(self, price_per_unit, weight):
        super().__init__(price_per_unit)
        self.__weight = weight

    def get_total_cost(self):
        return self.price_per_unit * self.__weight
    
    @property
    def bag_weight(self) :
        return self.__weight

normal_seat = Category("normal_seat",0)
happy_seat = Category("happy_seat",200)
premium_seat = Category("happy_seat",500)

seats_data = []
for r in range(1,10):
    for c in range(0,6):
        alphabets = "ABCDEF"
        seat_id = f"{alphabets[c]}{r}"
        seat_category = normal_seat
        if r <= 2:
            seat_category = premium_seat
        if r <= 4:
            seat_category = happy_seat
        seats_data.append(Seats(seat_id, seat_category))

def init_db():
    AirportSystem.create_airport(Airport("Don Mueang", "[BKK]"))
    AirportSystem.create_airport(Airport("Chiang Mai", "[CNX]"))
    AirportSystem.create_airport(Airport("Phuket", "[BKK]"))
    
    AirportSystem.create_admin("Mr.", "Admin", "", "A", "1990-01-01", "0812345678", "a1@gmail.com")

    AirportSystem.create_aircraft("B737-1", "B737-2", "B737-2")
    
    don_mueang = AirportSystem.get_airport_list()[0]
    chiang_mai = AirportSystem.get_airport_list()[1]
    phuket = AirportSystem.get_airport_list()[2]
    
    AirportSystem.create_flight(don_mueang, chiang_mai, "DD 712")
    AirportSystem.create_flight(chiang_mai, don_mueang, "DD 721")

    AirportSystem.create_flight(don_mueang, phuket, "DD 813")
    AirportSystem.create_flight(phuket, don_mueang, "DD 831")

    AirportSystem.create_flight(chiang_mai, phuket, "DD 823")
    AirportSystem.create_flight(phuket, chiang_mai, "DD 832")
    
    AirportSystem.create_flight_instance("Admin A", "DD 712", "B737-1", "08:00", "10:00", "01-01-2000", 1000)
    AirportSystem.create_flight_instance("Admin A", "DD 721", "B737-1", "10:00", "12:00", "02-01-2000", 1000)
    AirportSystem.create_reservation()
    reservation = AirportSystem.get_reservation_list()[0]
    reservation.create_passenger("Mr.", "P", "A", "S", "now", "666", "p@gmail.com")
    d_to_c = AirportSystem.get_flight_instance_list()[0]
    c_to_d = AirportSystem.get_flight_instance_list()[1]
    reservation.choose_flight_instance(don_mueang.name, chiang_mai.name, "01-01-2000", "08:00", "10:00", 0)
    

    

init_db()

app = FastAPI()

@app.get("/")
def normal():
    html_content = """
    <html>
<head>
<style>
.myButton {
	box-shadow: 1px 7px 24px -7px #276873;
	background:linear-gradient(to bottom, #599bb3 5%, #408c99 100%);
	background-color:#599bb3;
	border-radius:21px;
	display:inline-block;
	cursor:pointer;
	color:#ffffff;
	font-family:Arial;
	font-size:23px;
	font-weight:bold;
	padding:19px 43px;
	text-decoration:none;
	text-shadow:0px 0px 0px #3d768a;
}
.myButton:hover {
	background:linear-gradient(to bottom, #408c99 5%, #599bb3 100%);
	background-color:#408c99;
}
.myButton:active {
	position:relative;
	top:1px;
}
</style>
</head>
<body>
<center><a href="/docs" class="myButton">GO TO DOCS</a></center>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.get("/all_flight", tags=["Debug List Getter"])
def all_flight():
    return AirportSystem.get_flight_list()

@app.get("/all_aircraft", tags=["Debug List Getter"])
def all_aircraft():
    return AirportSystem.get_aircraft_list()

@app.get("/all_reservation", tags=["Debug List Getter"])
def all_reservation():
    return AirportSystem.get_reservation_list_for_show()

@app.get("/all_flight_instance", tags=["Debug List Getter"])
def all_flight_instance():
    return AirportSystem.get_flight_instance_list()

@app.get("/all_admin", tags=["Admin"])
def all_admin():
    return AirportSystem.get_admin_list()

@app.post("/create_admin", tags=["Admin"])
def create_admin(title : str, first_name : str, last_name : str, birth_date : str, phone_number : str, email : str, middle_name : Optional[str] = None):
    return AirportSystem.create_admin(title, first_name, middle_name, last_name, birth_date, phone_number, email).convert_to_json()

@app.post("/create_flight_instance", tags=["Admin"])
def create_flight_instance(name : str, flight_number : str, aircraft_number : str, time_departure : str, time_arrival : str, date : str, cost : float):
    return AirportSystem.create_flight_instance(name, flight_number, aircraft_number, time_departure, time_arrival, date, cost)

@app.post("/create_reservation", tags=["Reservation"])
def new_reservation():
    return AirportSystem.create_reservation()

@app.get("/see_reservation" , tags=["Reservation"])
def show_reservation(booking_reference : str) :
    return AirportSystem.show_reservation(booking_reference)

@app.get("/flight_instance_matches", tags=["1: Get + Select Flight Instance"])
def get_flight_instances_matches(froml : str, to : str, depart_date : str, return_date : Optional[str] = None):
    return AirportSystem.check_flight_instance_matches(froml, to, depart_date, return_date)
                                               
@app.put("/select_flight_instance", tags=["1: Get + Select Flight Instance"])  #
def select_flight_instance(booking_reference : str, froml : str, to : str, date : str, depart_time : str, arrive_time : str, flight_instance_order: int):
    reservation = AirportSystem.find_reservation(booking_reference)
    return reservation.choose_flight_instance(froml, to, date, depart_time, arrive_time, flight_instance_order)

@app.post("/passenger", tags=["2: Add Passengers"])
def new_passenger(booking_reference : str, title : str, first_name : str, last_name : str, birthday : str, phone_number : str, email : str, middle_name : Optional[str] = None):
    reservation = AirportSystem.find_reservation(booking_reference)
    reservation.create_passenger(title, first_name, middle_name, last_name, birthday, phone_number, email)
    return reservation.convert_to_json()

@app.get("/see_seat" , tags=["3: Get Seats + Select Seats + Apply Services"])
def see_seat(froml : str, to : str, date : str, depart_time : str, arrive_time : str):
    # return AirportSystem.check_flight_seat(AirportSystem.choose_flight_instance(AirportSystem.check_flight_instance(froml, to, date) , depart_time, arrive_time).flight_seats)
    return AirportSystem.get_flight_instance(froml, to, date, depart_time, arrive_time).see_flight_seats()

@app.put("/select_seat", tags=["3: Get Seats + Select Seats + Apply Services"])
def select_seat(booking_reference : str, name : str, seat_number : str, flight_instance_order: int):
    # passenger = AirportSystem.check_passenger(booking_reference, name)
    # reservation = AirportSystem.find_reservation(booking_reference)
    # depart_flight_instance = reservation.flight_instances[0]

    # AirportSystem.choose_flight_seat(passenger, depart_flight_instance, seat)
    # if return_seat != None:
    #     return_flight_instance = reservation.flight_instances[1]
    #     AirportSystem.choose_flight_seat(passenger, return_flight_instance, return_seat)
    # return passenger
    reservation = AirportSystem.find_reservation(booking_reference)
    return reservation.select_flight_seat(name, seat_number, flight_instance_order)

@app.put("/apply_services", tags=["3: Get Seats + Select Seats + Apply Services"])
def apply_services (booking_reference: str, name : str, baggage_kilo : Optional[int] = None, insurance : Optional[bool] = None):
    AirportSystem.check_passenger(booking_reference, name).add_extra_service(baggage_kilo, insurance)
    return AirportSystem.check_passenger(booking_reference, name).extra_services

@app.post("/payment_credit", tags=["4: Payment"])
def pay_by_credit(booking_referrence: str, card_number: str, cardholder_name: str, expiry_date: str, cvv: str, paid_time: str):
    return CreditCard(paid_time, card_number, cardholder_name, expiry_date, cvv).pay(AirportSystem.find_reservation(booking_referrence))

@app.post("/pay_qr", tags=["4: Payment"])
def pay_by_qr(booking_reference: str, paid_time: str) :
    return Qr(paid_time).pay(AirportSystem.find_reservation(booking_reference))

@app.get("/boarding_pass", tags=["5: Check In"])
def board_pass(booking_reference : str, name : str, return_trip : Optional[bool] = False):
    return AirportSystem.check_in(booking_reference, name, return_trip)

@app.get("/test")
def test():
    return uuid.uuid4()

if __name__ == "__main__":
    uvicorn.run("test_branch2:app", host="127.0.0.1", port=8000, log_level="info")

# @app.get("/see_flight_instance", tags=["flight"]) #
# def see_flight_instance(froml : str, to : str, date_depart : str, return_depart : Optional[str] = None):
#     return AirportSystem.get_detail_of_flight(AirportSystem.check_flight_instance(froml, to, date_depart, return_depart))

    
    # depart_flight_instance = AirportSystem.check_flight_instance(froml, to, date)
    # reservation = AirportSystem.find_reservation(booking_reference)

    # if depart_flight_instance and reservation:
    #     reservation.flight_instances = AirportSystem.choose_flight_instance(depart_flight_instance, depart_time, arrive_time)

    #     if return_date:
    #         return_flight_instance = AirportSystem.check_flight_instance(to, froml, return_date)
    #         reservation.flight_instances = AirportSystem.choose_flight_instance(return_flight_instance, return_depart_time, return_arrive_time)
    
    # return reservation
    
    # if AirportSystem.check_flight_instance(froml, to, date) and AirportSystem.find_reservation(booking_reference):
    #     AirportSystem.find_reservation(booking_reference).flight_instances = AirportSystem.choose_flight_instance(AirportSystem.check_flight_instance(froml, to, date), depart_time, arrive_time)

    #     if return_date:
    #         return_flight_instance = AirportSystem.check_flight_instance(to, froml, return_date)
    #         AirportSystem.find_reservation(booking_reference).flight_instances = AirportSystem.choose_flight_instance(return_flight_instance, return_depart_time, return_arrive_time)
    
    # return AirportSystem.find_reservation(booking_reference).convert_to_json()




