from enum import Enum  # Import Enum to define specific categories
from datetime import date, datetime, timedelta # Import date class to handle dates


# Enum for ticket types to represent ticket categories
class TicketType(Enum):
    SINGLE_DAY = "Single-Day"
    TWO_DAY = "Two-Day"
    ANNUAL = "Annual"
    CHILD = "Child"
    GROUP = "Group"
    VIP = "VIP"

# Enum for ticket statuses to track the state of a ticket
class TicketStatus(Enum):
    ACTIVE = "Active"
    USED = "Used"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"

# Enum for payment methods to ensure consistency in payment processing
class PaymentMethod(Enum):
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    DIGITAL_WALLET = "Digital Wallet"


#Represents a ticket in the theme park system
class Ticket:
# Static dictionary holding ticket details for all ticket types
    TICKET_DETAILS = {
        TicketType.SINGLE_DAY: {"price": 275, "validity_period": 1, "discount": 0},
        TicketType.TWO_DAY: {"price": 480, "validity_period": 2, "discount": 10},  # 10% for online purchase
        TicketType.ANNUAL: {"price": 1840, "validity_period": 365, "discount": 15},  # 15% for renewal
        TicketType.CHILD: {"price": 185, "validity_period": 1, "discount": 0},
        TicketType.GROUP: {"price": 220, "validity_period": 1, "discount": 20},  # 20% for groups of 20+
        TicketType.VIP: {"price": 550, "validity_period": 1, "discount": 0},
    }
# Initialize a Ticket attribute
    def __init__(self, ticket_type: TicketType, price, validity_period, discount=0.0, guest_id=None ):
        self._ticket_id = id(self)  # protected attribute to store ticket Unique ID
        self._ticket_type = ticket_type  #protected Enum to store ticket type
        self._price = price  # protected Ticket price
        self._validity_period = validity_period  #protected Validity of the ticket
        self._purchase_date = datetime.now().date() # protected Purchase date of the ticket
        self._discount = discount  # protected Discount applied to the ticket
        self._status = TicketStatus.ACTIVE  #protected Default status is "Active"
        self._guest_id = guest_id  #protected Associate the ticket with a guest ID

        # Ensure guest ID is either None or an integer
        if self._guest_id is not None and not isinstance(self._guest_id, int):
            raise ValueError("Guest ID must be an integer or None.")

        # Ensure the price is non-negative
        if self._price < 0:
            raise ValueError("Price must be non-negative.")


    # Getters and Setters for ticket attributes
    def get_ticket_id(self):
        return self._ticket_id

    def get_ticket_type(self):
        return self._ticket_type
    def set_ticket_type(self, ticket_type):
        self._ticket_type = ticket_type

    def get_price(self):
        return self._price

    def get_validity_period(self):
        return self._validity_period

    def get_purchase_date(self):
        return self._purchase_date
    def set_purchase_date(self, purchase_date):
        self._purchase_date = purchase_date

    def get_status(self):
        return self._status
    def set_status(self, status):
        self._status = status

    def get_discount(self):
        return self._discount
    def set_discount(self, discount):
# Validate that discount is a percentage between 0 and 100
        if not (0 <= discount <= 100):
            raise ValueError("Discount must be between 0 and 100.")
        self._discount = discount

    def get_guest_id(self):
        return self._guest_id  # Access the protected guest_id
    def set_guest_id(self, guest_id):
        self._guest_id = guest_id


# Validate that discount is a percentage between 0 and 100
    def apply_discount(self, discount_type, group_size=0):
#Apply a discount based on type or group size.
        if discount_type == "Online Purchase" and self._ticket_type == TicketType.TWO_DAY:
            self._discount = 10  # 10% discount for online purchase
        elif discount_type == "Renewal" and self._ticket_type == TicketType.ANNUAL:
            self._discount = 15  # 15% discount for renewal
        elif discount_type == "Group Discount" and self._ticket_type == TicketType.GROUP and group_size >= 20:
            self._discount = 20  # 20% discount for groups of 20 or more
        else:
            self._discount = 0  # No discount by default

# Calculate the final price of the ticket after applying the discount.
    def calculate_final_price(self):
        return self._price * (1 - self._discount / 100)# Final price as a float


# Activate the ticket by setting its status to ACTIVE.
    def activate_ticket(self):
        self.set_status(TicketStatus.ACTIVE)


