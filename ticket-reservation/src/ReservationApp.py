import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from event import read_event_info_from_file, update_event_reserved_seats_by_name, Event
from reservation import Reservation

class TicketReservationApp:
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    FONT_LARGE = ("consolas", 16)
    FONT_MEDIUM = ("consolas", 14)
    FONT_SMALL = ("consolas", 12)
    EVENTS_DB_PATH = "./data/events_data.txt"

    def __init__(self, master):
        # Initialize the TicketReservationApp
        self.master = master
        self.configure_window()
        self.configure_styles()
        self.initialize_data()
        self.display_home_scene()
    
    def configure_window(self):
        # Configure window dimensions
        self.master.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
    
    def configure_styles(self):
        # Configure styles for reserved and available seats
        style = ttk.Style()
        style.configure('Reserved.TButton', background='red', font=('Helvetica', 10))
        style.configure('Available.TButton', background='green', font=('Helvetica', 10))
    
    def initialize_data(self):
        # Initialize data including events, selected event, reservation, and seating map
        self.events = read_event_info_from_file(self.EVENTS_DB_PATH)
        self.selected_event = Event()
        self.reservation = Reservation()
        self.seating_map = [
                ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
                ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'],
                ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
                ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
                ['VIP1', 'VIP2', 'VIP3', 'VIP4', 'VIP5', 'VIP6', 'VIP7', 'VIP8'],
                ['VIP9', 'VIP10', 'VIP11', 'VIP12', 'VIP13', 'VIP14', 'VIP15', 'VIP16']
            ]
    
    def clear_widgets(self):
        # Clear all widgets from the master window
        for widget in self.master.winfo_children():
            widget.destroy()
    
    # *Home Scene*
    def display_home_scene(self):
        # Display the home scene with welcome message, event listbox, and select event button
        self.clear_widgets()
        self.refresh_events()
        self.create_frame()
        self.add_label('Welcome to Ticket Reservation System', self.FONT_LARGE)
        self.populate_event_listbox()
        self.add_button("Select Event", self.handle_event_selection)
    
    def refresh_events(self):
        # Refresh events data
        self.events = read_event_info_from_file(self.EVENTS_DB_PATH)
        self.selected_event = Event()
        self.reservation = Reservation()
    
    def create_frame(self):
        # Create a new frame for the current scene
        self.current_frame = ttk.Frame(self.master)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
    
    def add_label(self, text, font, padding_y=10):
        # Add a label with specified text, font, and padding
        label = ttk.Label(self.current_frame, text=text, font=font)
        label.pack(pady=padding_y)
    
    def populate_event_listbox(self):
        # Populate the event listbox with events from the database
        self.event_listbox = tk.Listbox(self.current_frame, selectmode=tk.SINGLE, font=self.FONT_SMALL)
        for event in self.events:
            self.event_listbox.insert(tk.END, event.event_name)
        self.event_listbox.pack(pady=10)
    
    def add_button(self, text, command, padding_y=10, padding_x=5):
        # Add a button with specified text, command, and padding
        button = ttk.Button(self.current_frame, text=text, command=command)
        button.pack(pady=padding_y, ipadx=padding_x, ipady=3)
    
    def handle_event_selection(self):
        # Handle the selection of an event and transition to the booking scene
        selected_index = self.get_selected_event_index()
        if selected_index is None:
            # Show an error message if no event is selected
            messagebox.showerror("Event Selection Error", "Please select an event to continue!")
            return
        self.update_selected_event(selected_index)
        self.display_booking_scene()
    
    def get_selected_event_index(self):
        # Get the index of the selected event in the listbox
        selection = self.event_listbox.curselection()
        return selection[0] if selection else None
    
    def update_selected_event(self, index):
        # Update the selected event and reservation based on the index
        self.selected_event = self.events[index]
        self.reservation.event_name = self.selected_event.event_name
        print(f"Selected Event: {self.reservation.event_name}")
        
    # *Booking Scene*
    def display_booking_scene(self):
        # Display the booking scene with reserved seats and seating map
        self.clear_widgets()
        self.create_frame()
        self.add_label('Select Seats and Confirm Booking', self.FONT_LARGE)
        self.display_reserved_seats()
        self.display_seating_map()
    
    def display_reserved_seats(self):
        # Display reserved seats for the selected event
        reserved_seats_text = "Reserved seats: " + ', '.join(self.selected_event.reserved_seats)
        self.add_label(reserved_seats_text, self.FONT_MEDIUM)
    
    def display_seating_map(self):
        # Display the seating map with buttons for each seat
        seating_map_frame = ttk.Frame(self.current_frame)
        seating_map_frame.pack(pady=10)
        self.create_seating_buttons(seating_map_frame)
    
    def create_seating_buttons(self, frame):
        # Create buttons for each seat in the seating map
        for row_index, row in enumerate(self.seating_map):
            for col_index, seat in enumerate(row):
                if seat in self.selected_event.reserved_seats:
                    seat_button = ttk.Button(frame, text=seat, command=lambda s=seat: self.select_seat(s), style='Reserved.TButton')
                else:
                    seat_button = ttk.Button(frame, text=seat, command=lambda s=seat: self.select_seat(s), style='Available.TButton')

                seat_button.grid(row=row_index, column=col_index, padx=5, pady=5)
    
    def select_seat(self, seat):
        # Handle seat selection, check availability, and transition to confirmation scene
        if seat in self.selected_event.reserved_seats:
            # Show an error message if the seat is already reserved
            messagebox.showerror("Seat Reserved", f"Seat {seat} is already reserved for {self.selected_event.event_name}")
            return
          
        self.reservation.selected_seat = seat
        
        if self.reservation.selected_seat.startswith("VIP"):
            self.reservation.total_cost = self.selected_event.event_cost[1]
            self.reservation.ticket_type = "VIP"
        else:
            self.reservation.total_cost = self.selected_event.event_cost[0]
            self.reservation.ticket_type = "standard " + self.reservation.selected_seat[0]
            
        self.display_confirmation_scene()    
    
    # *Confirmation Scene*
    def display_confirmation_scene(self):
        # Display the confirmation scene with customer name entry, reservation details, and finish buttons
        self.clear_widgets()
        self.create_frame()
        self.add_label("Reservation Details", self.FONT_LARGE)
        self.add_customer_name_entry()
        self.display_reservation_details()
        self.add_finish_buttons()
    
    def add_customer_name_entry(self):
        # Add an entry for customer name input
        ttk.Label(self.current_frame, text="Name:", font=self.FONT_MEDIUM).pack(pady=10, anchor='w')
        self.customer_name_entry = ttk.Entry(self.current_frame, font=self.FONT_MEDIUM)
        self.customer_name_entry.pack(pady=10)
    
    def display_reservation_details(self):
        # Display reservation details including customer name, event name, selected seat, and total cost
        details = self.reservation.get_details()
        for detail in details:
            ttk.Label(self.current_frame, text=detail[0], font=self.FONT_MEDIUM).pack(anchor='w')
            ttk.Label(self.current_frame, text=detail[1], font=self.FONT_MEDIUM, foreground="green").pack(anchor='w')
    
    def add_finish_buttons(self):
        # Add buttons for finishing the booking or canceling
        self.add_button("Finish", self.confirm_booking, padding_y=20)
        self.add_button("Cancel", self.display_home_scene)
    
    def confirm_booking(self):
        # Confirm the booking, validate customer name, save reservation, and return to the home scene
        customer_name = self.customer_name_entry.get().strip()
        if not customer_name:
            # Show an error message if customer name is not entered
            messagebox.showerror("Confirmation Error!", "Please enter your name to confirm the ticket reservation!")
            return
        self.reservation.customer_name = customer_name
        self.finalize_booking()
    
    def finalize_booking(self):
        # Finalize the booking by updating reserved seats, saving reservation, and displaying details
        update_event_reserved_seats_by_name(self.EVENTS_DB_PATH, self.reservation.event_name, self.reservation.selected_seat)
        self.reservation.save()
        print(self.reservation.to_string())
        self.display_home_scene()

if __name__ == "__main__":
    # Run the TicketReservationApp
    root = tk.Tk()
    app = TicketReservationApp(root)
    root.mainloop()
