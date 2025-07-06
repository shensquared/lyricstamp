#!/usr/bin/env python3
"""
AI-powered phonetics and translation script for .lcrx files using Ollama.
This script reads a .lcrx file and uses Ollama to add phonetics and translations.
"""

import json
import os
import sys
import argparse
import requests
import time
from pathlib import Path
from typing import List, Tuple, Optional
import re


class OpenAIClient:
    """Client for interacting with OpenAI API."""
    
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
    
    def generate(self, model: str, prompt: str, system: str = None) -> str:
        """Generate text using OpenAI."""
        # Reload API key from environment in case it changed
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.session.headers.update({'Authorization': f'Bearer {api_key}'})
        url = "https://api.openai.com/v1/chat/completions"
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 200
        }
        
        try:
            response = self.session.post(url, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                raise e  # Re-raise to handle in calling function
            else:
                print(f"Error calling OpenAI: {e}")
                return ""
        except requests.exceptions.RequestException as e:
            print(f"Error calling OpenAI: {e}")
            return ""


class OllamaClient:
    """Client for interacting with Ollama API."""
    def __init__(self):
        self.ollama_url = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def generate(self, model: str, prompt: str, system: str = None) -> str:
        url = f"{self.ollama_url}/api/generate"
        
        # Combine system and user prompt for generate endpoint
        full_prompt = ""
        if system:
            full_prompt += f"{system}\n\n"
        full_prompt += prompt
        
        data = {
            "model": model,
            "prompt": full_prompt,
            "stream": False
        }
        
        try:
            response = self.session.post(url, json=data, timeout=120)  # Increased timeout
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama: {e}")
            return ""


def parse_lrcx_file(file_path: str) -> Tuple[List[str], List[str]]:
    """Parse a .lrcx file and return timestamps and lyrics."""
    timestamps = []
    lyrics = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Find the timestamp at the beginning of the line
                timestamp_end = line.find(']')
                if timestamp_end != -1 and line.startswith('['):
                    timestamp = line[:timestamp_end + 1]
                    lyric = line[timestamp_end + 1:].strip()
                    timestamps.append(timestamp)
                    lyrics.append(lyric)
                else:
                    # No timestamp, treat as lyric only
                    timestamps.append("")
                    lyrics.append(line)
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    return timestamps, lyrics


def detect_language(text: str) -> str:
    """Detect the language of the text using OpenAI."""
    client = OpenAIClient()
    
    system_prompt = """You are a language detection expert. Given a text, return only the ISO 639-1 language code (e.g., 'en', 'ja', 'zh', 'ko', 'es', 'fr', etc.). If you're unsure, return 'en'."""
    
    prompt = f"Detect the language of this text and return only the ISO 639-1 language code:\n\n{text[:500]}"
    
    result = client.generate("gpt-3.5-turbo", prompt, system_prompt)
    return result.lower().strip()


def add_ai_phonetics_and_translation(lyrics: List[str], target_language: str = "en", model: str = "gpt-3.5-turbo", include_kanji: bool = False, ollama_url: str = None, use_ollama: bool = False) -> List[str]:
    """Add English translations and romaji versions for Japanese text using AI."""
    client = OllamaClient() if use_ollama else OpenAIClient()
    
    # Use appropriate model for each backend
    if use_ollama:
        ollama_model = "phi3.5:3.8b"  # Default Ollama model
    else:
        ollama_model = model  # Use the provided model for OpenAI
    
    # Use the include_kanji flag to determine if we should add kanji
    should_include_kanji = include_kanji
    print(f"Kanji inclusion: {should_include_kanji}")
    print(f"Using model: {ollama_model if use_ollama else model}")
    
    system_prompt = """You are a Japanese text processing expert. For each line of Japanese lyrics, provide the romaji (Latin alphabet transcription).

For romaji conversion:
- Convert all Japanese text to romaji (Latin alphabet)
- Examples: "こんにちは" → "konnichiwa", "ありがとう" → "arigatou", "さようなら" → "sayounara"
- For non-Japanese text, return the text as-is
- For mixed text, convert only the Japanese parts

IMPORTANT: Respond ONLY with valid JSON. Do not include any thinking process, explanations, or other text.

Format your response as JSON with this structure:
{
    "romaji": "romaji transcription of the Japanese text"
}

Only respond with valid JSON, no other text."""

    enhanced_lyrics = []
    
    for i, lyric in enumerate(lyrics):
        if not lyric or lyric.startswith('[tr]') or lyric.startswith('[tl]'):
            enhanced_lyrics.append(lyric)
            continue
        
        print(f"Processing line {i+1}/{len(lyrics)}: {lyric[:50]}...")
        
        prompt = f"Provide romaji transcription for this Japanese text:\n{lyric}"
        
        try:
            result = client.generate(ollama_model, prompt, system_prompt)
            
            # Try to parse JSON response
            try:
                # Try to extract JSON from the response (in case there's extra text)
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    parsed = json.loads(json_str)
                else:
                    parsed = json.loads(result)
                
                romaji = parsed.get("romaji", "")
                
                # Debug output
                print(f"  AI Response: {result}")
                print(f"  Parsed romaji: '{romaji}'")
                
                # Add original lyric
                enhanced_lyrics.append(lyric)
                
                # Only add romaji line when kanji is requested, skip translations
                romaji_line = romaji if romaji else lyric
                if should_include_kanji:
                    enhanced_lyrics.append(f"[tr]{romaji_line}")
                    
            except json.JSONDecodeError:
                print(f"Warning: Could not parse AI response for line {i+1}, skipping enhancement")
                print(f"  Raw response: {result}")
                enhanced_lyrics.append(lyric)
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"Rate limited, waiting 5 seconds...")
                time.sleep(5)
                # Try one more time
                try:
                    result = client.generate(ollama_model, prompt, system_prompt)
                    try:
                        # Try to extract JSON from the response (in case there's extra text)
                        json_match = re.search(r'\{.*\}', result, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(0)
                            parsed = json.loads(json_str)
                        else:
                            parsed = json.loads(result)
                        
                        romaji = parsed.get("romaji", "")
                        enhanced_lyrics.append(lyric)
                        if should_include_kanji:
                            enhanced_lyrics.append(f"[tr]{romaji}")
                    except json.JSONDecodeError:
                        print(f"Warning: Could not parse AI response for line {i+1}, skipping enhancement")
                        enhanced_lyrics.append(lyric)
                except Exception as retry_e:
                    print(f"Error on retry for line {i+1}: {retry_e}")
                    enhanced_lyrics.append(lyric)
            else:
                print(f"Error processing line {i+1}: {e}")
                enhanced_lyrics.append(lyric)
        except Exception as e:
            print(f"Error processing line {i+1}: {e}")
            enhanced_lyrics.append(lyric)
        
        # Add delay to avoid rate limiting
        if i < len(lyrics) - 1:
            time.sleep(2)
    
    return enhanced_lyrics


def save_enhanced_lrcx(timestamps: List[str], enhanced_lyrics: List[str], output_path: str):
    """Save the enhanced lyrics to a new .lrcx file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            timestamp_index = 0
            for lyric in enhanced_lyrics:
                # Use the corresponding timestamp for original lyrics
                if not lyric.startswith('[tr]') and not lyric.startswith('[tl]'):
                    if timestamp_index < len(timestamps):
                        timestamp = timestamps[timestamp_index]
                        timestamp_index += 1
                    else:
                        timestamp = ""
                else:
                    # For translation and kanji lines, use the same timestamp as the original line
                    if timestamp_index > 0:
                        timestamp = timestamps[timestamp_index - 1]
                    else:
                        timestamp = ""
                
                if timestamp:
                    f.write(f"{timestamp}{lyric}\n")
                else:
                    f.write(f"{lyric}\n")
        print(f"Enhanced lyrics saved to: {output_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Add AI-powered romaji and translation to .lrcx files using OpenAI or Ollama"
    )
    parser.add_argument(
        "input_file",
        help="Path to the input .lrcx file (can be relative to $HOME/Music/LyricsX)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: input_file_enhanced.lrcx in $HOME/Music/LyricsX)"
    )
    parser.add_argument(
        "-t", "--target-language",
        default="en",
        help="Target language for translation (default: en)"
    )
    parser.add_argument(
        "-m", "--model",
        default="gpt-3.5-turbo",
        help="OpenAI model to use (default: gpt-3.5-turbo)"
    )
    parser.add_argument(
        "--ollama-url",
        help="Legacy Ollama URL option (not used with OpenAI)"
    )
    parser.add_argument(
        "--detect-language",
        action="store_true",
        help="Automatically detect the source language"
    )
    parser.add_argument(
        "--kanji",
        action="store_true",
        help="Add kanji versions for Japanese text"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all .lrcx files in $HOME/Music/LyricsX"
    )
    parser.add_argument(
        "--lyricsx-dir",
        default="~/Music/LyricsX",
        help="LyricsX directory (default: $HOME/Music/LyricsX)"
    )
    parser.add_argument(
        "--use-ollama",
        action="store_true",
        help="Use Ollama backend instead of OpenAI"
    )
    
    args = parser.parse_args()
    
    # Expand LyricsX directory path
    lyricsx_dir = os.path.expanduser(args.lyricsx_dir)
    
    # List files if requested
    if args.list:
        if not os.path.exists(lyricsx_dir):
            print(f"LyricsX directory not found: {lyricsx_dir}")
            sys.exit(1)
        
        lrcx_files = [f for f in os.listdir(lyricsx_dir) if f.endswith('.lrcx')]
        if not lrcx_files:
            print(f"No .lrcx files found in {lyricsx_dir}")
        else:
            print(f"Found {len(lrcx_files)} .lrcx files in {lyricsx_dir}:")
            for i, file in enumerate(sorted(lrcx_files), 1):
                print(f"{i:2d}. {file}")
        return
    
    # Handle input file path
    input_file = args.input_file
    if not os.path.isabs(input_file):
        # If not absolute path, try relative to LyricsX directory
        lyricsx_input = os.path.join(lyricsx_dir, input_file)
        if os.path.exists(lyricsx_input):
            input_file = lyricsx_input
        elif not os.path.exists(input_file):
            # Try with .lrcx extension if not provided
            if not input_file.endswith('.lrcx'):
                lyricsx_input = os.path.join(lyricsx_dir, input_file + '.lrcx')
                if os.path.exists(lyricsx_input):
                    input_file = lyricsx_input
    
    # Validate input file
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        print(f"Tried paths:")
        print(f"  - {input_file}")
        if not os.path.isabs(args.input_file):
            print(f"  - {os.path.join(lyricsx_dir, args.input_file)}")
            if not args.input_file.endswith('.lrcx'):
                print(f"  - {os.path.join(lyricsx_dir, args.input_file + '.lrcx')}")
        sys.exit(1)
    
    if not input_file.endswith('.lrcx'):
        print("Warning: Input file doesn't have .lrcx extension")
    
    # Set output file
    if args.output:
        output_file = args.output
        if not os.path.isabs(output_file):
            output_file = os.path.join(lyricsx_dir, output_file)
    else:
        input_path = Path(input_file)
        output_file = os.path.join(lyricsx_dir, f"{input_path.stem}_enhanced.lrcx")
    
    print(f"Processing: {input_file}")
    print(f"Output: {output_file}")
    print(f"Target language: {args.target_language}")
    print(f"Model: {args.model}")
    
    # Parse the input file
    timestamps, lyrics = parse_lrcx_file(input_file)
    print(f"Found {len(lyrics)} lyrics lines")
    
    # Add AI enhancements (language detection is done automatically)
    enhanced_lyrics = add_ai_phonetics_and_translation(
        lyrics, 
        args.target_language, 
        args.model,
        args.kanji,
        args.ollama_url,
        args.use_ollama
    )
    
    # Save the enhanced file
    save_enhanced_lrcx(timestamps, enhanced_lyrics, output_file)
    
    print("Processing complete!")


if __name__ == "__main__":
    main() 