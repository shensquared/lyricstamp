import lyricsgenius

def get_texts(title, artist):
    try:
        genius = lyricsgenius.Genius()
    except Exception as e:
        print('Genius API Token not found; check out https://pypi.org/project/lyricsgenius/ usage')
        raise e
    clean_title = title.split('(')[0]
    song = genius.search_song(clean_title, artist)
    l = song.lyrics
    # TODO: clean up text format
    lines = l.split('\n')
    lines = [line for line in lines if line.strip()]
    return lines