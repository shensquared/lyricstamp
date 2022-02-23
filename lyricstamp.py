import pygame
import time
import os
import sys
import player_control


def stamp_internal(pos):
    m = str(int((pos) / 60)).rjust(2, '0')
    s = str(round(pos % 60, 3)).rjust(2, '0')
    return "[" + m + ":" + s + "]"


def stamp(begin, end, all_pauses):
    t = end - begin - all_pauses
    return stamp_internal(t)


def save_lyrics(lines, out_name):
    home = os.path.expanduser("~")
    path = home + '/Music/LyricsX'
    out_name += '.lrcx'
    with open(os.path.join(path, out_name), "w") as f:
        [f.write(i) for i in lines]
    print('Saved ' + out_name + ' in ' + path)


# Modified from https://gist.github.com/seankmartin/f660eff4787b586f94d5f678932bcd27
# TODO: Non-western chars not displaying
def text_to_screen(screen, text, x, y, font, color=(0, 0, 0)):
    try:
        text = str(text)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))
    except Exception as e:
        print('Font Error, saw it coming')
        raise e


def screen_banner(screen, text1, text2, font, char_size):
    color = (255, 000, 000)
    text_to_screen(screen, text1, 20, 10, font, color=color)
    text_to_screen(screen, text2, 20, 10 + char_size[1], font, color=color)


def print_info(screen, lines, counter, font, char_size, out_name=''):
    for i, l in enumerate(lines):
        if counter - 3 < i < max(counter, 2) + 9:
            text_to_screen(screen, str(i) + ': ' + l, 20,
                           char_size[1] * (i - max(counter, 2) + 5), font)
    if counter == 0:
        screen_banner(screen, "Press 'Down-Arrow'",
                      "to start the media playing and reset the timer", font, char_size)
    elif counter >= len(lines):
        screen_banner(screen, "Press Enter to end stamping and confirm that", out_name + " will be saved", font,
                      char_size)
    else:
        screen_banner(screen, "Press 'Down-Arrow' to go to the next line",
                      "'Up-Arrow' to go back to the previous line.", font, char_size)

# TODO: Surely there's a better way to handle even mixed languages...
def main(in_name="lyrics.txt", mode=1, font_type=['songti', 'hiraginosansgb', 'Palatino']):
    with open(in_name) as f:
        lines = [line for line in f.readlines() if line.strip()]
    title, artist = player_control.now_playing()
    out_name = title + ' - ' + artist
    lines.insert(0, out_name + "\n")
    counter = 0
    # Setup interface
    background_colour = (255, 255, 255)
    pygame.init()
    font = pygame.font.SysFont(font_type, 30)
    char_size = font.size('a')
    (width, height) = (
        (max([len(i) for i in lines]) + 10) * char_size[0], 16 * char_size[1])

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('LyricStamp: ' + out_name)
    screen.fill(background_colour)
    pygame.display.flip()

    running = True
    clock = pygame.time.Clock()
    all_pauses = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and counter > 0:
                    player_control.play_pause()
                    if is_playing:
                        # start of a pause
                        pause_start = time.time()
                    else:
                        # end of a pause
                        pause_end = time.time()
                        all_pauses += (pause_end - pause_start)
                    is_playing = 1 - is_playing
                if event.key == pygame.K_DOWN:
                    is_playing = True
                    print("Caret is at line: " + str(counter))
                    if counter == 0:
                        player_control.play()
                        lines[counter] = "[00:00.000]" + ' ' + lines[counter]
                        begin = time.time()
                    elif counter <= len(lines) - 1:
                        # insert new stamp into line
                        now = time.time()
                        if mode == 1:
                            # use iTunes/Music's internal player's position
                            pos = player_control.player_position()
                            s = stamp_internal(pos)
                        else:
                            # use pygame's timer.
                            s = stamp(begin, now, all_pauses)
                        lines[counter] = s + ' ' + lines[counter]
                    counter += 1
                if event.key == pygame.K_UP:
                    counter -= 1
                    try:
                        # remove the old/wrong timestamp
                        lines[counter] = " ".join(lines[counter].split(']')[1:])[1:]
                    except:
                        pass
                if event.key == pygame.K_RETURN and counter >= len(lines):
                    save_lyrics(lines, out_name)
                    running = False
                    pygame.quit()
                    break
                if event.key == pygame.K_ESCAPE:
                    return
            screen.fill(background_colour)
            print_info(screen, lines, counter, font, char_size, out_name)
            pygame.display.update()
            clock.tick(40)


if __name__ == "__main__":
    # in_name = sys.argv[0]
    main()