# Expire the ticket by setting its status to EXPIRED.
    def expire_ticket(self):
        self.set_status(TicketStatus.EXPIRED)


# Cancel the ticket by setting its status to CANCELLED.
    def cancel_ticket(self):
        self.set_status(TicketStatus.CANCELLED)

# Check if the ticket is still valid
    def is_valid(self):
        valid_until = self._purchase_date + timedelta(days=self._validity_period)
        return datetime.now() <= valid_until

# Validate if the ticket is still valid based on the purchase date and validity period.
    def validate_ticket(self):
        if not self.is_valid():
            self.expire_ticket()
            return "Expired"
        else:
            valid_until = self._purchase_date + timedelta(days=self._validity_period)
            remaining_time = valid_until - datetime.now()
            return f"Valid: {remaining_time.days} days, {remaining_time.seconds // 3600} hours remaining"


# String representation of the Ticket in a clear readable way
    def __str__(self):
        return f"Ticket(ID: {self._ticket_id}, Type: {self._ticket_type.value}, Price: {self._price:.2f}, Status: {self._status.value})"


# Represents a customer in the theme park system
class Guest:
    def __init__(self, guest_id, name, email, phone_number, age=None):
        # Initialize a Customer attributes
        self._guest_id = guest_id  # protected attribute to store customer Unique ID
        self._name = name  # protected Customer name
        self._email = email  # protected Customer email
        self._phone_number = phone_number  # protected Customer phone number
        self._age = age #protected age for validation (specific to child tickets)
        self._purchase_history = []  #protected List of tickets purchased by the guest


    #Getters and Setters  for Guest attributes
    def get_guest_id(self):
        return self._guest_id
    def set_guest_id(self, guest_id):
        self._guest_id = guest_id

    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name

    def get_email(self):
        return self._email
    def set_email(self, email):
        if "@" not in email:
            raise ValueError("Invalid email address.")
        self._email = email

    def get_phone_number(self):
        return self._phone_number
    def set_phone_number(self, phone_number):
        self._phone_number = phone_number

    def get_age(self):
        return self._age
    def set_age(self, age):
        if age is not None and age < 0:
            raise ValueError("Age must be a positive integer.")
        self._age = age

    def get_purchase_history(self):
        return self._purchase_history

# Method to view the purchase history -view all tickets in the guest's purchase history
    def view_purchase_history(self):
        if not self._purchase_history:
            print("No tickets in purchase history.")
            return []
        print("Purchase History:")
        for ticket in self._purchase_history:
            print(ticket)
        return self._purchase_history

    # Create an account for the guest
    def create_account(self, name, email, phone_number, age=None):
        self.set_name(name)
        self.set_email(email)
        self.set_phone_number(phone_number)
        self.set_age(age)
        print(f"Account created successfully for Guest: {self._name}!")

# Book a ticket
    def book_ticket(self, ticket_type, price, validity_period, discount=0.0, group_size=0):
        # Validate age for child ticket
        if ticket_type == TicketType.CHILD and (self._age is None or not (3 <= self._age <= 12)):
            raise ValueError("Child tickets can only be purchased for guests aged 3 to 12.")

        # Create a new ticket for the Guest and add it to their purchase history.
        ticket = Ticket(ticket_type, price, validity_period, discount=0.0)  # Create a new Ticket
        ticket.apply_discount("Group Discount", group_size)  # Apply group discount if applicable
        self._purchase_history.append(ticket)  # Add the ticket to the Guest's purchase history
        return ticket  # Return the booked Ticket


    # String representation of the Guest in a clear readable way
    def __str__(self):
        return f"Guest(ID: {self._guest_id}, Name: {self._name}, Email: {self._email}, Age: {self._age})"


