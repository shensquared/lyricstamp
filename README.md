Play a song/audiobook in iTunes/Music on Mac, and use LyricStamp to: 
- [x] Fetch plain text lyrics/scripts from the Internet, or a local `.txt` file, or the clipboard
- [x] Add timestamps to plain text lyrics by playing a keyboard game alongside (think lip-sync)
- [ ] Add optional (context-based) phonetics automatically
  - [x] Romaji for Japanese
  - [x] Jyutping for Cantonese
  - [ ] Pinying for Mandarin
- [ ] Add optional (multi-language, i.e., one-to-many) translations

The end result is a rich `.lrcx` file, to be used in tandem with [LyricsX](https://github.com/ddddxxx/LyricsX) for synchronized lyrics/scripts display. (And why do we want synchronization in the first place? To 🎙️Karaoke🥳! And also to learn languages; e.g., to read along while listening and to precisely one-click jump to lines for repetition/reinforcement.)
![Demo](/demos/language.gif)

### Usage:
Run `python3 lyricstamp.py` to call out the 'game' interface. ~~(Currently the `lyrics.txt` is hard-coded to the song 'Je Lui Dirai' by 'Céline Dion'; automation incoming.)~~ Auto-fetching added. Need to update the text here.

- Press 'Down-Arrow' to tell Apple Music to start media playing and simultaneously reset LyricStamp's timer (so the sound/text are auto-aligned at '00:00')
- Keep pressing 'Down-Arrow' to go through the lines and to add stamp, one line at a time
- Press 'Up-Arrow' to go to the previous lines (e.g. to correct a 'jumped the gun')
- Press 'Enter' to end stamping, and save a `media_title - artist.lrcx` file to your LyricsX folder (where the `media_title` and `artist` are extracted from Music's now playing track properties via AppleScript). Enjoy!

[YouTube Demo](https://youtu.be/qZp7A0i0zl0) (Where the gif below was generated from)
![Demo](/demos/demo.gif) 

#### Tips:
- AirPlay-ing to e.g. Homepods creates a (systematic) delay that needs to be adjusted via adding a manual offset. Either avoid this by playing directly via the built-in speaker; or experiment to get your systematic delay value (to be embedded in the script globally)

### Motivation:
- LyricsX works wonders with Apple Music, especially for songs with no built-in synchronized lyrics. However, LyricsX relies on `*.lrcx` searched and fetched from a few Asia-based web services, and understandably, supply for songs in other languages or indie/obscure songs are scarce. And while plain-text lyrics are abundant online, time-stamping solutions I've found (e.g. NLP-based, iMovie timeline adjustment) are either an overkill or a hassle. 
- Audiobooks (particularly those targeted at language learning) can benefit greatly from having synchronized listening/reading too. These audiobooks often do come with an accompanying .pdf or .epub for the scripts, which can be easily turned into .txt, but time-stamping is still a hassle. (Fwiw, my limited research had led me to the so-called 'forced alignment', a sound-wave-analysis-based technique to align texts and audio. Not sure if/how well it can handle multi-language in a single file though.)