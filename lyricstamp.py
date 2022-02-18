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


def screen_banner(screen, text, y=10):
    text_to_screen(screen, text, 20, y, size=30, color=(255, 000, 000))


def print_info(screen, lines, counter, out_name=''):
    for i, l in enumerate(lines):
        if counter - 3 < i < counter + 10:
            text_to_screen(screen, str(i) + ': ' + l, 20, 20 * (i - counter + 6))
    if counter == 0:
        screen_banner(screen, "Press 'Down-Arrow' to start playing")
        screen_banner(screen, "and reset the timer", y=30)
    elif counter == len(lines):
        screen_banner(screen, "Press Enter to end stamping and confirm")
        screen_banner(screen, out_name + "will be saved", y=30)
    else:
        screen_banner(screen, "Press 'Down-Arrow' to go to the next line")


def save_lyrics(lines, out_name):
    home = os.path.expanduser("~")
    path = home + '/Music/LyricsX'
    out_name += '.lrcx'
    with open(os.path.join(path, out_name), "w") as f:
        [f.write(i) for i in lines]
    print('Saved ' + out_name + ' in ' + path)


def stamp(begin, end):
    time = end - begin
    m = str(int(time / 60)).rjust(2, '0')
    s = str(round(time % 60, 3)).rjust(2, '0')
    return "[" + m + ":" + s + "]"


def main(in_name="lyrics.txt"):
    with open(in_name) as f:
        lines = f.readlines()
    title, artist = now_playing()
    out_name = title + ' - ' + artist
    lines.insert(0, out_name + "\n")
    counter = 0
    background_colour = (255, 255, 255)
    (width, height) = (max([len(i) for i in lines]) * 10, 15 * 25)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('LyricStamp Timer')
    screen.fill(background_colour)
    pygame.display.flip()

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    print("Current cursor counter is at: " + str(counter))
                    if counter == 0:
                        play()
                        lines[counter] = "[00:00.000]" + ' ' + lines[counter]
                        begin = time.time()
                    elif counter <= len(lines) - 1:
                        # insert new stamp into line
                        now = time.time()
                        lines[counter] = stamp(begin, now) + ' ' + lines[counter]
                    counter += 1
                if event.key == pygame.K_RETURN and counter == len(lines):
                    save_lyrics(lines, out_name)
                    running = False
                    pygame.quit()
                    break
                if event.key == pygame.K_ESCAPE:
                    return
            screen.fill(background_colour)
            print_info(screen, lines, counter, out_name)
            pygame.display.update()
            clock.tick(40)


if __name__ == "__main__":
    # in_name = sys.argv[0]
    main()
