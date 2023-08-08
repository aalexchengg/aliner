import pygame as pg
from utils import tileBackground
from info import MAXLINES, MARGIN, LINEHEIGHT, FIRSTY
import webbrowser

class SceneManager():
    def __init__(self, screen, background, scenes=dict()):
        pg.init()
        self.currscene = None
        self.scenes = scenes
        self.screen = screen
        self.background = background
        self.cache = dict()
    
    def update(self, key, scene):
        self.currscene = key
    
    def add_scene(self, title, func, **kwargs):
        args = []
        for key, value in kwargs.items():
            args.append(key)
            self.cache[key] = value
        self.scenes[title] = (func, args)
        if self.currscene == None:
            self.currscene = title
    
    def run_scene(self, events, keys_pressed):
        func, args = self.scenes[self.currscene]
        variables = dict()
        for arg in args:
            variables[arg] = self.cache[arg]
        self.currscene = func(screen=self.screen, background=self.background, events = events, keys_pressed = keys_pressed,**variables)
        return

def bedroom(screen, background, events, keys_pressed, allsprites, character, furniture, bg, activated, carpet_tile):
    for event in events:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
    mvmt = [0,0]
    # keys_pressed = pg.key.get_pressed()
    if keys_pressed[pg.K_w]:
        mvmt[1] += -1
    if keys_pressed[pg.K_s]:
        mvmt[1] += 1
    if keys_pressed[pg.K_a]:
        mvmt[0] += -1
    if keys_pressed[pg.K_d]:
        mvmt[0] += 1
    if activated:
        if keys_pressed[pg.K_RETURN]:
            activation = activated.activate(True)
            if(activation):
                print(activation)
                return activation
    character.update(mvmt, furniture)
    furniture.update(character, activated)
    screen.blit(background, (0, 0))
    tileBackground(screen, carpet_tile)
    bg.draw(screen)
    activated.draw(screen)
    furniture.draw(screen)
    activated.type(screen)
    allsprites.draw(screen)
    pg.display.flip()
    return "bedroom"

class Start():
    def __init__(self):
        self.start = 0

def letter(screen, background, events, keys_pressed, allsprites, furniture, bg, activated, carpet_tile, start, paper, font, text, shade):
    # print(" in letter")
    for event in events:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            activated.deactivate()
            return "bedroom"
        if(event.type == pg.MOUSEWHEEL):
                start.start = start.start - event.y
        elif(event.type == pg.KEYDOWN and event.key == pg.K_DOWN):
            start.start = start.start + 2
        else:
            # keys_pressed = pg.key.get_pressed()
            if keys_pressed[pg.K_UP]:
                start.start = start.start - 2
            if keys_pressed[pg.K_DOWN]:
                start.start = start.start + 2
            start.start = max(start.start, 0)
    start.start = max(start.start, 0)
    start.start = min(start.start, len(text) - MAXLINES)
    end = start.start + MAXLINES
    print(start.start, end)
    screen.blit(background, (0, 0))
    tileBackground(screen, carpet_tile)
    bg.draw(screen)
    activated.draw(screen)
    furniture.draw(screen)
    activated.type(screen)
    allsprites.draw(screen)
    screen.blit(shade, (0,0))
    screen.blit(paper, (MARGIN/2,FIRSTY + MARGIN/2))
    for i in range(start.start, end):
        screen.blit(font.render(text[i], True, (0,0,0)), (MARGIN, FIRSTY + 24*(i - start.start)))
    pg.display.flip()
    return "letter"
    

def laptop(screen, background, events, keys_pressed, allsprites, furniture, bg, activated, carpet_tile, videos, font, shade):
    for event in events:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            activated.deactivate()
            return "bedroom"
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            for sprite in videos.sprites():
                if sprite.rect.collidepoint(pos):
                    webbrowser.open(sprite.url)
    screen.blit(background, (0, 0))
    tileBackground(screen, carpet_tile)
    bg.draw(screen)
    activated.draw(screen)
    furniture.draw(screen)
    activated.type(screen)
    allsprites.draw(screen)
    screen.blit(shade, (0,0))
    videos.draw(screen, font)
    pg.display.flip()
    return "laptop"
        
