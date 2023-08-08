import pygame as pg
from sprite import Character
from furniture import Obstacle
from utils import *
from activated import Activated
from info import FILE_PATHS, SCALES, TEXT, MARGIN, LINEHEIGHT, MAXLINES
import asyncio
import os
from manager import SceneManager, bedroom, letter, laptop, Start
# from video import Video, Videos

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

# Create The Backgound
background = pg.Surface(screen.get_size())
background = background.convert()
background.fill((216, 249, 255))
shade = pg.Surface(screen.get_size())
shade = shade.convert()
shade.set_alpha(128)
shade.fill((0,0,0))

font = None
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
dresser = Obstacle(FILE_PATHS['dresser'], can_activate=False, text = TEXT['dresser'],left = bed.rect.right, bottom = srect.bottom)
corner = Obstacle(FILE_PATHS['corner'], scale = SCALES['corner'], right = srect.right, bottom = srect.bottom)
desk = Obstacle(FILE_PATHS['desk'], can_activate=False, text = TEXT['desk'],scale = SCALES['desk'], right = srect.right, bottom = corner.rect.top)
window_bottom = Obstacle(FILE_PATHS['windowbot'], can_activate=True, text = TEXT['windowbot'], scene = "letter", scale = SCALES['windowbot'], centerx = backwall.rect.centerx, top = backwall.rect.bottom)
window_top = Obstacle(FILE_PATHS['windowtop'], colorkey = (0,0,0), scale = SCALES['windowtop'], centerx = backwall.rect.centerx, bottom = backwall.rect.bottom)

carpet_tile,_ = load_image(FILE_PATHS['carpet_tile'], scale=SCALES['carpet_tile'])
bg = pg.sprite.Group((backwall, backwall_bottom))
allsprites = pg.sprite.RenderPlain((character))
furniture = pg.sprite.Group((bed, dresser, corner, desk, pickle, window_bottom, window_top))
activated = Activated(corner.rect, font_file_path)

start = Start()
chars_per_line, char_height = get_character_dims(font, screen, MARGIN, MAXLINES)
paper = pg.Surface((screen.get_width() - MARGIN, LINEHEIGHT*MAXLINES + MARGIN))
paper = paper.convert()
paper.fill((224, 226, 220))
text = text_to_list("data\letter.txt", chars_per_line)
print(len(text))

# video_info = get_videos("Stephanie Soo")
# videos = Videos()
# for i, info in enumerate(video_info):
#     videos.add(Video(info, scale=0.3, order = i))

manager = SceneManager(screen, background)
bedroom_args = {"allsprites": allsprites, "character": character, "furniture": furniture, "bg": bg, "activated": activated, "carpet_tile": carpet_tile}
manager.add_scene("bedroom", bedroom, **bedroom_args)
letter_args = {"allsprites": allsprites, "furniture": furniture, "bg": bg, "activated": activated, "carpet_tile": carpet_tile, "start": start, "paper": paper, "font": font, "text": text, "shade": shade}
manager.add_scene("letter", letter, **letter_args)
# video_args = {"allsprites": allsprites, "furniture": furniture, "bg": bg, "activated": activated, "carpet_tile": carpet_tile,"font": font, "videos" : videos, "shade": shade}
# manager.add_scene("laptop", laptop, **video_args)

async def main():
    going = True
    while going:
        clock.tick(15)
        # Handle Input Events
        events = pg.event.get()
        keys_pressed = pg.key.get_pressed()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                return
            # elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            #     pg.quit()
            #     return
        manager.run_scene(events, keys_pressed)
        await asyncio.sleep(0)
    # pg.quit()

# main()

asyncio.run(main())