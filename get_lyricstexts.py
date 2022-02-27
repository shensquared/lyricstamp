import lyricsgenius


def get_texts(title, artist):
    try:
        genius = lyricsgenius.Genius()
    except Exception as e:
        print('Genius API Token not found; check out https://pypi.org/project/lyricsgenius/ usage')
        raise e
    clean_title = title.split('(')[0]
    # TODO: if song returns None, should have an easy back-up. Was thinking of poping up a paste bin via pygame to
    #  dump the texts; seems a bit difficult. Alternatively, paste over in terminal.
    song = genius.search_song(clean_title, artist)
    if not song:
        return
    l = song.lyrics
    # TODO: clean up text format. Cleaned, but why were these so ugly added anyway?
    # remove the song title
    if l.startswith(song.title_with_featured):
        l = l.replace(song.title_with_featured, '')
    else:
        l = l.replace(song.title, '')
    # remove the prefix word 'Lyrics'
    l = l[7:]
    if l.endswith('Embed'):
        l = l.replace('Embed', '')

    lines = l.split('\n')
    lines = [line for line in lines if line.strip()]
    return lines
