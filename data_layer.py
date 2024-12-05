import pickle  # For data serialization and deserialization
import os  # For file operations
from models import *  # Import all models


class DataLayer:
    def __init__(self):
        # Define file paths for all models
        self.files = {
            "guests": "data/guests.pkl",  # File path for guest data
            "tickets": "data/tickets.pkl",  # File path for ticket data
            "reservations": "data/reservations.pkl",  # File path for reservation data
            "admins": "data/admins.pkl",  # File path for admin data
            "payments": "data/payments.pkl",  # File path for payment data
            "attractions": "data/attractions.pkl",  # File path for attraction data
            "events": "data/events.pkl",  # File path for event data
            "services": "data/services.pkl",  # File path for services data
        }

        # Auto-incrementing ID counters
        self.id_counters = {
            "guest_id": 1,  # Counter for guest IDs
            "ticket_id": 1,  # Counter for ticket IDs
            "reservation_id": 1,  # Counter for reservation IDs
            "payment_id": 1,  # Counter for payment IDs
            "admin_id": 1,  # Counter for admin IDs
        }

        # Create data directory if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")# Create the "data" director

        # Load ID counters from the persistent storage
        self.load_id_counters()

    def save_id_counters(self):
        # Save the current state of ID counters to a file for persistence
        with open("data/id_counters.pkl", "wb") as file:
            pickle.dump(self.id_counters, file)

    def load_id_counters(self):
        # Load ID counters from a file, ensuring the admin ID exists
        if os.path.exists("data/id_counters.pkl"):
            with open("data/id_counters.pkl", "rb") as file:
                self.id_counters = pickle.load(file)

        # Ensure admin_id counter is always initialized
        if "admin_id" not in self.id_counters:
            self.id_counters["admin_id"] = 1

    def get_next_id(self, id_type):
        #Generate the next unique ID for a given type
        if id_type not in self.id_counters:
            print(self.id_counters)  # Debug: Print current id_counters state
            raise ValueError(f"Invalid ID type: {id_type}")
        current_id = self.id_counters[id_type]  # Get the current ID
        self.id_counters[id_type] += 1  # Increment the counter
        self.save_id_counters()  # Save updated counters
        return int(current_id)  # Return the generated ID

    def load_data(self, file_key):
        # Load data from the specified file
        file_path = self.files[file_key]
        try:
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    return pickle.load(file) # Return deserialized data
            else:
                return []  # Return an empty list if the file doesn't exist
        except (EOFError, pickle.PickleError) as e:
            print(f"Error reading file {file_path}: {e}") # Handle errors gracefully
            return []  # Return an empty list if there’s an error

    def save_data(self, file_key, data):
        # Save data to the specified file
        file_path = self.files[file_key]  # Get file path
        try:
            with open(file_path, "wb") as file:
                pickle.dump(data, file) # Serialize and save data
        except pickle.PickleError as e:
            print(f"Error writing to file {file_path}: {e}") # Handle save errors

    def validate_instance(self, obj, cls):
        # Validate that the given object is an instance of a specified class
        if not isinstance(obj, cls):
            raise TypeError(f"Expected an instance of {cls.__name__}, got {type(obj).__name__}.")

    # CRUD Methods
    def add_object(self, file_key, obj, cls):
        # Add an object to the specified file
        self.validate_instance(obj, cls)  # Ensure object is valid
        data = self.load_data(file_key)  # Load existing data
        data.append(obj)  # Add the new object
        self.save_data(file_key, data)  # Save updated data

    def get_all_objects(self, file_key):
        # Retrieve all objects from the specified file
        return self.load_data(file_key)

    # Specialized CRUD Methods
    def save_guest(self, guest):
        # Save a guest object to the persistent storage
        if not isinstance(guest.get_guest_id(), int): # Validate guest ID
            raise TypeError("Guest ID must be an integer.")
        self.add_object("guests", guest, Guest)

    def get_all_guests(self):
        # Retrieve all guest objects and ensure attributes are initialized
        guests = self.get_all_objects("guests")
        for guest in guests:
            # Manually initialize missing attributes to avoid AttributeError
            if "_guest_id" not in vars(guest):  # Ensure _guest_id is set
                guest._guest_id = self.get_next_id("guest_id")
            if "_name" not in vars(guest):  # Ensure name is set
                guest._name = "Unknown"
            if "_email" not in vars(guest):  # Ensure email is set
                guest._email = "unknown@example.com"
            if "_phone_number" not in vars(guest):  # Ensure phone_number is set
                guest._phone_number = "000-000-0000"
            if "_age" not in vars(guest):  # Ensure age is set
                guest._age = None
            if "_purchase_history" not in vars(guest):  # Ensure purchase_history is initialized
                guest._purchase_history = []

        return guests

    def save_ticket(self, ticket):
        # Save a ticket object to persistent storage
        if not isinstance(ticket.get_guest_id(), int):  # Validate guest ID
            raise ValueError("Ticket must have a valid guest ID as an integer.")
        self.add_object("tickets", ticket, Ticket)

    def get_all_tickets(self):
        # Retrieve all ticket objects and ensure attributes are initialized
        tickets = self.get_all_objects("tickets")  # Load tickets from storage
        for ticket in tickets:
            if "_guest_id" not in vars(ticket):  # # Ensure guest ID is set
                ticket._guest_id = None  # Default value for missing guest ID
        return tickets


    def save_reservation(self, reservation):
        # Save a reservation object
        self.add_object("reservations", reservation, Reservation)

    def get_all_reservations(self):
        # Retrieve all reservation objects
        return self.get_all_objects("reservations")

    def save_admin(self, admin):
        # Save an admin object
        self.add_object("admins", admin, Admin)

    def get_all_admins(self):
        # Retrieve all admin objects and ensure attributes are initialized
        admins = self.get_all_objects("admins")  # Load all admin objects from persistent storage
        for admin in admins:
            # `hasattr` checks if the admin object has a specific attribute.
            # If the attribute doesn't exist, it adds and initializes it to avoid errors.
            if not hasattr(admin, "_admin_id"):  # Check if `_admin_id` attribute exists
                admin._admin_id = self.get_next_id("admin_id")  # Initialize `_admin_id` if missing
            if not hasattr(admin, "_email"):  # Check if `_email` attribute exists
                admin._email = "unknown@example.com"  # Initialize `_email` if missing
            if not hasattr(admin, "_name"):  # Check if `_name` attribute exists
                admin._name = "Unknown Admin"  # Initialize `_name` if missing
        return admins  # Return the list of admin objects


    def save_attraction(self, attraction):
        # Save an attraction object
        self.add_object("attractions", attraction, Attraction)

    def get_all_attractions(self):
        # Retrieve all attraction objects
        return self.get_all_objects("attractions")

    def save_event(self, event):
        # Save an event object
        self.add_object("events", event, Event)

    def get_all_events(self):
        # Retrieve all event objects
        return self.get_all_objects("events")

    def save_payment(self, payment):
        # Save a payment object
        self.add_object("payments", payment, Payment)

    def get_all_payments(self):
        # Retrieve all payment objects
        return self.get_all_objects("payments")

    def update_payment_method(self, payment_id, new_payment_method: PaymentMethod):
        # Update the payment method for a specific payment
        payments = self.get_all_payments()
        for payment in payments:
            if payment.get_payment_id() == payment_id:  # Find matching payment
                payment.set_payment_method(new_payment_method)  # Update method
                self.save_data("payments", payments)  # Save updated payments
                return payment
        raise ValueError(f"Payment with ID {payment_id} not found.")  # Raise error if not found

    def delete_payment(self, payment_id):
        # Delete a payment object by its ID
        payments = self.get_all_payments()
        updated_payments = [p for p in payments if p.get_payment_id() != payment_id]  # Exclude matching ID
        if len(payments) == len(updated_payments):  # No deletion occurred
            raise ValueError(f"Payment with ID {payment_id} not found.")
        self.save_data("payments", updated_payments)  # Save updated payments


    def save_service(self, service):
        # Save a service object
        self.add_object("services", service, Services)

    def get_all_services(self):
        # Retrieve all service objects from persistent storage
        return self.get_all_objects("services")

    def refresh_data(self):
        # Reload in-memory data from the data layer to reflect the latest updates
        self.guests = self.data_layer.get_all_guests()  # Refresh guest data
        self.tickets = self.data_layer.get_all_tickets()  # Refresh ticket data
        self.reservations = self.data_layer.get_all_reservations()  # Refresh reservation data

# Next part: Implement business_logic.py to handle file storage.