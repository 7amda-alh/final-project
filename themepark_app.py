import tkinter as tk  # Import tkinter for GUI creation
from tkinter import messagebox # Import messagebox for showing pop-up alerts
from models import *  # Import all models
from business_logic import BusinessLogic  # Import business logic class for backend operations




class App:
   def __init__(self, root):
       # Initialize the main application window
       self.root = root
       self.root.title("Theme Park Management System") # Set the title of the application
       self.root.geometry("900x900") # Set the dimensions of the window


       self.business_logic = BusinessLogic() # Create an instance of BusinessLogic
       self.guest = None # Initialize the current guest as None
       self.admin = None # Initialize the current admin as None


       # Mapping for user-friendly ticket names to backend ticket types enum
       self.ticket_type_mapping = {
           "Single-Day Pass": "SINGLE_DAY",
           "Two-Day Pass": "TWO_DAY",
           "Annual Membership": "ANNUAL",
           "Child Ticket": "CHILD",
           "Group Ticket": "GROUP",
           "VIP Experience Pass": "VIP",
       }


       self.role_selection_screen()  # Start with the role selection screen


   def role_selection_screen(self):
       # Display the role selection screen
       self.clear_window() # Clear any existing widgets


       # Add a label for role selection
       role_label = tk.Label(self.root, text="Select Your Role", font=("Arial", 16, "bold"))
       role_label.pack(pady=20)


       # Add buttons for Guest and Admin roles
       guest_button = tk.Button(self.root, text="Guest", command=self.login_screen)
       guest_button.pack(pady=10)


       admin_button = tk.Button(self.root, text="Admin", command=self.admin_login_screen)
       admin_button.pack(pady=10)




   def login_screen(self):
       # Display the login screen for guests
       self.clear_window()


       # Add a label for guest login
       login_label = tk.Label(self.root, text="Login as Guest", font=("Arial", 14))
       login_label.pack(pady=20)


       # Add an input field for email
       email_label = tk.Label(self.root, text="Email:")
       email_label.pack(pady=5)


       self.email_entry = tk.Entry(self.root)
       self.email_entry.pack(pady=5)


       # Add buttons for login and account creation
       login_button = tk.Button(self.root, text="Login", command=self.login)
       login_button.pack(pady=10)


       register_button = tk.Button(self.root, text="Create Account", command=self.create_account)
       register_button.pack(pady=10)


       # Add a back button to return to the role selection screen
       back_button = tk.Button(self.root, text="Back", command=self.role_selection_screen)
       back_button.pack(pady=10)


   def create_admin_account_screen(self):
       # Display the screen to create a new admin account
       self.clear_window()


       # Add a label for creating an admin account
       create_label = tk.Label(self.root, text="Create Admin Account", font=("Arial", 14))
       create_label.pack(pady=20)


       # Add input fields for name and email
       name_label = tk.Label(self.root, text="Name:")
       name_label.pack(pady=5)


       self.admin_name_entry = tk.Entry(self.root)
       self.admin_name_entry.pack(pady=5)


       email_label = tk.Label(self.root, text="Email:")
       email_label.pack(pady=5)


       self.admin_email_entry = tk.Entry(self.root)
       self.admin_email_entry.pack(pady=5)


       # Add a button to create the admin account
       create_button = tk.Button(self.root, text="Create Account", command=self.save_admin_account)
       create_button.pack(pady=20)


       # Add a back button to return to the role selection screen
       back_button = tk.Button(self.root, text="Back", command=self.role_selection_screen)
       back_button.pack(pady=10)


   def save_admin_account(self):
       # Save the new admin account details
       name = self.admin_name_entry.get()  # Get the entered name
       email = self.admin_email_entry.get() # Get the entered email


       # Validate that all fields are filled
       if not (name and email):
           messagebox.showerror("Error", "All fields are required.")
           return


       try:
           # Add the admin to the business logic and show success message
           self.admin = self.business_logic.add_admin(name, email)  # Create admin account and generate ID
           messagebox.showinfo("Success", f"Admin account created! Your Admin ID is: {self.admin.get_admin_id()}")
           self.role_selection_screen() # Return to the role selection screen
       except Exception as e:
           # Show an error message if something goes wrong
           messagebox.showerror("Error", f"An error occurred: {str(e)}")


   def admin_login_screen(self):
       # Display the admin login screen
       self.clear_window()


       # Add a label for admin login
       login_label = tk.Label(self.root, text="Login as Admin", font=("Arial", 14))
       login_label.pack(pady=20)


       # Add input fields for email and admin ID
       email_label = tk.Label(self.root, text="Email:")
       email_label.pack(pady=5)


       self.email_entry = tk.Entry(self.root)
       self.email_entry.pack(pady=5)


       admin_id_label = tk.Label(self.root, text="Admin ID:")
       admin_id_label.pack(pady=5)


       self.admin_id_entry = tk.Entry(self.root)
       self.admin_id_entry.pack(pady=5)


       # Add a login button
       login_button = tk.Button(self.root, text="Login", command=self.admin_login)
       login_button.pack(pady=10)


       # Add a button to create a new admin account
       create_admin_button = tk.Button(self.root, text="Create Admin Account",command=self.create_admin_account_screen)
       create_admin_button.pack(pady=10)


       # Add a back button to return to the role selection screen
       back_button = tk.Button(self.root, text="Back", command=self.role_selection_screen)
       back_button.pack(pady=10)


   def admin_login(self):
       # Handle the admin login process
       email = self.email_entry.get() # Get the entered email
       admin_id = self.admin_id_entry.get() # Get the entered admin ID


       try:
           admin_id = int(admin_id)  # Ensure admin_id is an integer.
           admins = self.business_logic.get_all_admins() # Get all admin accounts
           # Find matching admin account
           self.admin = next(
               (a for a in admins if a.get_email() == email and a.get_admin_id() == admin_id), None
           )


           if self.admin:
               # If admin is found, show success message and navigate to the dashboard
               messagebox.showinfo("Login Successful", f"Welcome back, {self.admin.get_name()}!")
               self.admin_dashboard()
           else:
               # If no matching admin is found, show an error message
               messagebox.showerror("Login Failed", "Invalid email or Admin ID.")
       except ValueError:
           # If the admin ID is not numeric, show an error message
           messagebox.showerror("Login Failed", "Admin ID must be a numeric value.")
       except Exception as e:
           # Catch any other exceptions and show an error message
           messagebox.showerror("Error", f"An error occurred: {str(e)}")


   def create_account(self):
       # Display the screen to create a new guest account
       self.clear_window()


       # Add a label for creating an account
       create_label = tk.Label(self.root, text="Create Account", font=("Arial", 14))
       create_label.pack(pady=20)


       # Add input fields for name, email, and phone number
       name_label = tk.Label(self.root, text="Name:")
       name_label.pack(pady=5)


       self.name_entry = tk.Entry(self.root)
       self.name_entry.pack(pady=5)


       email_label = tk.Label(self.root, text="Email:")
       email_label.pack(pady=5)


       self.email_entry = tk.Entry(self.root)
       self.email_entry.pack(pady=5)


       phone_label = tk.Label(self.root, text="Phone Number:")
       phone_label.pack(pady=5)


       self.phone_entry = tk.Entry(self.root)
       self.phone_entry.pack(pady=5)


       # Add a button to create the account
       create_button = tk.Button(self.root, text="Create Account", command=self.save_account)
       create_button.pack(pady=20)


       # Add a back button to return to the login screen
       back_button = tk.Button(self.root, text="Back", command=self.login_screen)
       back_button.pack(pady=10)


   def save_account(self):
       # Save the new guest account details
       name = self.name_entry.get() # Get the entered name
       email = self.email_entry.get() # Get the entered email
       phone = self.phone_entry.get() # Get the entered phone number


       # Validate that all fields are filled
       if not (name and email and phone):
           messagebox.showerror("Error", "All fields are required.") # Show an error if any field is empty
           return


       try:
           # Add the guest to the business logic and show a success message
           self.guest = self.business_logic.add_guest(name, email, phone)
           messagebox.showinfo("Success", f"Welcome, {self.guest.get_name()}! Your account is created.")
           self.main_menu()  # Navigate to the main menu
       except Exception as e:
           # Show an error message if something goes wrong
           messagebox.showerror("Error", f"An error occurred: {str(e)}")




   def login(self):
       # Handle the guest login process
       email = self.email_entry.get() # Get the entered email
       guests = self.business_logic.get_all_guests()# Retrieve all guest accounts


       # Find the matching guest account
       self.guest = next((g for g in guests if g.get_email() == email), None)


       if self.guest:
           # If the guest is found, show a success message and navigate to the main menu
           messagebox.showinfo("Login Successful", f"Welcome back, {self.guest.get_name()}!")
           self.main_menu()
       else:
           # If no matching guest is found, show an error message
           messagebox.showerror("Login Failed", "Invalid email or user does not exist.")


   def main_menu(self):
       # Display the main menu for guests
       self.clear_window()


       # Add a title label for the main menu
       title_label = tk.Label(self.root, text="Theme Park Management System", font=("Arial", 16, "bold"))
       title_label.pack(pady=20)


       # Add buttons for ticket purchasing and account management
       buy_ticket_button = tk.Button(self.root, text="Buy Ticket", command=self.ticket_purchasing_screen)
       buy_ticket_button.pack(pady=10)


       manage_account_button = tk.Button(self.root, text="Manage Account", command=self.manage_account_screen)
       manage_account_button.pack(pady=10)


       # Add an exit button to close the application
       exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
       exit_button.pack(pady=10)


   def manage_account_screen(self):
       # Display the screen for managing the guest account
       self.clear_window()


       # Add a label for managing the account
       manage_label = tk.Label(self.root, text="Manage Account", font=("Arial", 14))
       manage_label.pack(pady=20)


       # Add buttons for modifying account details, deleting the account, and viewing purchase orders
       modify_button = tk.Button(self.root, text="Modify Account Details", command=self.modify_account_screen)
       modify_button.pack(pady=10)


       delete_button = tk.Button(self.root, text="Delete Account", command=self.delete_account)
       delete_button.pack(pady=10)


       view_orders_button = tk.Button(self.root, text="View Purchase Orders", command=self.view_purchase_orders)
       view_orders_button.pack(pady=10)


       # Add a back button to return to the main menu
       back_button = tk.Button(self.root, text="Back", command=self.main_menu)
       back_button.pack(pady=10)


   def delete_account(self):
       # Handle account deletion process
       confirmation = messagebox.askyesno(
           "Confirm Delete", "Are you sure you want to delete your account? This action cannot be undone."
       )


       if confirmation:
           try:
               # Delete the guest using business logic and show success message
               self.business_logic.delete_guest(self.guest.get_guest_id())
               self.guest = None  # Clear the current guest data
               messagebox.showinfo("Account Deleted", "Your account has been deleted successfully.")
               self.login_screen()  # Redirect to the login screen
           except Exception as e:
               # Show an error message if something goes wrong
               messagebox.showerror("Error", f"An error occurred while deleting the account: {str(e)}")


   def modify_account_screen(self):
       # Display the screen for modifying account details
       self.clear_window()


       # Add a label for modifying account details
       modify_label = tk.Label(self.root, text="Modify Account Details", font=("Arial", 14))
       modify_label.pack(pady=20)


       # Add input fields pre-filled with the current guest's details
       name_label = tk.Label(self.root, text="Name:")
       name_label.pack(pady=5)


       self.name_entry = tk.Entry(self.root)
       self.name_entry.insert(0, self.guest.get_name())  # Pre-fill with current name
       self.name_entry.pack(pady=5)


       email_label = tk.Label(self.root, text="Email:")
       email_label.pack(pady=5)


       self.email_entry = tk.Entry(self.root)
       self.email_entry.insert(0, self.guest.get_email())  # Pre-fill with current email
       self.email_entry.pack(pady=5)


       phone_label = tk.Label(self.root, text="Phone Number:")
       phone_label.pack(pady=5)


       self.phone_entry = tk.Entry(self.root)
       self.phone_entry.insert(0, self.guest.get_phone_number())  # Pre-fill with current phone
       self.phone_entry.pack(pady=5)


       # Add a button to update account details
       update_button = tk.Button(self.root, text="Update Details", command=self.update_account)
       update_button.pack(pady=20)


       # Add a back button to return to the account management screen
       back_button = tk.Button(self.root, text="Back", command=self.manage_account_screen)
       back_button.pack(pady=10)


   def update_account(self):
       # Update the guest's account details
       new_name = self.name_entry.get()  # Get the updated name
       new_email = self.email_entry.get()  # Get the updated email
       new_phone = self.phone_entry.get()  # Get the updated phone number


       # Validate that all fields are filled
       if not (new_name and new_email and new_phone):
           messagebox.showerror("Error", "All fields are required.")
           return


       try:
           # Update the guest's details and save the changes
           self.guest.set_name(new_name)
           self.guest.set_email(new_email)
           self.guest.set_phone_number(new_phone)
           self.business_logic.update_guest(self.guest)
           messagebox.showinfo("Success", "Account details updated successfully!")
           self.manage_account_screen() # Return to the account management screen
       except Exception as e:
           # Show an error message if something goes wrong
           messagebox.showerror("Error", f"An error occurred: {str(e)}")

   def view_purchase_orders(self):
       # Display the screen to view the guest's purchase orders
       self.clear_window()

       # Add a label for the purchase orders section
       orders_label = tk.Label(self.root, text="Your Purchase Orders", font=("Arial", 14))
       orders_label.pack(pady=20)

       # Get the guest's purchase orders based on their ID
       guest_id = self.guest.get_guest_id()
       orders = self.business_logic.get_tickets_by_guest(guest_id)

       if not orders:
           # Display a message if no tickets have been purchased yet
           no_orders_label = tk.Label(self.root, text="No tickets purchased yet.", font=("Arial", 12))
           no_orders_label.pack(pady=20)
       else:
           # Create a larger scrollable text widget for the purchase orders
           text_widget = tk.Text(self.root, height=50, width=90, wrap="word", bg="black", fg="white")
           text_widget.pack(pady=10)

           # Populate the text widget with purchase order details
           for order in orders:
               ticket_id = order.get_ticket_id()  # Assuming your Ticket class has a get_ticket_id method
               ticket_type = order.get_ticket_type().value  # Get ticket type
               price = order.get_price()  # Get ticket price
               status = order.get_status()  # Assuming there's a status field in the Ticket
               purchase_date = order.get_purchase_date()  # Assuming this retrieves the date

               # Append each ticket as a formatted string
               text_widget.insert(
                   "end",
                   f"Ticket(ID: {ticket_id}, Type: {ticket_type}, Price: {price:.2f}, "
                   f"Status: {status}, Date: {purchase_date})\n\n"
               )

           text_widget.config(state="disabled")  # Make the text widget read-only

       # Add a back button to return to the account management screen
       back_button = tk.Button(self.root, text="Back", command=self.manage_account_screen)
       back_button.pack(pady=20)

   def admin_dashboard(self):
       # Display the admin dashboard
       self.clear_window()


       # Add a title for the admin dashboard
       admin_label = tk.Label(self.root, text="Admin Dashboard", font=("Arial", 16, "bold"))
       admin_label.pack(pady=20)


       # Add buttons for admin functionalities
       ticket_sales_button = tk.Button(self.root, text="View Ticket Sales", command=self.view_ticket_sales)
       ticket_sales_button.pack(pady=10)


       modify_discounts_button = tk.Button(self.root, text="Modify Discount Availability",command=self.modify_discounts)
       modify_discounts_button.pack(pady=10)


       update_capacity_button = tk.Button(self.root, text="Update Attraction Capacity", command=self.update_capacity_screen)
       update_capacity_button.pack(pady=10)


       # Add a back button to return to the role selection screen
       back_button = tk.Button(self.root, text="Back", command=self.role_selection_screen)
       back_button.pack(pady=10)


   def update_capacity_screen(self):
       # Display the screen to update attraction capacity
       self.clear_window()


       # Add a label for updating capacity
       update_label = tk.Label(self.root, text="Update Attraction Capacity", font=("Arial", 14))
       update_label.pack(pady=20)


       # Add input fields for attraction ID and new capacity
       attraction_id_label = tk.Label(self.root, text="Attraction ID:")
       attraction_id_label.pack(pady=5)


       self.attraction_id_entry = tk.Entry(self.root)
       self.attraction_id_entry.pack(pady=5)


       capacity_label = tk.Label(self.root, text="New Capacity:")
       capacity_label.pack(pady=5)


       self.new_capacity_entry = tk.Entry(self.root)
       self.new_capacity_entry.pack(pady=5)


       # Add a button to update the capacity
       update_button = tk.Button(self.root, text="Update", command=self.update_capacity)
       update_button.pack(pady=10)


       # Add a back button to return to the admin dashboard
       back_button = tk.Button(self.root, text="Back", command=self.admin_dashboard)
       back_button.pack(pady=10)


   def update_capacity(self):
       # Update the capacity of a specific attraction
       try:
           # Get the input values for attraction ID and new capacity
           attraction_id = int(self.attraction_id_entry.get())
           new_capacity = int(self.new_capacity_entry.get())


           # Update the attraction capacity using business logic
           self.business_logic.update_attraction_capacity(attraction_id, new_capacity)
           messagebox.showinfo("Success", "Attraction capacity updated successfully!")
       except ValueError:
           # Handle invalid input errors
           messagebox.showerror("Error", "Please enter valid numeric values for Attraction ID and Capacity.")
       except Exception as e:
           # Handle other errors
           messagebox.showerror("Error", f"An error occurred: {str(e)}")


   def view_ticket_sales(self):
       # Display the screen to view ticket sales data
       self.clear_window()


       # Add a label for ticket sales
       sales_label = tk.Label(self.root, text="Ticket Sales Data", font=("Arial", 14))
       sales_label.pack(pady=20)


       try:
           # Retrieve all tickets and aggregate sales data by date
           tickets = self.business_logic.get_all_tickets()
           sales_data = {}


           # Collect sales data
           for ticket in tickets:
               # Get the purchase date of the ticket
               ticket_date = ticket.get_purchase_date()  # Access will work as all tickets are now properly initialized
               sales_data[ticket_date] = sales_data.get(ticket_date, 0) + 1  # Increment the count for that date


           # Display the sales data sorted by date
           for date, count in sorted(sales_data.items()):
               ticket_label = tk.Label(self.root, text=f"Date: {date}, Tickets Sold: {count}")
               ticket_label.pack(pady=5)


       except Exception as e:
           # Handle any errors that occur during retrieval or display
           messagebox.showerror("Error", f"An error occurred: {str(e)}")


       # Add a back button to return to the admin dashboard
       back_button = tk.Button(self.root, text="Back", command=self.admin_dashboard)
       back_button.pack(pady=10)




   def modify_discounts(self):
       # Clear the current window to display the discount modification interface
       self.clear_window()


       # Add a label for the discount modification section
       modify_label = tk.Label(self.root, text="Modify Discounts", font=("Arial", 14))
       modify_label.pack(pady=20)


       # Add a label for selecting the ticket type
       ticket_type_label = tk.Label(self.root, text="Select Ticket Type:")
       ticket_type_label.pack(pady=5)


       # Create a dropdown menu for ticket types
       ticket_types = list(self.ticket_type_mapping.keys()) # Get user-friendly ticket type names
       self.discount_ticket_var = tk.StringVar(value=ticket_types[0]) # Default selection
       ticket_menu = tk.OptionMenu(self.root, self.discount_ticket_var, *ticket_types)
       ticket_menu.pack(pady=10)


       # Add a label and entry field for the discount percentage
       discount_label = tk.Label(self.root, text="Enter Discount Percentage:")
       discount_label.pack(pady=5)
       self.discount_entry = tk.Entry(self.root)
       self.discount_entry.pack(pady=5)


       # Add a button to apply the discount
       apply_button = tk.Button(self.root, text="Apply Discount", command=self.apply_discount)
       apply_button.pack(pady=10)


       # Add a back button to return to the admin dashboard
       back_button = tk.Button(self.root, text="Back", command=self.admin_dashboard)
       back_button.pack(pady=10)


   def apply_discount(self):
       # Get the selected ticket type and entered discount value
       ticket_type = self.discount_ticket_var.get()
       discount = self.discount_entry.get()


       try:
           discount = int(discount)  # Convert the discount value to an integer
           if not (0 <= discount <= 100):  # Validate the discount range
               raise ValueError("Discount must be between 0 and 100.")


           # Map the user-friendly ticket type to the backend TicketType enum
           backend_ticket_type = self.ticket_type_mapping.get(ticket_type)
           if not backend_ticket_type:  # Validate the mapping
               raise ValueError("Invalid ticket type selected.")


           # Convert to TicketType enum and apply the discount using business logic
           ticket_type_enum = TicketType[backend_ticket_type]
           self.business_logic.modify_ticket_discount(ticket_type_enum, discount)


           # Show success message and return to the admin dashboard
           messagebox.showinfo("Success", f"Discount of {discount}% applied to {ticket_type}.")
           self.admin_dashboard()
       except ValueError as ve:
           # Show an error message for invalid inputs
           messagebox.showerror("Error", str(ve))
       except Exception as e:
           # Show an error message for any other exceptions
           messagebox.showerror("Error", f"An error occurred: {str(e)}")


   def ticket_purchasing_screen(self):
       # Clear the current window to display the ticket purchasing interface
       self.clear_window()


       # Add a label for ticket selection
       ticket_label = tk.Label(self.root, text="Select a Ticket Type", font=("Arial", 14))
       ticket_label.pack(pady=20)


       # Create a dropdown menu for ticket types
       ticket_options = list(self.ticket_type_mapping.keys())  # Get user-friendly ticket type names
       self.ticket_var = tk.StringVar(value=ticket_options[0])  # Default selection
       ticket_menu = tk.OptionMenu(self.root, self.ticket_var, *ticket_options)
       ticket_menu.pack(pady=10)


       # Add an entry field for the number of tickets
       ticket_quantity_label = tk.Label(self.root, text="Enter Number of Tickets:")
       ticket_quantity_label.pack(pady=5)
       self.ticket_quantity_entry = tk.Entry(self.root)
       self.ticket_quantity_entry.pack(pady=5)


       # Add an entry field for child age (specific to Child Ticket)
       child_label = tk.Label(self.root, text="Enter Child Age (3-12 for discounts):")
       child_label.pack(pady=5)
       self.child_age_entry = tk.Entry(self.root)
       self.child_age_entry.pack(pady=5)


       # Add an entry field for group size (specific to Group Ticket)
       group_size_label = tk.Label(self.root, text="Enter Group Size (For Group Tickets):")
       group_size_label.pack(pady=5)
       self.group_size_entry = tk.Entry(self.root)
       self.group_size_entry.pack(pady=5)


       # Add a date picker for ticket selection
       date_label = tk.Label(self.root, text="Select Date (YYYY-MM-DD):")
       date_label.pack(pady=5)
       self.date_entry = tk.Entry(self.root)
       self.date_entry.insert(0, "YYYY-MM-DD")  # Placeholder for the date
       self.date_entry.pack(pady=5)


       # Add a button to calculate the ticket price
       calculate_button = tk.Button(self.root, text="Calculate Price", command=self.calculate_price)
       calculate_button.pack(pady=10)


       # Add a back button to return to the main menu
       back_button = tk.Button(self.root, text="Back", command=self.main_menu)
       back_button.pack(pady=10)


   def calculate_price(self):
       # Get the selected ticket type, quantity, and date from the user input
       ticket_type = self.ticket_var.get()  # Get user-friendly ticket type from dropdown
       selected_date = self.date_entry.get()  # Get the selected date
       quantity = self.ticket_quantity_entry.get()  # Get the ticket quantity


       try:
           # Validate ticket quantity input
           quantity = int(quantity)  # Convert quantity to integer
           if quantity <= 0:
               raise ValueError("The number of tickets must be greater than zero.")


           # Validate date input
           if not selected_date or selected_date == "YYYY-MM-DD":
               raise ValueError("Please select a valid date for your ticket.")


           # Map user-friendly ticket type to backend TicketType Enum
           backend_ticket_type = self.ticket_type_mapping.get(ticket_type)
           if not backend_ticket_type:  # Validate the mapping
               raise ValueError("Invalid ticket type selected.")


           # Convert to TicketType Enum
           ticket_type_enum = TicketType[backend_ticket_type]


           # Fetch ticket details like price and discount
           ticket_details = Ticket.TICKET_DETAILS.get(ticket_type_enum)
           if not ticket_details:  # Validate ticket details existence
               raise ValueError(f"No details found for ticket type: {ticket_type}")


           price = ticket_details["price"]  # Base price of the ticket
           discount = ticket_details["discount"]  # Default or admin-modified discount


           # Apply predefined discount rules for specific tickets
           if ticket_type == "Two-Day Pass":
               discount = max(discount, 10)  # Ensure at least a 10% discount for Two-Day Pass
           elif ticket_type == "Annual Membership":
               discount = max(discount, 15)  # Ensure at least a 15% discount for renewal
           elif ticket_type == "Group Ticket":
               group_size = int(self.group_size_entry.get())
               if group_size >= 20:  # Only apply discount for groups of 20+
                   discount = max(discount, 20)
               else:
                   discount = 0  # No discount for smaller groups
           elif ticket_type == "Child Ticket":
               age = int(self.child_age_entry.get())
               if not (3 <= age <= 12):
                   messagebox.showerror("Error", "Child ticket is valid for ages 3-12 only.")
                   return


           # Calculate final price after applying discount and multiply by quantity
           final_price = price * (1 - discount / 100) * quantity


           # Proceed to payment screen
           self.payment_screen(ticket_type, price, discount, final_price, selected_date, quantity)


       except ValueError as ve:
           # Show an error message for invalid inputs
           messagebox.showerror("Error", f"Invalid input: {str(ve)}")
       except Exception as e:
           # Show an error message for any unexpected errors
           messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


   def payment_screen(self, ticket_type, price, discount, final_price, selected_date, quantity):
       # Clear the current window to display the payment screen
       self.clear_window()


       # Create a summary of the ticket details and payment information
       summary = (
           f"Ticket Type: {ticket_type}\n"  # Display the type of ticket
           f"Quantity: {quantity}\n"  # Display the number of tickets
           f"Selected Date: {selected_date}\n"  # Display the selected date for the ticket
           f"Original Price (per ticket): {price} DHS\n"  # Display the original ticket price
           f"Discount Applied: {discount}%\n"  # Display the discount applied
           f"Final Price (Total): {final_price:.2f} DHS"  # Display the final price after applying the discount
       )
       # Display the summary in a label
       summary_label = tk.Label(self.root, text=summary, font=("Arial", 14))
       summary_label.pack(pady=20)


       # Add a label for payment method selection
       payment_method_label = tk.Label(self.root, text="Select Payment Method:")
       payment_method_label.pack(pady=5)


       # Create a dropdown menu for selecting the payment method
       self.payment_method_var = tk.StringVar(value="Credit Card")
       payment_method_menu = tk.OptionMenu(self.root, self.payment_method_var, "Credit Card", "Debit Card", "Digital Wallet")
       payment_method_menu.pack(pady=10)


       # Add a label and entry field for card number
       card_number_label = tk.Label(self.root, text="Card Number:")
       card_number_label.pack(pady=5)
       self.card_number_entry = tk.Entry(self.root)
       self.card_number_entry.pack(pady=5)


       # Add a label and entry field for card expiry date
       expiry_label = tk.Label(self.root, text="Expiry Date (MM/YY):")
       expiry_label.pack(pady=5)
       self.expiry_entry = tk.Entry(self.root)
       self.expiry_entry.pack(pady=5)


       # Add a label and entry field for the CVV
       cvv_label = tk.Label(self.root, text="CVV:")
       cvv_label.pack(pady=5)
       self.cvv_entry = tk.Entry(self.root)
       self.cvv_entry.pack(pady=5)


       # Add a button to proceed with the payment
       pay_button = tk.Button(self.root, text="Pay",command=lambda: self.process_payment(ticket_type, final_price, selected_date, quantity))
       pay_button.pack(pady=10)


       # Add a back button to return to the ticket purchasing screen
       back_button = tk.Button(self.root, text="Back", command=self.ticket_purchasing_screen)
       back_button.pack(pady=10)


   def process_payment(self, ticket_type, final_price, selected_date, quantity):
       # Add the quantity parameter to the ticket creation logic
       try:
           # Retrieve payment details from user input
           card_number = self.card_number_entry.get()  # Card number entered by the user
           expiry = self.expiry_entry.get()  # Expiry date entered by the user
           cvv = self.cvv_entry.get()  # CVV entered by the user
           payment_method = self.payment_method_var.get()  # Payment method selected by the user


           # Validate that all payment details are provided
           if not (card_number and expiry and cvv):
               messagebox.showerror("Error", "All payment details are required.")
               return


           # Validate the payment amount
           if final_price <= 0:
               raise ValueError("The payment amount must be greater than zero.")


           # Map the user-friendly ticket type to the backend TicketType Enum
           backend_ticket_type = self.ticket_type_mapping.get(ticket_type)
           if not backend_ticket_type:
               raise ValueError("Invalid ticket type selected.")


           # Get the corresponding TicketType Enum value
           ticket_type_enum = TicketType[backend_ticket_type]


           # Create multiple tickets for the specified quantity
           for _ in range(quantity):
               self.business_logic.add_ticket_to_guest(
                   self.guest.get_guest_id(),  # Guest ID of the currently logged-in guest
                   ticket_type_enum,  # Backend enum for ticket type
                   final_price / quantity,  # Price per ticket
                   selected_date  # Selected date for the ticket
               )


           # Display a success message for the payment
           messagebox.showinfo(
               "Success",
               f"Payment Successful!\nDate: {selected_date}\nTotal Amount Paid: {final_price:.2f} DHS\nMethod: {payment_method}",
           )
           # Redirect to the purchase orders screen
           self.view_purchase_orders()


       except ValueError as ve:
           # Show an error message for invalid inputs
           messagebox.showerror("Payment Error", f"Error: {str(ve)}")
       except Exception as e:
           # Show an error message for unexpected errors
           messagebox.showerror("Payment Error", f"An error occurred: {str(e)}")


   def clear_window(self):
       # Clear all widgets from the current window
       for widget in self.root.winfo_children():
           widget.destroy()


# Entry point of the application
if __name__ == "__main__":
   root = tk.Tk()  # Create the main Tkinter window
   app = App(root)  # Initialize the application
   root.mainloop()  # Start the Tkinter main event loop