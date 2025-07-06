# LyricStamp

![LyricStamp Icon](lyricstamp.png)

Create timestamped lyrics files with while listening to music. Translate and/or add phonetics. Display the lyrics in karaoke style.


## Features

- [x] **Easy Line Stamping**: Simple click-to-stamp interface for timing lyrics while music plays
- [x] **Apple Music Integration**: Direct control of playback (play/pause, next track, position control)
- [x] **Karaoke-Style Display**: Immersive full-screen lyrics display with progress animations, inspired by LyricsX
- [x] **Multiple Input Sources**: Manual input, file upload, or clipboard
- [x] **AI Enhancements**: Optional romaji and translation support via AI
- [x] **Display Page**: View existing lyrics files with synchronized highlighting and auto-scroll
- [x] **AI Processing Page**: Real-time status monitoring for AI enhancements

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the web interface:
   ```bash
   python web_lyricstamp.py
   ```
4. Open your browser to `http://localhost:5734`

## Usage

### Setup Page (`/setup`)
1. Enter lyrics manually, upload a file, or paste from clipboard
2. The filename will auto-generate from the current song info
3. Click "Start Session" to begin timing

### Timing Page (`/timing`)
1. **Simple Stamping**: Just click "Next" to stamp each line's timing while music plays
2. **Music Control**: Use the Apple Music controls to manage playback
3. **Real-time Feedback**: See current line highlighted as you stamp it
4. **Navigation**: Use arrow keys or buttons to move between lines
5. **AI Enhancements**: Use the "🤖 AI Enhancements" button to add romaji or translations
6. **Save**: Click "Save File" when done, or it will prompt you at the last line

### Display Page (`/display`)
1. **Auto-load**: Automatically loads lyrics file matching current song
2. **Synchronized Display**: Highlights current line based on music position with LyricsX-style auto-scroll
3. **Music Control**: Full Apple Music integration for playback control
4. **File Info**: Shows song title, artist, and filename information

### Karaoke Page (`/karaoke`)
1. **Full-Screen Experience**: Immersive karaoke-style display with backdrop blur
2. **Progress Animation**: Text fills with gradient color as lyrics progress
3. **Two-Line Display**: Current line with progress + preview of next line
4. **Auto-Hide Controls**: Hover to reveal navigation controls
5. **Smooth Transitions**: Beautiful animations between lyric changes

### AI Processing Page (`/ai-processing`)
1. **Real-time Status**: Live monitoring of AI enhancement progress
2. **Progress Tracking**: Visual progress bar and percentage completion
3. **Processing Details**: Shows current line being processed and total lines
4. **Status Indicators**: Color-coded status (idle, processing, completed, error)
5. **Thinking Animation**: Visual feedback during AI processing

### Keyboard Shortcuts
- **Space**: Stop timing (when recording)
- **Left Arrow**: Previous line
- **Right Arrow**: Next line
- **Vim Mode**: Full Vim keybindings in lyrics textarea

## Output

Saves `.lrcx` files to `~/Music/LyricsX/` for use with [LyricsX](https://github.com/ddddxxx/LyricsX) or display directly in the app's built-in lyrics viewer.

## Motivation

LyricsX works wonders with Apple Music, especially for songs with no built-in synchronized lyrics. However, LyricsX relies on `*.lrcx` files from web services, and supply for songs in other languages or indie/obscure songs can be scarce. While plain-text lyrics are abundant online, time-stamping solutions are often overkill or a hassle.

This tool provides a simple, intuitive way to create timestamped lyrics files by playing along with music and clicking to mark each line's timing. Perfect for songs without built-in synchronized lyrics, making karaoke-style experiences accessible for any song. The built-in display brings the professional LyricsX experience to your browser.