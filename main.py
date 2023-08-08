import pygame as pg
from sprite import Character
from furniture import Obstacle
from utils import *
from activated import Activated
from info import FILE_PATHS, SCALES, TEXT
import asyncio
import os

BG_COLORKEY = (250, 239, 253)
SPRITE_SCALE = 0.5

print(os.getcwd())
font_file_path = "data/fonts/PixeloidMono-d94EV.ttf"
char_file_path = "data/img/sprites"
# font_file_path = "./fonts/PixeloidMono-d94EV.ttf"
# char_file_path = ".\img\sprites"
pg.init()
# screen = pg.display.set_mode((960, 480), pg.SCALED)
screen = pg.display.set_mode((960, 625.25), pg.SCALED)
pg.display.set_caption("Rory's World")
pg.mouse.set_visible(False)

# Create The Backgound
background = pg.Surface(screen.get_size())
background = background.convert()
background.fill((216, 249, 255))
if pg.font:
    font = pg.font.Font(font_file_path, 12)
    text = font.render("Rory's World", True, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
    background.blit(text, textpos)
screen.blit(background, (0,0))
pg.display.flip()

srect = screen.get_rect() # screen rect

clock = pg.time.Clock()
character = Character(char_file_path, screen, colorkey = BG_COLORKEY)
character.rect.center = srect.center
backwall = Obstacle(FILE_PATHS["backwall"], scale = SCALES["backwall"], left=srect.left, top = srect.top)
backwall_bottom = Obstacle(FILE_PATHS["wallbottom"], scale = SCALES["wallbottom"], left=srect.left, top = backwall.rect.bottom)
bed = Obstacle(FILE_PATHS['bed'], scale = SCALES["bed"], left=srect.left, bottom = srect.bottom)
pickle = Obstacle(FILE_PATHS['pickle'], scale = SCALES["pickle"], left=srect.left, bottom = bed.rect.top)
dresser = Obstacle(FILE_PATHS['dresser'], can_activate=True, text = TEXT['dresser'],left = bed.rect.right, bottom = srect.bottom)
corner = Obstacle(FILE_PATHS['corner'], scale = SCALES['corner'], right = srect.right, bottom = srect.bottom)
desk = Obstacle(FILE_PATHS['desk'], can_activate=True, text = TEXT['desk'],scale = SCALES['desk'], right = srect.right, bottom = corner.rect.top)
window_bottom = Obstacle(FILE_PATHS['windowbot'], can_activate=True, text = TEXT['windowbot'], scale = SCALES['windowbot'], centerx = backwall.rect.centerx, top = backwall.rect.bottom)
window_top = Obstacle(FILE_PATHS['windowtop'], colorkey = (0,0,0), scale = SCALES['windowtop'], centerx = backwall.rect.centerx, bottom = backwall.rect.bottom)

carpet_tile,_ = load_image(FILE_PATHS['carpet_tile'], scale=SCALES['carpet_tile'])
bg = pg.sprite.Group((backwall, backwall_bottom))
allsprites = pg.sprite.RenderPlain((character))
furniture = pg.sprite.Group((bed, dresser, corner, desk, pickle, window_bottom, window_top))
activated = Activated(corner.rect, font_file_path)
async def main():
    # going = True
    while True:
        clock.tick(15)
        mvmt = [0,0]
        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                return
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_w]:
            mvmt[1] += -1
        if keys_pressed[pg.K_s]:
            mvmt[1] += 1
        if keys_pressed[pg.K_a]:
            mvmt[0] += -1
        if keys_pressed[pg.K_d]:
            mvmt[0] += 1
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
        await asyncio.sleep(0)
    # pg.quit()

# main()

asyncio.run(main())