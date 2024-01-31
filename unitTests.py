import unittest
from unittest.mock import patch
from eventScheduler import (
    add_event,
    delete_eventt,
    search_events,
    edit_event,
    events  
)


class TestEventFunctions(unittest.TestCase):

    def setUp(self):
        # Ensure that the events list is empty before each test
        events.clear()

    def test_add_event(self):
        add_event("Event 1", "Description 1", "2024-01-31", "12:00")
        self.assertEqual(len(events), 1)
        # Add more assertions as needed

    def test_delete_event(self):
        events.append({'title': 'Event 1', 'description': '1st event', 'date': '2023-12-31', 'time': '08:00'})
        events.append({'title': 'Existing Title', 'description': 'Some Description', 'date': '2023-12-31', 'time': '08:00'})
        delete_eventt("Event 1")
        self.assertEqual(len(events), 1)
        # Add more assertions as needed

    @patch('builtins.input', side_effect=['New description', '2024-01-31', '12:00'])
    def test_edit_event_existing_title(self, mock_input):
        # Add an event to edit
        events.append({'title': 'Existing Title', 'description': 'Old Description', 'date': '2023-12-31', 'time': '08:00'})
        
        # Call edit_event with existing title
        edit_event('Existing Title')
        
        # Assert that the event has been updated
        self.assertEqual(events[0]['description'], 'New description')
        self.assertEqual(events[0]['date'], '2024-01-31')
        self.assertEqual(events[0]['time'], '12:00')

    @patch('builtins.input', side_effect=['New description', '2024-01-31', '12:00'])
    def test_edit_event_non_existing_title(self, mock_input):
        # Call edit_event with a non-existing title
        edit_event('A Title we dont have')
        
        # Assert that no changes were made to the events list
        self.assertEqual(len(events), 0)  # No events should be added


    def test_search_events(self):
        events.append({'title': 'Event 1', 'description': '1st event', 'date': '2023-11-31', 'time': '08:00'})
        events.append({'title': 'Event 2', 'description': '2nd Event', 'date': '2023-12-31', 'time': '08:00'})
        events.append({'title': 'Unique Title', 'description': 'Different naming', 'date': '2023-12-31', 'time': '01:30'})
        found_events = search_events(events, "Event")
        self.assertEqual(len(found_events), 2)
        # Add more assertions as needed

    # Add more test cases for other functions


if __name__ == '__main__':
    unittest.main()