class Reservation:
    def __init__(self, reservation_id,  tickets, admin): #Initialize Reservation with composition of Guest
        self._reservation_id = reservation_id #protected Reservation unique ID
        self._reservation_date = date.today()  #protected Automatically set reservation date
        self._guest = None # protected Composition: Create a Guest
        self._tickets = tickets  #protected Aggregation: Tickets are associated with Reservation
        self._total_amount = self.calculate_total_amount()  # Automatically calculate total amount
        self._payment = None  #protected Aggregation: Payment will be associated later
        self._admin = admin  #protected Association: Admin object is associated for reservation management

    # Getters and setter for reservation attributes
    def get_reservation_id(self):
        return self._reservation_id

    def get_reservation_date(self):
        return self._reservation_date
    def set_reservation_date(self, reservation_date):
        self._reservation_date = reservation_date

    def get_tickets(self):
        return self._tickets
    def set_tickets(self, tickets):
        self._tickets = tickets
        self._total_amount = self.calculate_total_amount()  # Recalculate total amount when tickets are updated

    def get_guest(self):
        return self._guest
    def set_guest(self, guest):
        if isinstance(guest, Guest): # Ensure the provided object is a Guest
            self._guest = guest
        else:
            raise ValueError("Invalid Guest object provided.")

    # Create a Guest object as part of the Reservation (Composition)
    def create_guest(self, name, email, phone_number):
        return Guest(self._reservation_id, name, email, phone_number)  # Guest ID same as Reservation ID

    # Calculate the total amount by summing the prices of all tickets
    def calculate_total_amount(self):
        return sum(ticket.get_price() for ticket in self._tickets)

# Add a single ticket to the reservation - add a new ticket to the reservation
    def add_ticket(self, ticket):
        self._tickets.append(ticket)
        self._total_amount = self.calculate_total_amount()  # Update total amount

#Sets a payment for the reservation (Aggregation).
    def set_payment(self, payment):
        if isinstance(payment, Payment): # Ensure the provided object is a Payment
            self._payment = payment
        else:
            raise ValueError("Invalid payment object provided.")

    # Update reservation details by adding a new ticket
    def update_reservation(self, ticket):
        self.add_ticket(ticket)

# Generate a summary invoice for the reservation
    def generate_invoice(self):
        ticket_summary = "\n".join(
            [f"Ticket ID: {ticket.get_ticket_id()}, Price: {ticket.get_price()}" for ticket in self._tickets])
        payment_status = f"Payment Amount: {self._payment.get_amount_paid()}" if self._payment else "Payment: Not made yet"
        return (
            f"--- Invoice ---\n"
            f"Reservation ID: {self._reservation_id}\n"
            f"Reservation Date: {self._reservation_date}\n"
            f"Guest: {self._guest}\n"
            f"Tickets:\n{ticket_summary}\n"
            f"Total Amount: {self._total_amount}\n"
            f"{payment_status}\n"
            f"Admin in Charge: {self._admin.get_name()} ({self._admin.get_email()})"
        )

#Returns a string representation of the Reservation, showing all details easy to read.
    def __str__(self):
        ticket_details = ", ".join([str(ticket) for ticket in self._tickets])
        return (
            f"Reservation(ID: {self._reservation_id}, Date: {self._reservation_date}, "
            f"Guest: {self._guest}, Tickets: [{ticket_details}], Total: {self._total_amount})"
        )

# Represents an admin managing the theme park system
class Admin:
    def __init__(self, admin_id, name, email): # Initialize admin attributes
        self._admin_id = admin_id #protected admin id
        self._name = name #protected admin name
        self._email = email #protected admin email

        # Ensure admin ID is an integer
        if not isinstance(admin_id, int):
            raise TypeError("admin_id must be an integer")


    # Getters and setters for admin attributes
    def get_admin_id(self):
        return self._admin_id

    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name

    def get_email(self):
        return self._email
    def set_email(self, email):
        self._email = email

    def create_account(self, name, email):
        self.set_name(name)
        self.set_email(email)
        print(f"Account created successfully for Admin: {self._name}!")

    # View ticket sales by returning a summary of sold tickets
    def view_ticket_sales(self, tickets):
        if not tickets:
            return "No tickets sold yet."
        return "\n".join(str(ticket) for ticket in tickets)

    # Manage discounts for a specific ticket type
    def manage_discounts(self, ticket_type, discount_percentage):
        print(f"Discount of {discount_percentage}% applied to {ticket_type.value} tickets.")

    # Update the capacity of a specific attraction
    def update_capacity(self, attraction_id, new_capacity):
        # Simulate updating capacity
        print(f"Attraction ID {attraction_id} capacity updated to {new_capacity}.")

    # String representation of Admin easy to read
    def __str__(self):
        return f"Admin(ID: {self._admin_id}, Name: {self._name}, Email: {self._email})"

