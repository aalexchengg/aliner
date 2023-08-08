import pygame as pg
from utils import text_to_list, get_character_dims

MAXLINES=15
MARGIN = 10
LINEHEIGHT = 24

def main():

    font_file_path = "data/fonts/PixeloidMono-d94EV.ttf"
    pg.init()
    # screen = pg.display.set_mode((960, 480), pg.SCALED)
    screen = pg.display.set_mode((960, 625.25), pg.SCALED)
    pg.display.set_caption("08.07.2023")
    pg.mouse.set_visible(True)
    font = None
    # Create The Backgound
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((216, 249, 255))
    if pg.font:
        font = pg.font.Font(font_file_path, 24)
        text = font.render("Rory's World", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)
    screen.blit(background, (0,0))
    pg.display.flip()
    start = 0
    end = MAXLINES


    clock = pg.time.Clock()
    chars_per_line, char_height = get_character_dims(font, screen, MARGIN, MAXLINES)
    paper = pg.Surface((screen.get_width() - MARGIN, LINEHEIGHT*MAXLINES + MARGIN))
    paper = paper.convert()
    paper.fill((224, 226, 220))
    text = text_to_list("data\letter.txt", chars_per_line)
    print(len(text))
    going = True
    firsty = 90
    while going:
        clock.tick(15)
        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            if(event.type == pg.MOUSEWHEEL):
                start = start - event.y
            elif(event.type == pg.KEYDOWN and event.key == pg.K_DOWN):
                start = start + 2
            else:
                keys_pressed = pg.key.get_pressed()
                if keys_pressed[pg.K_UP]:
                    start = start - 2
                if keys_pressed[pg.K_DOWN]:
                    start = start + 2
        start = max(start, 0)
        start = min(start, len(text) - MAXLINES)
        end = start + MAXLINES
        # print("pstn")
        # print(start, end)
        screen.blit(background, (0, 0))
        screen.blit(paper, (MARGIN/2,firsty + MARGIN/2))
        for i in range(start, end):
            screen.blit(font.render(text[i], True, (0,0,0)), (MARGIN, firsty + 24*(i - start)))
        pg.display.flip()
    pg.quit()

main()