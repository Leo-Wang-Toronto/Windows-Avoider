# A simple module to get user input allowing for backspace but not arrow keys or delete key
# Shown in a box in the middle of the screen,Only near the center of the screen is blitted to 
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
# colors and valid keys can be changed by changing the constants at the beginning of the program

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

BACKGROUND_COLOR = (0,0,0)
TEXT_COLOR = (255,255,255)
BOX_COLOR = (255,255,255)
VALID_KEYS = 'abcdefghijklmnopqrstuvwxyz 0123456789'
capsOn = False

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  if len(message) != 0:
    fontobject = pygame.font.Font(None,18)
    #rect(Surface, color, Rect, width=0)
    message_surface = fontobject.render(message, 1, TEXT_COLOR)
    recWidth = message_surface.get_width() + 10
    if recWidth < 300:
      recWidth = 300
  else:
    recWidth = 300
    
  pygame.draw.rect(screen, BACKGROUND_COLOR,
                   ((screen.get_width() / 2) - 140,
                    150,
                    recWidth,30), 0)
  pygame.draw.rect(screen, BOX_COLOR,
                   ((screen.get_width() / 2) - 140,
                    150,
                    recWidth,30), 1)
  if len(message) != 0:
    screen.blit(message_surface,
                ((screen.get_width() / 2) - 135, 155))
  pygame.display.flip()

def ask(screen, question):
  global capsOn, VALID_KEYS
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + ''.join(current_string))
  enteringText = True
  while enteringText:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == K_LSHIFT or event.key == K_RSHIFT:
          capsOn = True
      
        if event.key == K_BACKSPACE:
          current_string = current_string[0:-1]
        if event.key == K_RETURN:
          enteringText = False
        if event.key == K_MINUS:
          current_string.append("_")
        if chr(event.key) in VALID_KEYS:
          inkeyLtr = chr(event.key)
          if capsOn:
            inkeyLtr = inkeyLtr.upper()
          current_string.append(inkeyLtr)
      if event.type == pygame.KEYUP:
        if event.key == K_LSHIFT or event.key == K_RSHIFT:
          capsOn = False

    display_box(screen, question + ": " + ''.join(current_string))  
  return ''.join(current_string)

def main():
  screen = pygame.display.set_mode((320,240))
  screen.fill((0,255,255))
  print (ask(screen, "Name") + " was entered")

if __name__ == '__main__': main()
