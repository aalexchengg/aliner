import pygame as pg
from utils import load_image, rect_distance
class Obstacle(pg.sprite.Sprite):
    def __init__(self, image, scale=0.4, can_activate=False, colorkey=(250, 239, 253), text = None, scene = None, left=None, right=None, top=None, bottom=None, centerx=None, centery=None):
        pg.sprite.Sprite.__init__(self)
        self.scale = scale
        self.colorkey = colorkey
        self.image, self.rect = load_image(image, scale = self.scale, colorkey = self.colorkey)
        self.can_activate = can_activate
        self.text = text
        self.scene = scene
        self.activated = -1
        self.activation_distance = 10
        if(left):
            self.rect.left = left
        if(right):
            self.rect.right = right
        if(top):
            self.rect.top = top
        if(bottom):
            self.rect.bottom = bottom
        if(centerx):
            self.rect.centerx = centerx
        if(centery):
            self.rect.centery = centery
    
    def update(self, character, group):
        if(self.can_activate):
            distance = rect_distance(self.rect, character.rect)
            if(distance < self.activation_distance and not self.activated):
                self.add(group)
                self.activated = 1
            elif(distance > self.activation_distance and self.activated):
                self.remove(group)
                self.activated = 0
        

    
    