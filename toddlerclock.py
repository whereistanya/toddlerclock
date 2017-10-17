#!/usr/bin/python3
"""A clock to tell your toddler whether they can wake you."""

import logging
import os
import time
import pygame

import events

from signal import alarm, signal, SIGALRM


WHITE = ((255, 255, 255))
BLACK = ((0, 0, 0))
RED = ((255, 0, 0))
BLUE = ((5, 20, 114))
GREEN = ((52, 114, 5))
ORANGE = ((239, 103, 19))
PINK = ((178, 53, 161))
INDIGO = ((59, 33, 135))

class Alarm(Exception):
  """A deadline for things that get wedged."""
  pass

def alarm_handler(unused_signum, frame):
  """Alarm when pygame gets wedged."""
  raise Alarm

class ToddlerClock(object):
  """Display the time with a message."""

  def __init__(self):
    """Make a ToddlerClock with graphics and events."""
    self.eventlist = events.EventList()
    self.add_events()
    # Needed to talk to the raspberry pi's PiTFT display. For the 7" display
    # attached to the DSI port, comment these out.
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

    # For 7" display, change to 800 and 600
    self.width = 320
    self.height = 240
    self.bottom = 200
    pygame.init()
    pygame.mouse.set_visible(False)
    #  If this hangs, it's because something else is using the screen. Ctrl-C
    #  here will bypass that.
    signal(SIGALRM, alarm_handler)
    alarm(2)
    try:
      logging.info(
          "Attempting to initialise the display. Waiting up to two seconds.")
      self.screen = pygame.display.set_mode((self.width, self.height))
      alarm(0)
    except Alarm:
      raise KeyboardInterrupt
    self.clocksurface = pygame.Surface((self.width, self.bottom)).convert()
    self.messagesurface = pygame.Surface(
            (self.width, self.height - self.bottom)).convert()

    self.bigfont = pygame.font.SysFont("verdana", 90)
    self.smallfont = pygame.font.SysFont("verdana", 18)
    self.clock = pygame.time.Clock()

  def add_events(self):
    """Add the events we care about."""
    self.eventlist.add(events.Event(
        (19, 0), (20, 00), "Bedtime. Goodnight, Biz! Sleep well!"))
    self.eventlist.add(events.Event(
        (20, 0), (23, 59), "Too early. Go back to sleep, Biz"))
    self.eventlist.add(events.Event(
        (0, 0), (6, 0), "Too early. Go back to sleep, Biz"))
    self.eventlist.add(events.Event(
        (6, 0), (7, 0), "Time to read, Biz"))
    self.eventlist.add(events.Event(
        (7, 0), (7, 15), "It's morning! Wake up, parents!"))
    self.eventlist.add(events.Event(
        (7, 15), (7, 30), "Get dressed and go downstairs, Biz!"))
    self.eventlist.add(events.Event(
        (7, 30), (8, 0), "Breakfast and get ready for school, Biz!"))

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
          self.eventlist.current(), True, WHITE)

      self.draw(color, nowstr, event)
      self.clock.tick(1) # every 1s

  def draw(self, color, nowstr, message):
    """Draw the clock with an optional message!"""
    self.clocksurface.fill(color)
    self.messagesurface.fill(color)

    self.clocksurface.blit(nowstr,
                           ((self.width - nowstr.get_width()) / 2,
                            (self.bottom - nowstr.get_height()) / 2))
    self.messagesurface.blit(
            message, ((self.width - message.get_width()) / 2,
                (self.height - self.bottom - message.get_height()) / 2))
    pygame.display.flip()


def main():
  """Make a clock and run forever."""
  clock = ToddlerClock()
  clock.run()

main()
