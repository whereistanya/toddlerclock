#!/usr/bin/python3
"""A clock to tell your toddler whether they can wake you."""

import logging
import time

MINUTES_IN_DAY = 1440

class Event(object):
  """A single event on a clock, with a start and stop time."""
  def __init__(self, start_time, stop_time, description):
    """Create an event. Can't cross midnight boundaries. Make two events.

    Midnight is minute 0. 1am is minute 60. 11:55pm is minute 1435.

    Args:
        start_time, stop_time: ((int, int)): tuple of hours and minutes.
                               All times are 24h. Events stop at the beginning
                               of the stop time, i.e., an event from 10am to
        description: (str) Text to display for this event.
    """
    logging.info("Adding %s from %s to %s", description, start_time, stop_time)
    if len(start_time) != 2 or len(stop_time) != 2:
      logging.warning(
          "Time looks screwy: start (%s), stop (%s)", start_time, stop_time)
      return
    self.start_minute = start_time[0] * 60 + start_time[1]
    self.stop_minute = stop_time[0] * 60 + stop_time[1]
    if self.start_minute > self.stop_minute:
      logging.warning(
          "Start is after stop: %s vs %s", self.start_minute, self.stop_minute)
      return
    self.description = description

class EventList(object):
  """Time-bounded daily events."""
  def __init__(self):
    self.minutes = []
    for _ in range(0, MINUTES_IN_DAY):
      self.minutes.append("")  # initialise every minute with no event.

  def add(self, event, overwrite=False):
    """Add an event to the day, optionally overwriting existing ones.

    One event at a time. Later maybe I'll come back and make this display
    multiple things at a time. One's good for now.
    Args:
      event: (Event): an event to add
    """
    for i in range(event.start_minute, event.stop_minute):
      if self.minutes[i] == "" or overwrite == True:
        self.minutes[i] = event.description

  def current(self):
    """Return the current event description.

    Returns:
      (str): Whatever should be happening right now or empty string.
    """
    now = time.localtime()
    return self.event_at_minute(now.tm_hour * 60 + now.tm_min)

  def event_at_minute(self, minute):
    """Return the event for any given minute.

    Returns:
      (str): Whatever should be happening at that minute or empty string.
    """
    if minute < 0:
      logging.warning("Minute less than zero: %s", minute)
      return ""

    return self.minutes[minute]
