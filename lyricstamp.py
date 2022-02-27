import pygame
import os
import argparse
import player_control
# import time
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


def get_song_info(phonectics):
    title, artist = player_control.now_playing()
    out_name = title + ' - ' + artist
    in_name = 'lyrics.txt'
    if in_name:
        with open(in_name) as f:
            lines = [line.replace('\n', '') for line in f.readlines() if line.strip()]
    else:
        lines = get_texts(title, artist)
    if phonectics:
        lines = add_phonetics(lines)
    lines.insert(0, out_name)
    counter = 0
    secs = [0] * len(lines)
    stamps = [''] * len(lines)
    return out_name, lines, counter, secs, stamps


def print_info(screen, counter, lines, stamps, out_name, font):
    # TODO: add a cursor here https://pygame.readthedocs.io/en/latest/4_text/text.html#initialize-a-font
    def text_to_screen(text, y, color):
        try:
            text = font.render(text, True, color)
            # everything starts at x=20
            screen.blit(text, (20, y))
        except Exception as e:
            raise e

    def screen_banner(*vargs):
        [text_to_screen(j, 10 + i * space[1], RED) for (i, j) in enumerate(vargs)]

    space = font.size('A')
    for i, l in enumerate(lines):
        if i == counter - 1:
            c = RED
        else:
            c = BLACK
        if counter - 3 < i < max(counter, 2) + 9:
            text_to_screen(str(i) + ': ' + stamps[i] + l, space[1] * (i - max(counter, 2) + 5), c)
    # if counter == 0:
    #     screen_banner("Press 'Down-Arrow'", "to start the media playing and reset t")
    if counter >= len(lines):
        screen_banner("Press Enter to end stamping and confirm that", out_name + " will be saved")
    else:
        screen_banner("Press 'Down-Arrow' to go to the next line", "'Up-Arrow' to go back to the previous line.")


def main(in_name='lyrics.txt', phonectics=True):
    pygame.init()
    # Setup interface
    font = pygame.font.Font('fonts/NotoSansCJK-Light.ttc', 30)
    # seems that CJK fonts have a pretty good coverage of western chars. Hard-code for now.
    # TODO: check e.g. Korean and Spanish
    # font = pygame.font.Font('fonts/NotoSerifDisplay-Light.ttf', 30)

    out_name, lines, counter, secs, stamps = get_song_info(phonectics)
    num_chars = (max([len(i) for i in lines]) + 10)
    space = font.size('A')
    (width, height) = (num_chars * space[0], 16 * space[1])
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('LyricStamp: ' + out_name)
    screen.fill(GRAY)
    pygame.display.flip()

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            # if event.type==pygame.DROPFILE:
            #     (event.file)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_control.play_next()
                    out_name, lines, counter, secs, stamps = get_song_info(phonectics)
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
            print_info(screen, counter, lines, stamps, out_name, font)
            pygame.display.update()
            clock.tick(10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=""".""")
    parser.add_argument("--in_name",
                        help="local file to read static lyrics from; if none supplied, fetch from e.g. genius.com")
    # parser.add_argument("--lang",
    #                     help="if the song/book is in Chinese (use CN), Japanese (use JP), or Korean (use KR).")
    args = parser.parse_args()
    in_name = args.in_name
    # lang = args.lang
    main(in_name)
