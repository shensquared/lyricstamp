# https://stackoverflow.com/questions/51775132/how-to-get-return-value-from-applescript-in-python
from subprocess import Popen, PIPE


def execute(script):
    proc = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE,
                 stderr=PIPE, universal_newlines=True)
    result, error = proc.communicate(script)
    return result


def now_playing():
    titlescript = '''
          tell application "Music"
          get name of current track
          end tell
      '''

    artistscript = '''
          tell application "Music"
          get artist of current track
          end tell
      '''
    title = execute(titlescript)
    artist = execute(artistscript)
    return title[:-1], artist[:-1]


def play():
    # TODO: hacky way to start play right from the beginning. Seems that Apple Music assigns
    # a unique `track id` and also a `persistent ID` for each song.
    # But couldn't use these as identifiers to play. Need investigate
    # further.
    playscript = '''
        tell application "Music"
        back track
        play
        end tell
    '''
    execute(playscript)


def play_pause():
    script = '''
        tell application "Music"
        playpause
        end tell
    '''
    execute(script)


def player_position():
    script = '''
        tell application "Music"
        get player position
        end tell
    '''
    return float(execute(script))

def set_player_position(pos):
    s = '''
        tell application "Music"
            set player position to %s
        end tell
    ''' %pos
    return execute(s)

def play_next():
    s = '''
        tell application "Music"
            next track
            play
        end tell
    '''
    return execute(s)

def get_duration():
    script = '''
        tell application "Music"
            get duration of current track
        end tell
    '''
    return float(execute(script))