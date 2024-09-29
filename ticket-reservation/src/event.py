class Event:
    def __init__(self, event_name=None, reserved_seats=None, event_cost=None):
        self.event_name = event_name
        self.reserved_seats = reserved_seats if reserved_seats else []
        self.event_cost = event_cost

    def __repr__(self):
        return f"{self.event_name}"

    def add_reserved_seat(self, seat):
        self.reserved_seats.append(seat)
        print(f"Seat {seat} reserved for {self.event_name}")

def read_event_info_from_file(file_path):
    events = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split(', ')
                event_name = data[0]
                reserved_seats = [seat.strip('[]') for seat in data[1].split()]
                event_costs = [float(cost.strip('[]')) for cost in data[2].split()]

                # Create Event object
                event = Event(event_name, reserved_seats, event_costs)
                events.append(event)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return events


def update_event_reserved_seats_by_name(file_path, event_name, new_reserved_seat):
    events = read_event_info_from_file(file_path)
    print(events)
    event = None  # Initialize event to None

    # Find the event by name
    for e in events:
        if e.event_name == event_name:
            # Remove the old event line
            events.remove(e)
            event = e  # Assign the found event to the 'event' variable
            break

    # Update the event with the new reserved seat
    if event:
        event.add_reserved_seat(new_reserved_seat)
        events.append(event)

        # Rewrite the entire file with the updated events
        with open(file_path, 'w') as file:
            for e in events:
                file.write(f"{e.event_name}, [{' '.join(e.reserved_seats)}], [{' '.join(map(str, e.event_cost))}]\n")