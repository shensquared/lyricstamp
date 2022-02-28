import pygame
import os
import argparse
import player_control
import time
# import re
from get_lyricstexts import get_texts
from phonetics import add_phonetics

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)


def stamp_internal(pos):
    m = str(int(pos / 60)).rjust(2, '0')
    s = str(round(pos % 60, 3)).rjust(2, '0')
    return "[" + m + ":" + s + "]"


def save_lyrics(lines, stamps, out_name):
    home = os.path.expanduser("~")
    path = home + '/Music/LyricsX'
    out_name += '.lrcx'
    with open(os.path.join(path, out_name), "w") as f:
        [f.write(i + j + '\n') for (i, j) in zip(stamps, lines)]
    print('Saved ' + out_name + ' in ' + path)


def get_song_info(p, space, counter):
    if counter == -2:
        out_name = ''
        lines = ['']
        secs = ['']
        stamps = ['']
        width, height = (800, 600)
    else:
        title, artist = player_control.now_playing()
        out_name = title + ' - ' + artist
        in_name = 'lyrics.txt'
        if in_name:
            with open(in_name) as f:
                lines = [line.replace('\n', '') for line in f.readlines() if line.strip()]
        else:
            lines = get_texts(title, artist)

        lines = add_phonetics(lines, p)
        lines.insert(0, out_name)
        secs = [0] * len(lines)
        stamps = [''] * len(lines)
        num_chars = (max([len(i) for i in lines]) + 10)
        (width, height) = (num_chars * space[0], 16 * space[1])
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('LyricStamp: ' + out_name)
    return out_name, lines, secs, stamps, screen


def print_info(screen, counter, lines, stamps, out_name, font):
    def text_to_screen(text, y, color):
        try:
            text = font.render(text, True, color)
            # everything starts at x=20
            screen.blit(text, (20, y))
        except Exception as e:
            raise e

    def screen_banner(*vargs):
        [text_to_screen(j, 10 + k * space[1], RED) for (k, j) in enumerate(vargs)]

    space = font.size('A')
    h = space[1]

    if counter == -1:
        welcome_msg = ["Now let's get the lyrics",
                       "Or, drop a text file into this window for ",
                       "",
                       "",
                       "Supported phonetics:",
                       "-Romaji for Japanese (type in 'J')",
                       "-Jyutping for Cantonese (type in 'Y')"]
        # n = len(welcome_msg)
        screen_banner(*welcome_msg)
        cursor = pygame.Rect((50 + 3.5 * space[0], h * 10), (3, h))

    elif counter == -2:
        welcome_msg = ["Type in the language code if wanna phonetics added.",
                       "Press the Right Arrow ➡ to skip",
                       "",
                       "",
                       "Supported phonetics:",
                       "-Romaji for Japanese (type in 'J')",
                       "-Jyutping for Cantonese (type in 'Y')"]
        # n = len(welcome_msg)
        screen_banner(*welcome_msg)
        cursor = pygame.Rect((50 + 3.5 * space[0], h * 10), (3, h))
    else:
        topleft = (20 + 3.5 * space[0], h * (counter - max(counter, 2)+5.3))
        if lines[counter + 1].startswith('[tr]'):
            h = 2 * h
        cursor = pygame.Rect(topleft, (3, h*.9))
        for i, l in enumerate(lines):
            if counter - 3 < i < max(counter, 2) + 9:
                y = space[1] * (i - max(counter, 2) + 5)
                text_to_screen(str(i).zfill(3) + ': ' + stamps[i] + l, y, BLACK)
        if counter >= len(lines):
            screen_banner("Press Enter to end stamping and confirm that", out_name + " will be saved")
        else:
            screen_banner("Press 'Down-Arrow' to go to the next line", "'Up-Arrow' to go back to the previous line.")
    return cursor


def main(in_name='lyrics.txt'):
    pygame.init()
    font = pygame.font.Font('fonts/NotoSansCJK-Light.ttc', 30)
    # seems that CJK fonts have a pretty good coverage of western chars. Hard-code for now.
    # TODO: check e.g. Korean and Spanish
    # font = pygame.font.Font('fonts/NotoSerifDisplay-Light.ttf', 30)
    space = font.size('A')
    p = None
    counter = -2
    out_name, lines, secs, stamps, screen = get_song_info(p, space, counter)
    screen.fill(GRAY)
    pygame.display.flip()

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            # if event.type==pygame.DROPFILE:
            #     (event.file)
            if event.type == pygame.KEYDOWN:
                if counter == -2:
                    if event.key == pygame.K_j:
                        p = 'J'
                    if event.key == pygame.K_y:
                        p = 'Y'
                    counter += 1
                if counter == -1:
                    out_name, lines, secs, stamps, screen = get_song_info(p, space, counter)
                    pygame.display.set_caption('LyricStamp: ' + out_name)
                    if event.key == pygame.K_RETURN:
                        counter=0
                if counter >= 0:
                    if event.key == pygame.K_RIGHT:
                        player_control.play_next()
                        out_name, lines, secs, stamps, screen = get_song_info(p, space, counter)
                        pygame.display.set_caption('LyricStamp: ' + out_name)
                    if event.key == pygame.K_SPACE and counter > 0:
                        player_control.play_pause()
                    if event.key == pygame.K_DOWN:
                        if counter == 0:
                            stamps[counter] = "[00:00.000]"
                            # player_control.play()
                        elif counter <= len(lines) - 1:
                            # insert new stamp into line; relies on iTunes/Music's internal player's position
                            pos = player_control.player_position()
                            secs[counter] = pos
                            stamps[counter] = stamp_internal(pos)
                            if counter <= len(lines) - 2 and lines[counter + 1].startswith('[tr]'):
                                counter += 1
                                secs[counter] = pos
                                stamps[counter] = stamp_internal(pos)
                        counter += 1
                    if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        counter -= 1
                        secs[counter] = 0
                        stamps[counter] = ''
                        if counter >= 0 and lines[counter].startswith('[tr]'):
                            counter -= 1
                            secs[counter] = 0
                            stamps[counter] = ''
                        if event.key == pygame.K_UP:
                            player_control.set_player_position(secs[counter - 1])
                if counter >= len(lines):
                    if event.key == pygame.K_RETURN:
                        save_lyrics(lines, stamps, out_name)
                        screen.fill(GRAY)
                if event.key == pygame.K_ESCAPE:
                    return
        screen.fill(GRAY)
        cursor = print_info(screen, counter, lines, stamps, out_name, font)
        if time.time() % 1 > 0.5:
            pygame.draw.rect(screen, RED, cursor)
        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=""".""")
    parser.add_argument("-i", "--in_name",
                        help="local file to read static lyrics from; if none supplied, fetch from e.g. genius.com")
    # parser.add_argument("--lang",
    #                     help="if the song/book is in Chinese (use CN), Japanese (use JP), or Korean (use KR).")
    args = parser.parse_args()
    in_name = args.in_name
    # lang = args.lang
    main(in_name)