#Base class for all services in the theme park.
class Services:
    def __init__(self, service_id, service_name, service_description):
        self._service_id = service_id #protected Unique ID for the service
        self._service_name = service_name #protected Name of the service
        self._service_description = service_description #protected Description of the service

    # Getters and Setters for service attributes
    def get_service_id(self):
        return self._service_id
    def set_service_id(self, service_id):
        self._service_id = service_id

    def get_service_name(self):
        return self._service_name
    def set_service_name(self, service_name):
        self._service_name = service_name

    def get_service_description(self):
        return self._service_description
    def set_service_description(self, service_description):
        self._service_description = service_description

    # String representation of Services easy to read
    def __str__(self):
        return f"Service(ID: { self._service_id}, Name: {self._service_name}, Description: {self._service_description})"


#Represents an attraction in the theme park.
class Attraction(Services):
    def __init__(self, attraction_id , attraction_name, service_id, service_name, location, service_description):
        super().__init__(service_id, service_name, service_description) # shows that it inherits from the service class
        self._attraction_id = attraction_id #protected Unique ID for the attraction
        self._attraction_name = attraction_name #protected Name of the attraction
        self._location = location  #protected Specific location of the attraction

    # Getter and Setter for attraction-specific attributes
    def get_attraction_id(self):
        return self._attraction_id
    def set_attraction_id(self, attraction_id):
        self._attraction_id = attraction_id

    def get_attraction_name(self):
        return self._attraction_name
    def set_attraction_attraction_name(self, attraction_name):
        self._attraction_name = attraction_name

    def get_location(self):
        return self._location
    def set_location(self, location):
        self._location = location

    # String representation of Attraction easy to read
    def __str__(self):
        return f"Attraction(ID: {self._attraction_id}, Name: {self._attraction_name}, Location: {self._location})"

#Represents an event in the theme park.
class Event(Services):
    def __init__(self, service_id, service_name, service_description, event_id, event_name, event_date):
        # Initialize attributes from the Service class
        super().__init__(service_id, service_name, service_description) #Shows that it inherits from the service class
        self._event_id = event_id  #protected Unique ID for the event
        self._event_name = event_name  #protected Name of the event
        self._event_date = event_date  #protected Date of the event

    # Getters and setters for event attributes
    def get_event_id(self):
        return self._event_id
    def set_event_id(self, event_id):
        self._event_id = event_id

    def get_event_name(self):
        return self._event_name
    def set_event_name(self, event_name):
        self._event_name = event_name

    def get_event_date(self):
        return self._event_date
    def set_event_date(self, event_date):
        self._event_date = event_date

    # String representation of Event easy to read
    def __str__(self):
        return f"Event(ID: {self._event_id}, Name: {self._event_name}, Date: {self._event_date})"

# Represents a payment made for reservations or tickets
class Payment:
    def __init__(self, payment_id, amount_paid, payment_method: PaymentMethod):
        self._payment_id = payment_id  #protected Unique ID for the payment
        self._amount_paid = amount_paid  #protected Total amount paid
        self._payment_date = date.today()  #protected Automatically set payment date
        self._payment_method = payment_method  #protected Payment method (enum)

    # Getters and setters for payment attributes
    def get_payment_id(self):
        return self._payment_id

    def get_amount_paid(self):
        return self._amount_paid

    def get_payment_date(self):
        return self._payment_date

    def get_payment_method(self):
        return self._payment_method
    def set_payment_method(self, payment_method: PaymentMethod):
        # Update the payment method and ensure it's a valid enum
        if not isinstance(payment_method, PaymentMethod):
            raise ValueError("Invalid payment method. Must be a PaymentMethod enum.")
        self._payment_method = payment_method

    # Processes a payment by adding the given amount to the total amount paid
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        self._amount_paid += amount
        return self._amount_paid

# Issues a refund for a reservation
    def issue_refund(self, reservation_id, refund_amount):
        if refund_amount <= 0:
            raise ValueError("Refund amount must be greater than zero.")
        if refund_amount > self._amount_paid:
            raise ValueError("Refund amount exceeds the total amount paid.")
        self._amount_paid -= refund_amount
        return f"Refund of ${refund_amount:.2f} issued for Reservation ID: {reservation_id}"

    # String representation of Payment easy to read
    def __str__(self):
        return f"Payment(ID: {self._payment_id}, Amount Paid: ${self._amount_paid:.2f}, Date: {self._payment_date})"
#End of models.py

# Next part: Implement data_layer.py to handle file storage.