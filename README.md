# lyricstamp

Play a keyboard game alongside a song/audiobook, to convert plain text `.txt` lyrics into time-stamped `.lrcx` . Use the time-stamped file in tandem with [LyricsX](https://github.com/ddddxxx/LyricsX), for synchronized lyrics display when you play the same media in the future.

### Motivation:
- LyricsX works wonders with Apple Music, especially for songs with no built-in synchronized lyrics. However, LyricsX relies on `*.lrcx` searched/fetched from a few Chinese/Asia-based web services, and understandably, such resources for songs in other languages, or indie songs, are somewhat lacking. And while plain-text lyrics are abundant online, time-stamping solutions I've found (e.g. NLP-based, iMovie timeline adjustment) are either a hassle or an overkill. 
- Audiobooks (particularly those targeted at language learning) can benefit greatly from synchronized listening/reading too. These audiobooks often do come with an accompanying .pdf or .epub for the scripts, which can be easily turned into .txt, but time-stamping is still a hassle. (Fwiw, my limited research had led me to the so-called 'forced alignment', a sound-wave-analysis-based technique to align texts and audio. Not sure if/how well it can handle multi-language in a single file.)

### Usage:
The timestamps insertion relies partially on you playing a keyboard `pygame` along the media (think lip sync).

Demo incoming.

```python3 lyricstamp.py```

Suppose you're playiing via Apple Music the song 'Je Lui Dirai' by 'Céline Dion'. You'll find a `Je Lui Dirai - Céline Dion.lrcx` file in your LyricsX folder. 