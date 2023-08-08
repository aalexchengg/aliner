
import pygame as pg
from utils import highlight_rect
class Activated(pg.sprite.Group):
    def __init__(self, textbox, font):
        pg.sprite.Group.__init__(self)
        self.textbox = textbox
        self.font = pg.font.Font(font, 12)
    

    def draw(self, screen):
        sprites = self.sprites()
        for sprite in sprites:
            highlight_rect(screen, sprite.rect)
    def activate(self, activate):
        sprites = self.sprites()
        if activate and len(sprites) == 1:
                sprites[0].activated = 2
                return sprites[0].scene
    def deactivate(self):
        sprites = self.sprites()
        if len(sprites) == 1:
            sprites[0].activated = 1
    def type(self, screen):
        sprites = self.sprites()
        if (len(sprites) == 1):
            lines = sprites[0].text[sprites[0].activated - 1].splitlines()
            for i, l in enumerate(lines):
                screen.blit(self.font.render(l, True, (0,0,0)), (self.textbox.x, self.textbox.y + 12*i))
