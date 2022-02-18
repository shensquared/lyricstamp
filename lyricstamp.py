# coding: utf-8
import pygame
import time
import os
import sys
from player_control import now_playing, play


# Modified from https://gist.github.com/seankmartin/f660eff4787b586f94d5f678932bcd27
def text_to_screen(screen, text, x, y, size=30, color=(000, 000, 000), font_type=''):
    # TODO: Non-western chars not displaying
    try:
        text = str(text)
        font = pygame.font.Font(None, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))
    except Exception as e:
        print('Font Error, saw it coming')
        raise e


def screen_banner(screen, text):
    text_to_screen(screen, text, 20, 10, size=30, color=(255, 000, 000))


def print_info(screen, lines, state):
    for i, l in enumerate(lines):
        text_to_screen(screen, l, 20, 20 * (i + 2))
    if state == -1:
        screen_banner(screen, "Press S to start playing the song (and reset timer)")
    elif state == 1:
        screen_banner(screen, "Press E to end")
    else:
        screen_banner(screen, "Press Down-arrow to go to the next line")


def save_lyrics(lines, out_name):
    home = os.path.expanduser("~")
    path = home + '/Music/LyricsX'
    out_name += '.lrcx'
    with open(os.path.join(path, out_name), "w") as f:
        [f.write(i) for i in lines]


def stamp(begin, end):
    time = end - begin
    m = str(int(time / 60)).rjust(2, '0')
    s = str(round(time % 60, 3)).rjust(2, '0')
    stamp = "[" + m + ":" + s + "]"
    return stamp


def main(in_name="lyrics.txt"):
    # state -1, 0, or 1. -1: haven't started stamping; 0: in the process; 1: at the last line
    with open(in_name) as f:
        lines = f.readlines()
    title, artist = now_playing()
    out_name = title + ' - ' + artist
    state = -1
    counter = 0
    background_colour = (255, 255, 255)

    (width, height) = (max([len(i) for i in lines]) * 10, len(lines) * 25)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('LyricStamp Timer')
    screen.fill(background_colour)
    pygame.display.flip()

    running = True
    clock = pygame.time.Clock()

    while running:
        # print(len(lines))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    state = 0
                    begin = time.time()
                    play()
                    lines.insert(0, "[00:00.000]" + out_name + "\n")
                if event.key == pygame.K_DOWN:
                    counter += 1
                    # insert new stamp into line
                    now = time.time()
                    lines[counter] = stamp(begin, now) + ' ' + lines[counter]
                    if counter == len(lines) - 1:
                        state = 1
                if event.key == pygame.K_e:
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
