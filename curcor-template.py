import pygame
# from pygame.locals import *
import time

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode((640, 240))

text = 'this text is editable'
font = pygame.font.SysFont(None, 48)
img = font.render(text, True, RED)

rect = img.get_rect()
rect.topleft = (20, 20)
cursor = pygame.Rect(rect.topright, (3, rect.height))

running = True
background = GRAY

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(text) > 0:
                    text = text[:-1]
            if event.key == pygame.K_RETURN:
                # This means to look for data.
                pygame.scrap.init()
                pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
                print("Getting the different clipboard data..")
                for t in pygame.scrap.get_types():
                    r = pygame.scrap.get(t)
                    if r and len(r) > 500:
                        print("Type %s : (large %i byte buffer)" % (t, len(r)))
                    elif r is None:
                        print("Type %s : None" % (t,))
                    else:
                        print("Type %s : '%s'" % (t, r.decode("ascii", "ignore")))
                    texts = r.decode('UTF-8')

            else:
                text += event.unicode
            img = font.render(text, True, RED)
            rect.size = img.get_size()
            cursor.topleft = rect.topright
        if event.type == pygame.DROPFILE:
            event
            print(event.file)

    screen.fill(background)
    screen.blit(img, rect)
    if time.time() % 1 > 0.5:
        pygame.draw.rect(screen, RED, cursor)
    pygame.display.update()

pygame.quit()
