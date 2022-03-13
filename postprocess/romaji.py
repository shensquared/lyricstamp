from player_control import now_playing
import os
import cutlet

title, artist = now_playing()
name = title + ' - ' + artist + '.lrcx'

home = os.path.expanduser("~")
path = home + '/Music/LyricsX'
with open(os.path.join(path, name)) as f:
    lines = f.readlines()

def backup(lines):
    home = os.path.expanduser("~")
    path = home + '/Music/LyricsX/Backup'
    with open(os.path.join(path, name), "w") as f:
        [f.write(i + '\n') for i in lines]

backup(lines)

katsu = cutlet.Cutlet()
katsu.use_foreign_spelling = False

new = []
for i in lines:
    if i.startswith('[0'):
        stamp = i[:11]
        words = i[11:]
        # print(words)
        # temp = ''.join(i.split(']')[1:])
        if not words.startswith('[t') and len(words)>1:
            # print(words)
            new.append(i)
            new.append(stamp + '[tr:il]' + katsu.romaji(words))
        elif words.startswith('[tr:zh-Hans]'):
            j = new.pop() + ' ' + words[12:]
            new.append(j)

with open(os.path.join(path, name), 'w') as f:
    [f.write(i +'\n') for i in new]
