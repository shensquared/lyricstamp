#!/usr/bin/env python3
"""
Web-based LyricStamp Interface
A web version of the pygame-based lyric timing interface
"""

import os
import sys
import json
import time
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import subprocess
import threading
import player_control

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lyricstamp-web-secret-key'

# Global variables to store current session data
current_session = {
    'lines': [],
    'timestamps': [],
    'current_line': 0,
    'is_recording': False,
    'start_time': 0,
    'output_filename': '',
    'audio_file': None
}

def get_lyricsx_dir():
    """Get the LyricsX directory path."""
    return os.path.expanduser("~/Music/LyricsX")

def list_audio_files():
    """List available audio files in common directories."""
    audio_extensions = {'.mp3', '.m4a', '.wav', '.flac', '.aac'}
    audio_files = []
    
    # Common audio directories
    search_dirs = [
        os.path.expanduser("~/Music"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop")
    ]
    
    for search_dir in search_dirs:
        if os.path.exists(search_dir):
            for root, dirs, files in os.walk(search_dir):
                for file in files:
                    if Path(file).suffix.lower() in audio_extensions:
                        rel_path = os.path.relpath(os.path.join(root, file), search_dir)
                        audio_files.append({
                            'path': os.path.join(root, file),
                            'name': file,
                            'display': rel_path
                        })
    
    return audio_files[:50]  # Limit to first 50 files

def get_song_info_from_clipboard():
    """Get song info from clipboard (placeholder for now)."""
    try:
        import pyperclip
        clipboard_text = pyperclip.paste()
        if clipboard_text and len(clipboard_text.strip()) > 0:
            return clipboard_text.strip()
    except ImportError:
        pass
    return ""

def create_safe_filename(title, artist):
    """Create a safe filename from song title and artist."""
    import re
    
    # Remove or replace unsafe characters
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    safe_artist = re.sub(r'[<>:"/\\|?*]', '', artist)
    
    # Replace spaces with underscores and limit length
    safe_title = safe_title.replace(' ', '_')[:50]
    safe_artist = safe_artist.replace(' ', '_')[:50]
    
    # Create filename
    filename = f"{safe_title}_-_{safe_artist}.lrcx"
    
    return filename

def save_lyrics(lines, timestamps, filename):
    """Save lyrics to .lrcx file."""
    try:
        output_path = os.path.join(get_lyricsx_dir(), filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, line in enumerate(lines):
                if i < len(timestamps) and timestamps[i]:
                    f.write(f"{timestamps[i]}{line}\n")
                else:
                    f.write(f"{line}\n")
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def process_ai_enhancements(lines, add_romaji=False, add_translation=False, use_ollama=False):
    """Process AI enhancements using the existing ai_phonetics script."""
    try:
        from ai_postprocess import add_ai_phonetics_and_translation
        
        # Extract lyrics without timestamps for AI processing
        lyrics_only = [line for line in lines if not line.startswith('[') and line.strip()]
        
        enhanced_lyrics = lyrics_only
        
        if add_romaji or add_translation:
            enhanced_lyrics = add_ai_phonetics_and_translation(
                lyrics_only,
                target_language="en",
                model="phi3.5:3.8b" if use_ollama else "gpt-3.5-turbo",
                include_kanji=add_romaji,
                use_ollama=use_ollama
            )
        
        return enhanced_lyrics
    except Exception as e:
        print(f"AI processing failed: {e}")
        return lines

@app.route('/')
def index():
    """Main page - redirect to setup."""
    return render_template('setup.html')

@app.route('/setup')
def setup():
    """Setup page for lyrics input."""
    return render_template('setup.html')

@app.route('/timing')
def timing():
    """Timing interface page."""
    return render_template('timing.html')

@app.route('/api/start_session', methods=['POST'])
def start_session():
    """Start a new timing session."""
    data = request.get_json()
    
    # Get lyrics from various sources
    lyrics = []
    if data.get('source') == 'clipboard':
        clipboard_text = get_song_info_from_clipboard()
        if clipboard_text:
            lyrics = [line.strip() for line in clipboard_text.split('\n') if line.strip()]
    elif data.get('source') == 'manual':
        lyrics = [line.strip() for line in data.get('lyrics', '').split('\n') if line.strip()]
    elif data.get('source') == 'file':
        # Handle file upload
        pass
    
    if not lyrics:
        return jsonify({'error': 'No lyrics provided'}), 400
    
    # Initialize session
    current_session['lines'] = lyrics
    current_session['timestamps'] = [''] * len(lyrics)
    current_session['current_line'] = 0
    current_session['is_recording'] = False
    current_session['output_filename'] = data.get('filename', 'untitled.lrcx')
    
    return jsonify({
        'success': True,
        'total_lines': len(lyrics),
        'current_line': 0,
        'lines': lyrics
    })

@app.route('/api/start_timing', methods=['POST'])
def start_timing():
    """Start timing the current line."""
    if not current_session['lines']:
        return jsonify({'error': 'No active session'}), 400
    
    current_session['is_recording'] = True
    current_session['start_time'] = time.time()
    
    return jsonify({
        'success': True,
        'current_line': current_session['current_line'],
        'line_text': current_session['lines'][current_session['current_line']]
    })

@app.route('/api/stop_timing', methods=['POST'])
def stop_timing():
    """Stop timing and save timestamp."""
    if not current_session['is_recording']:
        return jsonify({'error': 'Not currently timing'}), 400
    
    elapsed_time = time.time() - current_session['start_time']
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time % 1) * 1000)
    
    timestamp = f"[{minutes}:{seconds:02d}.{milliseconds:03d}]"
    current_session['timestamps'][current_session['current_line']] = timestamp
    current_session['is_recording'] = False
    
    return jsonify({
        'success': True,
        'timestamp': timestamp,
        'current_line': current_session['current_line']
    })

