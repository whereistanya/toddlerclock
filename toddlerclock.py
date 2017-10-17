#!/usr/bin/python3
"""A clock to tell your toddler whether they can wake you."""

import os
import time
import pygame

from signal import alarm, signal, SIGALRM


WHITE = ((255, 255, 255))
BLACK = ((0, 0, 0))
RED = ((255, 0, 0))
BLUE = ((5, 20, 114))
GREEN = ((52, 114, 5))
ORANGE = ((239, 103, 19))
PINK = ((178, 53, 161))
INDIGO = ((59, 33, 135))

MINUTES_IN_DAY = 1440

class Alarm(Exception):
  """A deadline for things that get wedged."""
  pass

def alarm_handler(signum, frame):
  raise Alarm

class Event(object):
  def __init__(self, start_time, stop_time, description):
    """Create an event. Can't cross midnight boundaries. Make two events. 

    Midnight is minute 0. 1am is minute 60. 11:55pm is minute 1435.

    Args:
        start_time, stop_time: ((int, int)): tuple of hours and minutes.
                               All times are 24h. Events stop at the beginning
                               of the stop time, i.e., an event from 10am to
        description: (str) Text to display for this event.
    """
    print ("Adding %s from %s to %s" % (description, start_time, stop_time))
    if len(start_time) != 2 or len(stop_time) != 2:
      print("Time looks screwy: start (%s), stop (%s)" % (start_time, stop_time))
      # TODO(tanya): log a warning instead.
      return
    self.start_minute = start_time[0] * 60 + start_time[1]
    self.stop_minute = stop_time[0] * 60 + stop_time[1]
    if self.start_minute > self.stop_minute:
      # TODO(tanya): log a warning here too!
      print("Start minute > stop minute: %s vs %s" % (
          self.start_minute, self.stop_minute))
      return
    self.desc = description

  def start_minute(self):
    """Return an integer for the minute of the day when this event starts. """
    return self.start_minute

  def stop_minute(self):
    """Return an integer for the minute of the day when this event stops."""
    return self.stop_minute

  def description(self):
    """Return the description string."""
    return self.desc


class EventList(object):
  def __init__(self):
    self.minutes = []
    for i in range(0, MINUTES_IN_DAY):
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
        self.minutes[i] = event.description()

  def current(self):
    """Return the current event description.

    Returns:
      (str): Whatever should be happening right now or empty string.
    """
    now = time.localtime()
    e = self.event_at_minute(now.tm_hour * 60 + now.tm_min)
    return e

  def event_at_minute(self, minute):
    """Return the event for any given minute.

    Returns:
      (str): Whatever should be happening at that minute or empty string.
    """
    if minute < 0:
      # TODO(tanya): Log a warning.
      return ""

    return self.minutes[minute]


class ToddlerClock(object):
  """Display the time with a message."""

  def __init__(self):
    """Make a ToddlerClock with graphics and events."""
    self.events = EventList()
    self.add_events()
    # Needed to talk to the raspberry pi's PiTFT display. For the 7" display
    # attached to the DSI port, comment these out.
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

    # For 7" display, change to 800 and 600
    self.x = 320
    self.y = 240
    self.bottom = 200
    pygame.init()
    pygame.mouse.set_visible(False)
    #  If this hangs, it's because something else is using the screen. Ctrl-C
    #  here will bypass that.
    signal(SIGALRM, alarm_handler)
    alarm(2)
    try:
      print("Attempting to initialise the display. Waiting up to two seconds.")
      self.screen = pygame.display.set_mode((self.x, self.y))
      alarm(0)
    except Alarm:
      raise KeyboardInterrupt
    self.clocksurface = pygame.Surface((self.x, self.bottom)).convert()
    self.messagesurface = pygame.Surface((self.x, self.y - self.bottom)).convert()

    self.bigfont = pygame.font.SysFont("verdana", 90)
    self.smallfont = pygame.font.SysFont("verdana", 18)
    self.clock = pygame.time.Clock()


  def add_events(self):
    # Starting at kid bedtime...
    self.events.add(Event((19,0), (20,00), "Bedtime. Goodnight, Biz! Sleep well!"))
    self.events.add(Event((20,0), (23,59), "Too early. Go back to sleep, Biz"))
    self.events.add(Event((0,0), (6,0), "Too early. Go back to sleep, Biz"))
    self.events.add(Event((6,0), (7,0), "Time to read, Biz"))
    self.events.add(Event((7,0), (7,15), "It's morning! Wake up, parents!"))
    self.events.add(Event((7,15), (7,30), "Get dressed and go downstairs, Biz!"))
    self.events.add(Event((7,30), (8,0), "Breakfast and get ready for school, Biz!"))
    self.events.add(Event((15,45), (15,48), "Stop asking questions, Biz!"))


  def run(self):
    """The main loop."""
    while True:
      self.screen.blit(self.clocksurface, ((0, 0)))
      self.screen.blit(self.messagesurface, ((0, self.bottom)))

      now = time.localtime()
      nowstr = self.bigfont.render("%.2d:%.2d" % (now.tm_hour, now.tm_min),
                                   True, WHITE)
      color = BLUE
      # Might render an empty string, i.e., nothing, which is fine.
      event = self.smallfont.render(
          self.events.current(), True, WHITE)

      self.draw(color, nowstr, event)
      self.clock.tick(1) # every 1s

  def draw(self, color, nowstr, message):
    """Draw the clock with an optional message!"""
    self.clocksurface.fill(color)
    self.messagesurface.fill(color)

    self.clocksurface.blit(nowstr,
                           ((self.x - nowstr.get_width()) / 2,
                            (self.bottom - nowstr.get_height()) / 2))
    self.messagesurface.blit(message,
                             ((self.x - message.get_width()) / 2,
                              (self.y - self.bottom - message.get_height()) / 2))
    pygame.display.flip()


# Main.
toddlerclock = ToddlerClock()
toddlerclock.run()
