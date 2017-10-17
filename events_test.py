#!/usr/bin/python3
"""Tests for events.py. Run them with py.test."""

import unittest
import events

class TestEventList(unittest.TestCase):
  """Tests for events.py."""

  def test_add_event(self):
    """Add a bunch of events and check they're recorded in the eventlist."""
    eventlist = events.EventList()
    eventlist.add(events.Event((10, 0), (11, 0), "Event 1"))
    eventlist.add(events.Event((12, 30), (13, 40), "Event 2"))
    self.assertEqual(eventlist.event_at_minute(10 * 60), "Event 1")
    self.assertEqual(eventlist.event_at_minute(10 * 60 + 59), "Event 1")
    self.assertEqual(eventlist.event_at_minute(11 * 60), "")
    self.assertEqual(eventlist.event_at_minute(9 * 60), "")
