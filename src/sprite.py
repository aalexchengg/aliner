import pygame as pg
import os
from utils import load_image, print_rect


class Character(pg.sprite.Sprite):

    def load_images(self, path):
        res = {"front": [], "back": [], "left": [], "right":[]}
        for key in res.keys():
            for file in os.listdir(f"{path}/{key}"):
                res[key].append("{}/{}/{}".format(path, key, file))
        return res

    def get_image_path(self):
        return self.directory[self.orientation][self.animation_frame]

    def __init__(self, directory, screen, speed=10, scale = 0.4, colorkey=None):
        pg.sprite.Sprite.__init__(self)
        self.colorkey = colorkey
        self.directory = self.load_images(directory)
        self.animation_frame = 1
        self.speed = speed
        self.scale = scale
        self.movements = {(0,1): "front", (0, -1): "back", (1,0): "right", (-1,0): "left"}
        self.x, self.y = 0,0
        self.orientation = "front"
        self.image, self.rect = load_image(self.get_image_path(), colorkey = self.colorkey, scale = self.scale)
        self.area = screen.get_rect()
        self.rect_center = screen.get_rect().centerx, screen.get_rect().centery

    def update(self, movement, furniture):
        self._move(movement, furniture)
    

    def check_vert(self, rect1, rect2, inside = True):
        if(inside):
            if(rect1.top < rect2.top):
                rect1.top = rect2.top
            elif(rect1.bottom > rect2.bottom):
                rect1.bottom = rect2.bottom
            return rect1
        else:
            if(rect1.top < rect2.bottom and rect1.bottom > rect2.bottom):
                rect1.top = rect2.bottom
            elif(rect1.bottom > rect2.top and rect1.top < rect2.top):
                rect1.bottom = rect2.top
            return rect1

    def check_hori(self, rect1, rect2, inside = True):
        if(inside):
            if(rect1.left < rect2.left):
                rect1.left = rect2.left
            elif(rect1.right > rect2.right):
                rect1.right = rect2.right
            return rect1
        else:
            if(rect1.left < rect2.right and rect1.left > rect2.left):
                rect1.left = rect2.right
            elif(rect1.right > rect2.left and rect1.right < rect2.right):
                rect1.right = rect2.left
            return rect1

    def move_direction(self, x, y, furniture, func):
        self.rect = self.rect.move((x*self.speed, y*self.speed))
        if not (self.area.contains(self.rect)):
            self.rect = func(self.rect, self.area) 
            return 0
        # self.rect = newpos
        collisions = pg.sprite.spritecollide(self, furniture, dokill=False)
        if(len(collisions) == 0):
            return x if x != 0 else y
        for collision in collisions:
            self.rect = func(self.rect, collision.rect, inside = False)
        return 0

    def _move(self, movement, furniture):
        x,y = movement
        oldx, oldy = x,y
        prevx, prevy = self.x, self.y
        # move in x direction
        if(x !=0):
            x = self.move_direction(x, 0, furniture, self.check_hori)
        # move in y direction
        if(y!=0):
            y = self.move_direction(0, y, furniture, self.check_vert) 
        # if did not move, change to stand still animation
        if(x == 0 and y == 0):
            if(abs(oldx) != abs(oldy)): #pythons jank logical xor
                # to allow 90 degree rotation while standing still
                self.x, self.y = oldx, oldy
                self.orientation = self.movements[(oldx, oldy)]
            self.animation_frame = 1
            self.image, _ = load_image(self.get_image_path(), colorkey=self.colorkey, scale = self.scale)
            return
        #code to change animation frames
        if(prevx == x and prevy == y):
            #moving in the same direction
            self.animation_frame = (self.animation_frame + 1) % 3
        else:
            # new movement is diagonal
            if(x & y):
                if(prevx == x):
                    self.orientation = self.movements[(x,0)]
                    self.animation_frame = (self.animation_frame + 1) % 3
                else:
                    self.orientation = self.movements[(0,y)]
                    self.animation_frame = 0
            # new movement is straight
            else:
                self.orientation = self.movements[(x,y)]
                self.animation_frame = 0
        # update fields
        self.image, _ = load_image(self.get_image_path(), colorkey=self.colorkey, scale = self.scale)
        self.x, self.y = x,y


