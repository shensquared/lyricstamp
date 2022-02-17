import pygame
import time
import os
import sys
from player import now_playing

# Modified from https://gist.github.com/seankmartin/f660eff4787b586f94d5f678932bcd27
def text_to_screen(screen, text, x, y, size=50, color=(000, 000, 000), font_type='Comic Sans MS'):
    try:
        text = str(text)
        font = pygame.font.SysFont(font_type, 12)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))
    except Exception as e:
        print('Font Error, saw it coming')
        raise e

def print_info(screen, lines, state):
    for i, l in enumerate(lines):
        text_to_screen(screen, l, 20, 20 * (i + 1))
    if state == -1:
        text_to_screen(screen, "Press S to start", 20, 20 * (len(lines) + 2))
    elif state == 1:
        text_to_screen(screen, "Press E to end", 20, 20 * (len(lines) + 2))
    else:
        text_to_screen(screen, "Press Down-arrow to go to the next line", 20, 20 * (len(lines) + 2))

def save_lyrics(lines, file):
    home = os.path.expanduser("~")
    path = home + '/Music/LyricsX'
    with open(os.path.join(path, file), "w") as f:
        [f.write(i) for i in lines]


def stamp(begin, end):
    time = end - begin
    m = str(int(time/60)).rjust(2,'0')
    s=str(round(time%60,3)).rjust(2,'0')
    stamp ="["+m+":"+s+"]"
    return stamp

def main(in_name="lyrics.txt"):
    # state -1, 0, or 1. -1: haven't started stamping; 0: in the process; 1: at the last line
    with open(in_name) as f:
        lines = f.readlines()
    out_name = now_playing() + '.lrcx'
    state = -1
    counter = -1
    background_colour = (255, 255, 255)

    (width, height) = (max([len(i) for i in lines])*10, len(lines)*25)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('LyricSync Timer')
    screen.fill(background_colour)
    pygame.display.flip()

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                counter += 1
                if event.key == pygame.K_s:
                    state = 0
                    begin = time.time()
                    lines[counter] = stamp(begin,begin) + ' ' + lines[counter]
                if event.key == pygame.K_DOWN:
                    # insert new stamp into line
                    now = time.time()
                    lines[counter] = stamp(begin, now) + ' ' + lines[counter]
                    if counter==len(lines):
                        state = 1
                if event.key == pygame.K_e:
                    # now = time.time()
                    # lines.insert(0, )
                    save_lyrics(lines, out_name)
                    running = False
                    pygame.quit()
                    break
            screen.fill(background_colour)
            print_info(screen, lines, state)
            pygame.display.update()
            clock.tick(40)

if __name__ == "__main__":
    # in_name = sys.argv[0]
    main()