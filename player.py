# https://stackoverflow.com/questions/51775132/how-to-get-return-value-from-applescript-in-python
from subprocess import Popen, PIPE

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

    proc = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    title, error = proc.communicate(titlescript)
    proc = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    artist, error = proc.communicate(artistscript)
    file_name = title[:-1] + ' - ' + artist
    return file_name[:-1]
