from models import *  # Import all models like Guest, Ticket, Reservation, etc.
from data_layer import DataLayer  # Import the DataLayer for data management


class BusinessLogic:
    def __init__(self):
        # Initialize the DataLayer instance for handling data persistence
        self.data_layer = DataLayer()
        # Load all guests from the data layer
        self.guests = self.data_layer.get_all_guests()
        # Load all tickets from the data layer
        self.tickets = self.data_layer.get_all_tickets()
        # Load all reservations from the data layer
        self.reservations = self.data_layer.get_all_reservations()

    def generate_unique_guest_id(self):
        # Generate a unique ID for a guest using the data layer
        return self.data_layer.get_next_id("guest_id")

    def generate_unique_ticket_id(self):
        # Generate a unique ID for a ticket using the data layer
        return self.data_layer.get_next_id("ticket_id")

    def generate_unique_admin_id(self):
        # Generate a unique ID for an admin using the data layer
        return self.data_layer.get_next_id("admin_id")


    def add_guest(self, name, email, phone):
        guest_id = self.generate_unique_guest_id()  # Generate a unique guest ID
        new_guest = Guest(guest_id, name, email, phone)  # Create a new guest
        self.guests.append(new_guest)  # Add the guest to the list
        self.data_layer.save_guest(new_guest)  # Save the guest
        return new_guest

    def add_ticket_to_guest(self, guest_id, ticket_type, price, validity_period=1):
        # Validate that the price is numeric
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a numeric value.")
        # Validate that the ticket type is an instance of TicketType enum
        if not isinstance(ticket_type, TicketType):
            raise ValueError("Invalid ticket type.")

        # Find the guest by ID
        guest = next((g for g in self.guests if g.get_guest_id() == guest_id), None)
        if not guest:
            raise ValueError(f"Guest with ID {guest_id} not found.")

        # Create a new ticket and associate it with the guest
        new_ticket = Ticket(
            ticket_type=ticket_type,
            price=price,
            validity_period=validity_period,
            guest_id=guest_id,  # Associate ticket with the guest ID
        )
        # Add the ticket to the in-memory list
        self.tickets.append(new_ticket)

        # Save the ticket in the data layer
        self.data_layer.save_ticket(new_ticket)

        # Return the ticket for further use if needed
        return new_ticket

    def get_tickets_by_guest(self, guest_id):
        # Retrieve all tickets associated with the given guest ID
        return [t for t in self.tickets if t.get_guest_id() == guest_id]


    def get_all_guests(self):
        # Retrieve all guests from the in-memory list
        return self.guests

    def update_guest(self, guest):
        # Update guest information in the in-memory list and save it in the data layer
        for idx, g in enumerate(self.guests): # Loop through the list of guests with both the index (idx) and the guest object (g)
            if g.get_guest_id() == guest.get_guest_id():
                # Update the guest in the list at the found index
                self.guests[idx] = guest
                # Save the updated guest to the data layer for persistence
                self.data_layer.save_guest(guest)
                # Exit the function once the update is complete
                return
            # If no matching guest is found, raise an error indicating the guest was not found
        raise ValueError("Guest not found.")

    def delete_guest(self, guest_id):
        # Delete a guest and their associated tickets
        self.guests = [g for g in self.guests if g.get_guest_id() != guest_id]
        self.data_layer.save_data("guests", self.guests)  # Save updated guests list
        self.tickets = [t for t in self.tickets if t.get_guest_id() != guest_id]
        self.data_layer.save_data("tickets", self.tickets)  # Save updated tickets list


    def get_tickets_by_guest(self, guest_id):
        # Use a list comprehension to filter tickets based on the guest ID
        return [t for t in self.tickets if t.get_guest_id() == guest_id]

    # Business Logic for Tickets
    def create_ticket(self, ticket_type, price, validity_period, discount=0):
        # Create a new ticket and save it in the data layer
        ticket_id = self.data_layer.get_next_id("ticket_id")  # Generate unique ticket ID
        ticket = Ticket(ticket_type, price, validity_period, discount)
        self.data_layer.save_ticket(ticket)
        return ticket


    def get_all_tickets(self):
        # Retrieve all tickets from the data layer
        return self.data_layer.get_all_tickets()

    # Business Logic for Reservations
    def make_reservation(self, guest_id, tickets):
        # Create a new reservation for a guest
        reservation_id = self.data_layer.get_next_id("reservation_id")  # Generate unique reservation ID
        guest = next(
            (g for g in self.data_layer.get_all_guests() if g.get_guest_id() == guest_id), None
        )
        if not guest:
            raise ValueError(f"Guest with ID {guest_id} does not exist.")

        # Create a new reservation object
        reservation = Reservation(reservation_id, tickets, guest)
        # Save the reservation in the data layer
        self.data_layer.save_reservation(reservation)
        # Return the reservation object
        return reservation


    def get_all_reservations(self):
        # Retrieve all reservations from the data layer
        return self.data_layer.get_all_reservations()

    # Business Logic for Admins
    def add_admin(self, name, email):
        # Add a new admin and save them in the data layer
        admin_id = self.data_layer.get_next_id("admin_id")  # Generate a unique Admin ID
        new_admin = Admin(admin_id, name, email)  # Create an Admin object
        self.data_layer.save_admin(new_admin)  # Save the Admin to the data layer
        return new_admin  # Return the Admin object for use in the application

    def get_all_admins(self):
        # Retrieve all admins from the data layer
        admins = self.data_layer.get_all_admins()
        return admins

    def modify_ticket_discount(self, ticket_type, discount):
        # Modify the discount for a specific ticket type
        if not isinstance(ticket_type, TicketType):
            raise ValueError("Invalid ticket type.")
        if not (0 <= discount <= 100):
            raise ValueError("Discount must be between 0 and 100.")

        # Update discount in the ticket details dictionary
        if ticket_type in Ticket.TICKET_DETAILS:
            Ticket.TICKET_DETAILS[ticket_type]["discount"] = discount

        # Update existing tickets with the new discount
        tickets = self.data_layer.get_all_tickets()
        for ticket in tickets:
            if ticket.get_ticket_type() == ticket_type:
                ticket.set_discount(discount)
        self.data_layer.save_data("tickets", tickets)


    # Business Logic for Attractions
    def add_attraction(self, attraction_name, location, service_description):
        # Add a new attraction and save it in the data layer
        attraction_id = self.data_layer.get_next_id("attraction_id")  # Generate unique attraction ID
        attraction = Attraction(
            attraction_id=attraction_id,
            attraction_name=attraction_name,
            location=location,
            service_id=attraction_id,  # Assuming service_id is the same as attraction_id
            service_name=attraction_name,
            service_description=service_description,
        )
        self.data_layer.save_attraction(attraction)
        return attraction

    def get_all_attractions(self):
        # Retrieve all attractions from the data layer
        return self.data_layer.get_all_attractions()

    # Business Logic for Events
    def add_event(self, event_name, event_date, service_description):
        # Add a new event and save it in the data layer
        event_id = self.data_layer.get_next_id("event_id")  # Generate unique event ID
        event = Event(
            service_id=event_id,  # Assuming service_id is the same as event_id
            service_name=event_name,
            service_description=service_description,
            event_id=event_id,
            event_name=event_name,
            event_date=event_date,
        )
        self.data_layer.save_event(event)
        return event

    def get_all_events(self):
        # Retrieve all events from the data layer
        return self.data_layer.get_all_events()

    # Business Logic for Payments
    def process_payment(self, reservation_id, amount_paid, payment_method: PaymentMethod):
        # Process a payment for a reservation.
        if not isinstance(payment_method, PaymentMethod):
            raise ValueError("Invalid payment method. Must be a PaymentMethod enum.")

        # Find the reservation by ID
        reservations = self.data_layer.get_all_reservations()
        reservation = next(
            (r for r in reservations if r.get_reservation_id() == reservation_id), None
        )
        if not reservation:
            raise ValueError(f"Reservation with ID {reservation_id} does not exist.")

        # Create and save the payment
        payment_id = self.data_layer.get_next_id("payment_id")  # Generate unique payment ID
        payment = Payment(payment_id, amount_paid, payment_method)

        # Associate the payment with the reservation
        reservation.set_payment(payment)
        # Save the updated reservation and payment in the data layer
        self.data_layer.save_reservation(reservation)
        self.data_layer.save_payment(payment)
        # Return the payment object
        return payment

    def update_payment_method(self, payment_id, new_payment_method: PaymentMethod):
        # Update the payment method for a specific payment
        if not isinstance(new_payment_method, PaymentMethod):
            raise ValueError("Invalid payment method. Must be a PaymentMethod enum.")
        return self.data_layer.update_payment_method(payment_id, new_payment_method)

    def get_all_payments(self):
        # Retrieve all payments from the data layer
        return self.data_layer.get_all_payments()

    # Business Logic for Services
    def add_service(self, name, description):
        # Add a new service and save it in the data layer
        service_id = self.data_layer.get_next_id("service_id")  # Generate unique service ID
        service = Services(service_id, name, description)
        self.data_layer.save_service(service)
        return service

    def get_all_services(self):
        # Retrieve all services from the data layer
        return self.data_layer.get_all_services()

# Next part: Implement themepark_app.py to handle file storage.