import pygame
from reference import *

class MenuItem:
    def __init__(self, text:str, color, x:int, y:int, width:int, height:int, screen, font, spacing = (0, 0)):
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.font = font
        self.spacing = spacing

    def draw_text(self, transparency):
        shown_text = self.font.render(self.text, True, self.color)
        shown_text.set_alpha(transparency)
        self.screen.blit(shown_text, (self.x + self.spacing[0], self.y + self.spacing[1]))


