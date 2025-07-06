# LyricStamp Web Interface

A web-based tool for adding timestamps to lyrics synchronized with Apple Music playback on Mac.

![LyricStamp Icon](lyricstamp.png)

## Features

- [x] **Web Interface**: Modern, responsive web UI for easy lyric timing
- [x] **Apple Music Integration**: Direct control of playback (play/pause, next track, position control)
- [x] **Multiple Input Sources**: Manual input, file upload, or clipboard
- [x] **Real-time Timing**: Add timestamps while music plays
- [x] **Auto-filename Generation**: Creates filenames from current song info
- [x] **AI Enhancements**: Optional romaji and translation support via AI
- [x] **Vim Keybindings**: Full Vim mode support in lyrics textarea
- [x] **Separate Workflow**: Setup page for lyrics input, timing page for timestamping
- [x] **Display Page**: View existing lyrics files with synchronized highlighting
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
4. Open your browser to `http://localhost:5000`

## Usage

### Setup Page (`/setup`)
1. Enter lyrics manually, upload a file, or paste from clipboard
2. The filename will auto-generate from the current song info
3. Click "Start Session" to begin timing

### Timing Page (`/timing`)
1. **Music Control**: Use the Apple Music controls to manage playback
2. **Timing**: Click "Start Timing" and press "Next" to add timestamps
3. **Navigation**: Use arrow keys or buttons to move between lines
4. **AI Enhancements**: Use the "🤖 AI Enhancements" button to add romaji or translations
5. **Save**: Click "Save File" when done, or it will prompt you at the last line

### Display Page (`/display`)
1. **Auto-load**: Automatically loads lyrics file matching current song
2. **Synchronized Display**: Highlights current line based on music position
3. **Music Control**: Full Apple Music integration for playback control
4. **File Info**: Shows song title, artist, and filename information

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

Saves `.lrcx` files to `~/Music/LyricsX/` for use with [LyricsX](https://github.com/ddddxxx/LyricsX).

## Motivation

LyricsX works wonders with Apple Music, especially for songs with no built-in synchronized lyrics. However, LyricsX relies on `*.lrcx` files from web services, and supply for songs in other languages or indie/obscure songs can be scarce. While plain-text lyrics are abundant online, time-stamping solutions are often overkill or a hassle.

This web interface provides a simple, intuitive way to add timestamps to any lyrics while listening to music, making synchronized lyrics accessible for any song.