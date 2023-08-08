import pygame as pg
import math

def load_image(name, colorkey=None, scale=1):
    pg.init()
    image = pg.image.load(name)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def print_rect(rect):
    print(f"top: {rect.top} bottom: {rect.bottom}")
    print(f"left: {rect.left} right: {rect.right}")

def tileBackground(screen, image) -> None:
    screenWidth, screenHeight = screen.get_size()
    imageWidth, imageHeight = image.get_size()
    
    # Calculate how many tiles we need to draw in x axis and y axis
    tilesX = math.ceil(screenWidth / imageWidth)
    tilesY = math.ceil(screenHeight / imageHeight)
    
    # Loop over both and blit accordingly
    for x in range(tilesX):
        for y in range(tilesY):
            screen.blit(image, (x * imageWidth, y * imageHeight))


def rect_distance(rect1, rect2, verbose = False):
    x1, y1 = rect1.topleft
    x1b, y1b = rect1.bottomright
    x2, y2 = rect2.topleft
    x2b, y2b = rect2.bottomright
    left = x2b < x1
    right = x1b < x2
    top = y2b < y1
    bottom = y1b < y2
    if bottom and left:
        if(verbose):
            print('bottom left')
        return math.hypot(x2b-x1, y2-y1b)
    elif left and top:
        if(verbose):
            print('top left')
        return math.hypot(x2b-x1, y2b-y1)
    elif top and right:
        if(verbose):
            print('top right')
        return math.hypot(x2-x1b, y2b-y1)
    elif right and bottom:
        if(verbose):
            print('bottom right')
        return math.hypot(x2-x1b, y2-y1b)
    elif left:
        if(verbose):
            print('left')
        return x1 - x2b
    elif right:
        if(verbose):
            print('right')
        return x2 - x1b
    elif top:
        if(verbose):
            print('top')
        return y1 - y2b
    elif bottom:
        if(verbose):
            print('bottom')
        return y2 - y1b
    else:  # rectangles intersect
        if(verbose):
            print('intersection')
        return 0.


def highlight_rect(screen, rect):
    pg.draw.rect(screen, (255,215,0), rect, 3)

def text_to_list(filepath, character_width=None):
    res = []
    with open(filepath) as file:
        for line in file:
            temp = ""
            for word in line.split():
                if(character_width != None and len(temp + " " + word) > character_width):
                    res.append(temp)
                    temp = word
                else:
                    temp = temp + " " + word
            if(temp != ""):
                res.append(temp)
    return res

def get_character_dims(font, surface, margins=0, lines=10):
    max_width,_ = surface.get_size()
    max_width -= 2*margins
    word_surface = font.render("MW", 0, pg.Color('black'))
    word_width, word_height = word_surface.get_size()
    word_width = word_width/2
    return ((max_width//word_width) - 1, word_height*lines)


# def get_videos(query):
#     res = []
#     youtube = googleapiclient.discovery.build(
#     api_service_name, api_version, developerKey = key)
#     request = youtube.search().list(
#         part="id,snippet",
#         type='video',
#         q=query,
#         videoDuration='short',
#         videoDefinition='high',
#         maxResults=3
# )
#     response = request.execute()
#     for item in response['items']:
#         title = item['snippet']['title']
#         img = item['snippet']['thumbnails']['default']['url']
#         link = "https://www.youtube.com/watch?v={}".format(item['id']['videoId'])
#         temp = {"title": title, "img": img, "url": link}
#         res.append(temp)
#     return res
