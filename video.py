import pygame as pg
import os
from utils import load_image, print_rect
from info import MARGIN

class Video(pg.sprite.Sprite):

    def __init__(self, info, order,scale = 0.4, colorkey = None):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(info['img'], colorkey =colorkey,scale = scale)
        self.url = info['url']
        self.title = info['title']
        self.rect.left = MARGIN
        self.rect.top = order*(MARGIN + self.rect.height)


class Videos(pg.sprite.Group):
    def __init__(self):
        pg.sprite.Group.__init__(self)
    
    def draw(self, screen, font):
        pg.sprite.Group.draw(self, screen)
        for video in self.sprites():
            title = font.render(video.title, True, (0,0,0))
            screen.blit(title, (video.rect.top, video.rect.right + MARGIN))

