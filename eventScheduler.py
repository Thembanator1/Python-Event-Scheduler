from datetime import datetime
import math

class Format:
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED ='\033[31m'


# Data storage
events = []

def binary_search(events, target_title):
    start = 0
    end = len(events) - 1

    while start <= end:
        mid = start + (end - start) // 2

        # Check if the target title is equal to the middle event's title
        if events[mid]['title'] == target_title:
            return mid

        # If the target title is greater, search in the right half
        elif events[mid]['title'] < target_title:
            start = mid + 1
        # If the target title is smaller, search in the left half
        else:
            end = mid - 1

    return None

def binary_search_insert(arr, new_event_title):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid]['title'] == new_event_title:
            return mid  # Element already exists at this position
        elif arr[mid]['title'] < new_event_title:
            left = mid + 1
        else:
            right = mid - 1

    return left  # Return the position where the element should be inserted

# add a new event
def add_event(title, description, date, time):
    # Check if the title already exists
    is_Duplicate = binary_search(events, title)
    if is_Duplicate != None:
        print(f"Cannot Create Event, title '{title}' already exists.")
        return

    new_event = {
        'title': title,
        'description': description,
        'date': date,
        'time': time
    }
    new_event_title = new_event['title']

    insert_position = binary_search_insert(events, new_event_title)
    events.insert(insert_position, new_event)
    print("Event added successfully!")
    #maintaining a sorted-insertion makes Deleting Events by title easier

def display_events(events, searching=False):
    if not events and  not searching:
        print("No events scheduled.")
        return
    if not events and searching:
        print(" No events with Keyword Found...")
        return

    # Calculate maximum description length for formatting
    max_description_length = 50  # Adjust as needed

    eventCounter=0
    for event in events:
        eventCounter+=1
        # Generate formatted output for each event
        formatted_output = []
        
        title_line = f"Title: {event['title']}"
        # Split the description into multiple lines

            # Initialize an empty list to store description lines
        description_lines = []

        # Loop through the event description in chunks of max_description_length characters
        for i in range(0, len(event['description']), max_description_length):
            # Extract a substring of max_description_length characters
            description_chunk = event['description'][i:i + max_description_length]

            # Create a formatted description line with the chunk and prepend "Description: "
            if i == 0:
                description_line = f"Description: {description_chunk}"
            else:
                description_line = description_chunk

            # Append the formatted description line to the list of description lines
            description_lines.append(description_line)

        date_line = f"Date: {event['date']}"
        time_line = f"Time: {event['time']}"

        # Add event details to the formatted output
        formatted_output.extend([title_line] + description_lines + [date_line, time_line, ""])

        # Format the output
        max_width = max(len(line) for line in formatted_output)
        top_line = "+" + "-" * math.floor(max_width / 2) +f"{eventCounter}"+ "-" * math.ceil(max_width / 2) + "+"
        bottom_line = "+" + "_" * (max_width + 2) + "+"
        formatted_output = [top_line] + ["| " + line.ljust(max_width) + " |" for line in formatted_output] + [bottom_line]

        # Print the formatted output
        print("\n".join(formatted_output))


def edit_event(title):
    for event in events:
        if event['title'] == title:
            print("Editing event:", title)
            description = input("Enter new description (press enter to keep existing): ")
            date = input("Enter new date (YYYY-MM-DD) (press enter to keep existing): ")
            time = input("Enter new time (HH:MM) (press enter to keep existing): ")

            if description:
                event['description'] = description
            if date:
                try:
                    datetime.strptime(date, '%Y-%m-%d')
                    event['date'] = date
                except ValueError:
                    print("Invalid date format. Date not updated.")

            if time:
                try:
                    datetime.strptime(time, '%H:%M')
                    event['time'] = time
                except ValueError:
                    print("Invalid time format. Time not updated.")

            print("Event updated successfully!")
            return
    print(f"Event with title '{title}' not found.")


# Fdelete an event by title
def delete_eventt(title):
    indx = binary_search(events, title)
    if indx != None:
        events.pop(indx)
        print(f"Event '{title}' deleted successfully!")
        return
    print(f"Event with title '{title}' not found.")


def search_events(events, query):
    found_events = []

    # Search by date
    for event in events:
        if query in event['date']:
            found_events.append(event)

    # Search by keyword in title/description
    for event in events:
        if query in event['title'] or query in event['description'] and event not in found_events:
                found_events.append(event)

    return found_events

def get_valid_input(prompt, format_str, error_message): #looping till user enters correct Date/Time
        while True:
            user_input = input(prompt)
            try:
                value = datetime.strptime(user_input, format_str)
                formatted_value = value.strftime("%B %d, %Y" if format_str == "%Y-%m-%d" else "%I:%M %p")
                print("Formatted Value:", formatted_value)
                return user_input
            except ValueError:
                print(error_message)


# Main function
def main():
    menu = """
    Event Scheduler Main Menu:
        1. Add Event
        2. Display Events
        3. Edit Event
        4. Delete Event
        5. Search For Event
        6. Exit
    """

    while True:
        print(Format.BOLD +  menu + Format.END)
    
        choice = input(f"{Format.RED}\tEnter your choice:{Format.END} ")
        print()


        if choice == '1':
            while True: #Till user enters unique title
                title = input("Enter event title: ")
                is_Duplicate = binary_search(events, title)
                if is_Duplicate == None:
                    break
                else:
                    print(f"Cannot Create Event, title '{title}' already exists.")
            
            description = input("Enter event description: ")

            date_input = get_valid_input("Enter a date (YYYY-MM-DD): ", "%Y-%m-%d", "Invalid date format. Please enter date in YYYY-MM-DD format.")
            time_input = get_valid_input("Enter a time (HH:MM): ", "%H:%M", "Invalid time format. Please enter time in HH:MM format.")

            add_event(title, description, date_input, time_input)

        elif choice == '2':
            sorted_events = sorted(events, key=lambda x: (x['date'], x['time']))
            print("MY Schedule: ")
            display_events(sorted_events)
        elif choice == '3':
            title = input("Enter title of event to edit: ")
            edit_event(title)
        elif choice == '4':
            title = input("Enter title of event to delete: ")
            delete_eventt(title)
        elif choice == '5':
            query = input("Enter search query (date or keyword in title/description): ")
            found_events = search_events(events, query)

            # if not found_events:
            #     print("No matching events found.")
            #     break

            print(f"Matching events found ({len(found_events)} results):")
            display_events(found_events, True)

        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")




if __name__ == "__main__":
    main()