@app.route('/api/next_line', methods=['POST'])
def next_line():
    """Move to the next line and add timestamp."""
    if current_session['current_line'] < len(current_session['lines']) - 1:
        # Add timestamp for current line before moving to next
        if current_session['current_line'] == 0:
            # First line gets 00:00.000 timestamp
            timestamp = "[00:00.000]"
        else:
            # Get current player position for timestamp
            try:
                pos = player_control.player_position()
                minutes = int(pos // 60)
                seconds = int(pos % 60)
                milliseconds = int((pos % 1) * 1000)
                timestamp = f"[{minutes}:{seconds:02d}.{milliseconds:03d}]"
            except Exception as e:
                # Fallback to current time if player position fails
                elapsed_time = time.time() - current_session.get('start_time', time.time())
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                milliseconds = int((elapsed_time % 1) * 1000)
                timestamp = f"[{minutes}:{seconds:02d}.{milliseconds:03d}]"
        
        # Save timestamp for current line
        current_session['timestamps'][current_session['current_line']] = timestamp
        
        # Move to next line
        current_session['current_line'] += 1
        
        return jsonify({
            'success': True,
            'current_line': current_session['current_line'],
            'line_text': current_session['lines'][current_session['current_line']],
            'timestamp': timestamp,
            'is_last': current_session['current_line'] == len(current_session['lines']) - 1
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Already at last line',
            'current_line': current_session['current_line'],
            'total_lines': len(current_session['lines']),
            'is_last': True
        })

@app.route('/api/prev_line', methods=['POST'])
def prev_line():
    """Move to the previous line."""
    if current_session['current_line'] > 0:
        current_session['current_line'] -= 1
        return jsonify({
            'success': True,
            'current_line': current_session['current_line'],
            'line_text': current_session['lines'][current_session['current_line']]
        })
    else:
        return jsonify({'error': 'Already at first line'}), 400

@app.route('/api/save', methods=['POST'])
def save_file():
    """Save the current session to file."""
    data = request.get_json()
    
    # Get filename from request or auto-generate
    provided_filename = data.get('filename')
    
    if provided_filename and provided_filename.strip():
        # Use provided filename
        filename = provided_filename
        if not filename.endswith('.lrcx'):
            filename += '.lrcx'
    else:
        # Auto-generate filename from current song
        try:
            title, artist = player_control.now_playing()
            filename = create_safe_filename(title, artist)
        except Exception as e:
            # Fallback to default
            filename = current_session.get('output_filename', 'untitled.lrcx')
    
    if save_lyrics(current_session['lines'], current_session['timestamps'], filename):
        return jsonify({
            'success': True, 
            'filename': filename,
            'full_path': os.path.join(get_lyricsx_dir(), filename)
        })
    else:
        return jsonify({'error': 'Failed to save file'}), 500

@app.route('/api/ai_menu', methods=['POST'])
def ai_menu():
    """Show AI processing options."""
    data = request.get_json()
    add_romaji = data.get('add_romaji', False)
    add_translation = data.get('add_translation', False)
    use_ollama = data.get('use_ollama', False)
    
    if add_romaji or add_translation:
        # Create backup first
        backup_filename = current_session['output_filename'].replace('.lrcx', '.backup.lrcx')
        save_lyrics(current_session['lines'], current_session['timestamps'], backup_filename)
        
        # Process AI enhancements
        enhanced_lines = process_ai_enhancements(
            current_session['lines'], 
            add_romaji=add_romaji, 
            add_translation=add_translation, 
            use_ollama=use_ollama
        )
        
        # Update session with enhanced lines
        current_session['lines'] = enhanced_lines
        current_session['timestamps'] = [''] * len(enhanced_lines)
        
        return jsonify({
            'success': True,
            'enhanced_lines': enhanced_lines,
            'total_lines': len(enhanced_lines)
        })
    
    return jsonify({'success': True})

@app.route('/api/get_status')
def get_status():
    """Get current session status."""
    if not current_session['lines']:
        return jsonify({'error': 'No active session'}), 400
    
    return jsonify({
        'current_line': current_session['current_line'],
        'total_lines': len(current_session['lines']),
        'is_recording': current_session['is_recording'],
        'current_line_text': current_session['lines'][current_session['current_line']],
        'timestamps': current_session['timestamps']
    })

@app.route('/api/get_session_lines')
def get_session_lines():
    """Get the lyrics lines and timestamps from the current session."""
    if not current_session['lines']:
        return jsonify({'error': 'No active session'}), 400
    
    return jsonify({
        'success': True,
        'lines': current_session['lines'],
        'timestamps': current_session['timestamps']
    })

# Apple Music Control Endpoints
@app.route('/api/music/now_playing')
def get_now_playing():
    """Get currently playing track info."""
    try:
        title, artist = player_control.now_playing()
        return jsonify({
            'success': True,
            'title': title,
            'artist': artist
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/music/play_pause', methods=['POST'])
def toggle_play_pause():
    """Toggle play/pause."""
    try:
        player_control.play_pause()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/music/play', methods=['POST'])
def play_music():
    """Start playing from beginning."""
    try:
        player_control.play()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/music/next', methods=['POST'])
def next_track():
    """Play next track."""
    try:
        player_control.play_next()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/music/position')
def get_position():
    """Get current player position."""
    try:
        position = player_control.player_position()
        return jsonify({
            'success': True,
            'position': position
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/music/position', methods=['POST'])
def set_position():
    """Set player position."""
    try:
        data = request.get_json()
        position = data.get('position', 0)
        player_control.set_player_position(position)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/music/duration')
def get_duration():
    """Get current track duration."""
    try:
        duration = player_control.get_duration()
        return jsonify({
            'success': True,
            'duration': duration
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("Starting LyricStamp Web Interface...")
    print("Open your browser to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 