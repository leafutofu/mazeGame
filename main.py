import pygame, settings
pygame.init()

class Page(): #Allows for switching screens in one window
    def __init__(self, title, width=settings.WIDTH, height=settings.HEIGHT, fill=settings.BGCOLOUR):
        self.height = height
        self.width = width
        self.title = title
        self.fill = fill
        self.CurrentState = False

class Button():
    pass