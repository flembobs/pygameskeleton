##############################################################################
# gamestate.py
##############################################################################
# Classes related to the game play state.
##############################################################################
# 12/12 Flembbobs
##############################################################################

import pygame

from engine.abs.gameobject import GameObject
from engine.abs.state import State
from engine.abs.events import *
from engine.systemevents import *

##############################################################################
# GAME EVENTS
##############################################################################

class ManMoveRequest(Event):
   """
   Generated by the game event manager when the player is requested to move.
   """
   
   def __init__(self,move_by):
      """
      move_by - tuple of amount to move by (x_amount,y_amount)
      """
      self.move_by = move_by
      
##############################################################################
# GAME EVENTS - MANAGER AND LISTENER CLASSES
##############################################################################

class GameEventManager(EventManager):
   pass

class GameEventListener(Listener):
   pass

##############################################################################
# GAME OBJECTS - MAN
##############################################################################

class Man(GameObject,GameEventListener):
   
   def __init__(self,game_event_manager,pos):
      GameEventListener.__init__(self,game_event_manager)

      self.pos = pos
      
   #--------------------------------------------------------------------------
          
   def render(self,surface):
      pygame.draw.rect(surface,(0,255,0),pygame.Rect(self.pos,(16,16)))
      
   #--------------------------------------------------------------------------
   
   def notify(self,event):
      
      if isinstance(event,ManMoveRequest):
         self.pos = (self.pos[0]+event.move_by[0],\
                     self.pos[1]+event.move_by[1])

##############################################################################
# GAME STATE CLASS
##############################################################################

class GameState(State,SystemEventListener):

   def __init__(self):
      """
      Note - states implement the SystemEventListener interface, but they
             do not directly listen to the system events manager.  Events
             are passed to them by the model.  Thus they do not call the
             event listener super constructor.
      """
      State.__init__(self)
      self.game_event_manager = GameEventManager()
      
      self.man = Man(self.game_event_manager,(240,240))
      self.game_objects.append(self.man)
      
   #--------------------------------------------------------------------------
   
   def notify(self,event):
      if isinstance(event,KeyboardEvent):
         if event.key == pygame.K_ESCAPE:
            self.model.system_event_manager.post(QuitEvent()) 
            
      if isinstance(event,KeyboardEvent):
         if event.type == pygame.KEYDOWN:
            
            move_request = None
            
            if event.key == pygame.K_UP:
               move_request = ManMoveRequest((0,-16))
            if event.key == pygame.K_DOWN:
               move_request = ManMoveRequest((0,16))
            if event.key == pygame.K_RIGHT:
               move_request = ManMoveRequest((16,0))
            if event.key == pygame.K_LEFT:
               move_request = ManMoveRequest((-16,0))
               
            self.game_event_manager.post(move_request)
               
               
   
