import lyricsgenius


def get_texts(title, artist):
    try:
        genius = lyricsgenius.Genius()
    except Exception as e:
        print('Genius API Token not found; check out https://pypi.org/project/lyricsgenius/ usage')
        raise e
    clean_title = title.split('(')[0]
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
    return cleanup(l)


def musicsmatch(url):
    # https://dev.to/starry69/how-to-scrape-musixmatch-to-get-lyrics-of-your-favourite-songs-in-python-3ocg
    import requests
    from bs4 import BeautifulSoup

    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    def get_soup(url: str) -> BeautifulSoup:
        """
        Utility function which takes a url and returns a Soup object.
        """
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    # build bs4 soup object.
    soup = get_soup(url)
    # find the lyrics data.
    cols = soup.findAll(class_="lyrics__content__ok", text=True)
    if cols:
        lyrics = "\n".join(x.text for x in cols)
    elif data := soup.find(class_="lyrics__content__warning", text=True):
        lyrics = data.get_text()
    # finally print the lyrics.
    return cleanup(lyrics)


def cleanup(l):
    lines = l.split('\n')
    lines = [line for line in lines if line.strip()]
    return lines
