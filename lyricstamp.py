import pygame as pg
import pygame.scrap as scrap
import os
# import argparse
import player_control
import time
# clean up get_texts
from get_lyricstexts import get_texts, cleanup, musicsmatch
from phonetics import add_phonetics

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
space = (18, 44)


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


def welcome():
    out_name = 'Settings'
    lines = ['']
    secs = ['']
    stamps = ['']
    width, height = (1200, 900)
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption('LyricStamp: ' + out_name)
    return out_name, lines, secs, stamps, screen


def get_song_info(p, lines):
    title, artist = player_control.now_playing()
    out_name = title + ' - ' + artist
    if not lines:
        lines = get_texts(title, artist)

    lines = add_phonetics(lines, p)
    lines.insert(0, out_name)
    secs = [0] * len(lines)
    stamps = [''] * len(lines)
    num_chars = (max([len(i) for i in lines]) + 10)
    (width, height) = (max(1200, num_chars * space[0]), max(16 * space[1], 900))
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption('LyricStamp: ' + out_name)
    return out_name, lines, secs, stamps, screen


def print_info(screen, font, counter, lines, stamps, out_name):
    def text_to_screen(text, y, color):
        try:
            text = font.render(text, True, color)
            # everything starts at x=20
            screen.blit(text, (20, y))
        except Exception as e:
            raise e

    def screen_banner(*vargs):
        [text_to_screen(j, 10 + k * space[1], RED) for (k, j) in enumerate(vargs)]

    h = space[1]
    cursor = None
    if counter == -2:
        # TODO, streamline below
        welcome_msg = ["Let's get the lyrics. A few ways to do that:",
                       "",
                       "",
                       "- Press Right Arrow ➡ and we'll try fetch it from Genius.com.",
                       "- Press M and we'll try fetch from Musixmatch.com",
                       "- Press Enter and we'll get the lyrics from your clipboard.",
                       "- Drop a text file into this window and we'll read it."]
        screen_banner(*welcome_msg)
    elif counter == -1:
        welcome_msg = ["Type in the language code if wanna phonetics added.",
                       "Press Enter to skip.",
                       "",
                       "",
                       "Supported phonetics:",
                       "-Romaji for Japanese (type in 'J')",
                       "-Jyutping for Cantonese (type in 'Y')"]
        screen_banner(*welcome_msg)
    elif 0 <= counter <= len(lines) - 1:
        screen_banner("Press:",
                      "- Down Arrow ⬇ to go to the next line,",
                      "- Left arrow ⬅ to erase the stamp of the current line,",
                      "- Up Arrow ⬆ to go back to the stamp of the previous line",
                      "- Space bar to pause Apple Music")
        topleft = (20 + 3.5 * space[0], h * (counter - max(counter, 2) + 8.3))
        if counter <= len(lines) - 2 and lines[counter + 1].startswith('[tr]'):
            h = 2 * h
        cursor = pg.Rect(topleft, (3, h * .9))
        for i, l in enumerate(lines):
            if counter - 3 < i < max(counter, 2) + 9:
                yy = space[1] * (i - max(counter, 2) + 8)
                text_to_screen(str(i).zfill(3) + ': ' + stamps[i] + l, yy, BLACK)
    elif counter >= len(lines):
        screen_banner("Press Enter to end stamping and confirm that", out_name + " will be saved")
    return cursor


def main():
    pg.init()
    font = pg.font.Font('fonts/NotoSansCJK-Light.ttc', 30)
    # seems that CJK fonts have a pretty good coverage of western chars. Hard-code for now.
    # TODO: check e.g. Korean and Spanish
    # font = pg.font.Font('fonts/NotoSerifDisplay-Light.ttf', 30)
    # counter:
    # -2: Choose the source of text lyrics
    # -1: Choose if to add phonetics
    # ≥0: Adding stamps
    counter = -2
    out_name, lines, secs, stamps, screen = welcome()
    screen.fill(GRAY)
    pg.display.flip()

    running = True
    clock = pg.time.Clock()

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                running = False
            # source selection page
            if counter == -2:
                if e.type == pg.KEYDOWN and (e.key == pg.K_RETURN or e.key == pg.K_m):
                    # Initialize the scrap module and use the clipboard mode.
                    scrap.init()
                    scrap.set_mode(pg.SCRAP_CLIPBOARD)
                    for t in scrap.get_types():
                        r = scrap.get(t)
                        clipboard = (r.decode('UTF-8'))
                        if e.key == pg.K_RETURN:
                            lines = cleanup(clipboard)
                        else:
                            lines = musicsmatch(clipboard)
                    counter = -1
                if e.type == pg.DROPFILE:
                    in_name = e.file
                    with open(in_name) as f:
                        lines = [line.replace('\n', '') for line in f.readlines() if line.strip()]
                    counter = -1
                if e.type == pg.KEYDOWN and e.key == pg.K_RIGHT:
                    lines = None
                    counter = -1
            # phonetics page
            elif counter == -1:
                keys = [pg.K_j, pg.K_y, pg.K_RETURN]
                if e.type == pg.KEYDOWN and e.key in keys:
                    counter = 0
                    p = None
                    if e.key == pg.K_j:
                        p = 'J'
                    if e.key == pg.K_y:
                        p = 'Y'
                    out_name, lines, secs, stamps, screen = get_song_info(p, lines)
            elif counter >= 0:
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_RIGHT:
                        player_control.play_next()
                        counter = -2
                        pg.display.set_caption('LyricStamp')
                    if e.key == pg.K_SPACE and counter > 0:
                        player_control.play_pause()
                    if e.key == pg.K_DOWN:
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
                    if e.key == pg.K_UP or e.key == pg.K_LEFT:
                        counter -= 1
                        secs[counter] = 0
                        stamps[counter] = ''
                        if counter >= 0 and lines[counter].startswith('[tr]'):
                            counter -= 1
                            secs[counter] = 0
                            stamps[counter] = ''
                        if e.key == pg.K_UP:
                            player_control.set_player_position(secs[counter - 1])
                    if counter >= len(lines) and e.key == pg.K_RETURN:
                        save_lyrics(lines, stamps, out_name)
                        screen.fill(GRAY)
        screen.fill(GRAY)
        cursor = print_info(screen, font, counter, lines, stamps, out_name)
        if cursor and time.time() % 1 > 0.5:
            pg.draw.rect(screen, RED, cursor)
        pg.display.update()
        clock.tick(10)
    pg.quit()


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description=""".""")
    # parser.add_argument("-i", "--in_name",
    #                     help="local file to read static lyrics from; if none supplied, fetch from e.g. genius.com")
    # parser.add_argument("--lang",
    #                     help="if the song/book is in Chinese (use C), Japanese (J), or Korean (K).")
    # args = parser.parse_args()
    # in_name = args.in_name
    # lang = args.lang
    main()
