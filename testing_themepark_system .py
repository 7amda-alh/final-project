import unittest
import os
from models import *
from data_layer import DataLayer
from business_logic import BusinessLogic


class TestThemeParkSystem(unittest.TestCase):
    """Unit tests for the Theme Park Management System"""

    def setUp(self):
        """Set up a clean testing environment before each test case."""
        data_layer = DataLayer()
        for file_key in data_layer.files.keys():
            if os.path.exists(data_layer.files[file_key]):
                os.remove(data_layer.files[file_key])

        if "attraction_id" not in data_layer.id_counters:
            data_layer.id_counters["attraction_id"] = 1
        if "event_id" not in data_layer.id_counters:
            data_layer.id_counters["event_id"] = 1
        data_layer.save_id_counters()

        self.business_logic = BusinessLogic()

    def test_guest_creation(self):
        guest = self.business_logic.add_guest("Hamda", "hamda@example.com", "123-456-7890")
        self.assertEqual(guest.get_name(), "Hamda")
        self.assertEqual(guest.get_email(), "hamda@example.com")
        self.assertEqual(guest.get_phone_number(), "123-456-7890")

    def test_ticket_creation(self):
        guest = self.business_logic.add_guest("Fatima", "fatima@example.com", "111-222-3333")
        ticket = self.business_logic.add_ticket_to_guest(
            guest.get_guest_id(), TicketType.SINGLE_DAY, 275, 1
        )
        self.assertEqual(ticket.get_ticket_type(), TicketType.SINGLE_DAY)
        self.assertEqual(ticket.get_price(), 275)

    def test_admin_creation(self):
        admin = self.business_logic.add_admin("Mariam", "mariam@example.com")
        self.assertEqual(admin.get_name(), "Mariam")
        self.assertEqual(admin.get_email(), "mariam@example.com")

    def test_ticket_discount_application(self):
        self.business_logic.modify_ticket_discount(TicketType.TWO_DAY, 20)
        ticket_details = Ticket.TICKET_DETAILS[TicketType.TWO_DAY]
        self.assertEqual(ticket_details["discount"], 20)

    def test_payment_processing(self):
        guest = self.business_logic.add_guest("Hamda", "hamda@example.com", "123-456-7890")
        ticket = self.business_logic.add_ticket_to_guest(
            guest.get_guest_id(), TicketType.ANNUAL, 1840, 365
        )
        reservation = self.business_logic.make_reservation(guest.get_guest_id(), [ticket])

        payment = self.business_logic.process_payment(
            reservation.get_reservation_id(), 1840, PaymentMethod.CREDIT_CARD
        )
        self.assertEqual(payment.get_amount_paid(), 1840)

    def test_reservation_creation(self):
        guest = self.business_logic.add_guest("Fatima", "fatima@example.com", "123-123-1234")
        tickets = [
            self.business_logic.add_ticket_to_guest(guest.get_guest_id(), TicketType.SINGLE_DAY, 275, 1),
            self.business_logic.add_ticket_to_guest(guest.get_guest_id(), TicketType.TWO_DAY, 480, 2),
        ]
        reservation = self.business_logic.make_reservation(guest.get_guest_id(), tickets)
        self.assertEqual(len(reservation.get_tickets()), 2)
        self.assertEqual(reservation.calculate_total_amount(), 755)

    def test_admin_discount_modification(self):
        self.business_logic.modify_ticket_discount(TicketType.GROUP, 30)
        ticket_details = Ticket.TICKET_DETAILS[TicketType.GROUP]
        self.assertEqual(ticket_details["discount"], 30)

    def test_guest_view_purchase_history(self):
        guest = self.business_logic.add_guest("Mariam", "mariam@example.com", "987-654-3210")
        ticket = self.business_logic.add_ticket_to_guest(
            guest.get_guest_id(), TicketType.CHILD, 185, 1
        )
        guest.get_purchase_history().append(ticket)
        history = guest.get_purchase_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].get_ticket_type(), TicketType.CHILD)

    def test_ticket_status_updates(self):
        guest = self.business_logic.add_guest("Ali", "ali@example.com", "999-888-7777")
        ticket = self.business_logic.add_ticket_to_guest(
            guest.get_guest_id(), TicketType.VIP, 550, 1
        )
        ticket.cancel_ticket()
        self.assertEqual(ticket.get_status(), TicketStatus.CANCELLED)

    def test_attraction_management(self):
        """Test Attraction Management."""
        attraction = self.business_logic.add_attraction(
            attraction_name="Roller Coaster",
            location="Zone A",
            service_description="High-speed thrill ride",
        )
        attractions = self.business_logic.get_all_attractions()
        matching_attraction = next(
            (a for a in attractions if a.get_attraction_name() == "Roller Coaster" and a.get_location() == "Zone A"),
            None
        )
        self.assertIsNotNone(matching_attraction, "The attraction was not found in the retrieved list.")

    def test_event_management(self):
        """Test Event Management."""
        event = self.business_logic.add_event(
            event_name="Fireworks Show",
            event_date="2024-12-25",
            service_description="Annual celebration",
        )
        events = self.business_logic.get_all_events()
        matching_event = next(
            (e for e in events if e.get_event_name() == "Fireworks Show" and e.get_event_date() == "2024-12-25"),
            None
        )
        self.assertIsNotNone(matching_event, "The event was not found in the retrieved list.")


    def test_payment_methods(self):
        guest = self.business_logic.add_guest("Hamda", "hamda@example.com", "123-456-7890")
        ticket = self.business_logic.add_ticket_to_guest(
            guest.get_guest_id(), TicketType.SINGLE_DAY, 275, 1
        )
        reservation = self.business_logic.make_reservation(guest.get_guest_id(), [ticket])
        payment = self.business_logic.process_payment(
            reservation.get_reservation_id(), 275, PaymentMethod.CREDIT_CARD
        )

        updated_payment = self.business_logic.update_payment_method(
            payment.get_payment_id(), PaymentMethod.DIGITAL_WALLET
        )
        self.assertEqual(updated_payment.get_payment_method(), PaymentMethod.DIGITAL_WALLET)


if __name__ == "__main__":
    unittest.main()
