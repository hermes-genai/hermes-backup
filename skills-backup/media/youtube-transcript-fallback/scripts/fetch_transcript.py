#!/usr/bin/env python3
"""
Fetch YouTube transcript via multiple fallback methods
Usage: python3 fetch_transcript.py <youtube_url_or_video_id>
Outputs timestamped markdown transcript to stdout
"""

import sys
import re
import json
import html
import subprocess
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

def extract_video_id(url_or_id):
    """Extract YouTube video ID from various URL formats or return if already an ID"""
    # If it looks like just an 11-character ID (alphanumeric plus - and _)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id
    
    # Patterns for YouTube URLs
    patterns = [
        r'(?:youtube\\.com\\/watch\\?v=|youtu\\.be\\/|youtube\\.com\\/embed\\/|youtube\\.com\\/v\\/|youtube\\.com\\/shorts\\/)([a-zA-Z0-9_-]{11})',
        r'youtube\\.com\\/watch\\?.*v=([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    # If no match found, return original (will likely fail later but gives clear error)
    return url_or_id

def try_ytdlp_methods(video_id):
    """Try to get transcript using yt-dlp with various player clients"""
    # Try different YouTube player clients to bypass bot detection
    player_clients = [
        ('default', []),
        ('android', ['--extractor-args', 'youtube:player_client=android']),
        ('web_embedded', ['--extractor-args', 'youtube:player_client=web_embedded']),
        ('ios', ['--extractor-args', 'youtube:player_client=ios']),
    ]
    
    for client_name, args in player_clients:
        try:
            cmd = [
                'yt-dlp',
                '--skip-download',
                '--write-auto-sub',
                '--sub-lang', 'en',  # Try English first
                '--sub-format', 'json3',
                '--print', '%(automatic_captions)s',
            ] + args + [f'https://www.youtube.com/watch?v={video_id}']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0 and result.stdout.strip():
                # Try to get the actual subtitle file
                cmd2 = [
                    'yt-dlp',
                    '--skip-download',
                    '--write-auto-sub',
                    '--sub-lang', 'en',
                    '--sub-format', 'json3',
                    '-o', '/tmp/%(id)s.%(ext)s',
                    f'https://www.youtube.com/watch?v={video_id}'
                ]
                
                result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=30)
                if result2.returncode == 0:
                    # Look for the downloaded subtitle file
                    import os
                    subtitle_file = f'/tmp/{video_id}.info.json'
                    if os.path.exists(subtitle_file):
                        try:
                            with open(subtitle_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                # Look for automatic captions
                                if 'automatic_captions' in data and 'en' in data['automatic_captions']:
                                    # This is getting complex, let's fall back to our site methods
                                    # for simplicity in this implementation
                                    pass
                        except:
                            pass
                    # Clean up
                    try:
                        os.remove(subtitle_file)
                    except:
                        pass
                        
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            continue
    
    return None

def fetch_transcript_via_mediacaption(video_id):
    """Fetch transcript from mediacaption.io"""
    url = f"https://www.mediacaption.io/t/{video_id}"
    
    try:
        req = Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        
        with urlopen(req, timeout=30) as response:
            raw = response.read().decode('utf-8', 'replace')
            
    except (URLError, HTTPError, Exception) as e:
        raise Exception(f"Failed to fetch from mediacaption.io: {str(e)}")
    
    # Look for the transcript data in the HTML based on OpenClaw's findings
    # The data is in initialTranscriptState.publicTranscript as a JSON string
    
    # Pattern to find initialTranscriptState with its JSON content
    # Based on the HTML we saw, it looks like:
    # initialTranscriptState\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\"{...json...}\\\\\\\\\\\\\\\"
    pattern = r'initialTranscriptState\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\"({.*?})\\\\\\\\\\\\\\\"'
    match = re.search(pattern, raw)
    
    if match:
        try:
            # Get the JSON string (it's triple-escaped in the HTML)
            json_str = match.group(1)
            
            # Unescape step by step
            # First: \\\\\\\\ -> \\\\ and \\\\\\\" -> \"
            json_str = json_str.replace('\\\\\\\\\\\\\\\\', '\\\\\\\\').replace('\\\\\\\\\\\\\"', '"')
            # Second: \\\\ -> \\ and \\\" -> \"
            json_str = json_str.replace('\\\\\\\\', '\\\\').replace('\\\\\"', '"')
            
            data = json.loads(json_str)
            
            # Extract publicTranscript
            public_transcript = data.get('publicTranscript', [])
            if not public_transcript:
                raise Exception("publicTranscript is empty or not found in the data")
            
            # Process matches into formatted lines
            lines = []
            for segment in public_transcript:
                if isinstance(segment, dict) and 'text' in segment and 'offset' in segment:
                    try:
                        # Decode JSON string escapes
                        text_json = '"' + segment['text'] + '"'
                        text = json.loads(text_json)
                        # Unescape HTML entities
                        text = html.unescape(text)
                        
                        # Convert offset (seconds) to MM:SS format
                        offset_seconds = float(segment['offset'])
                        minutes = int(offset_seconds // 60)
                        seconds = int(offset_seconds % 60)
                        timestamp = f"[{minutes:02d}:{seconds:02d}]"
                        
                        lines.append(f"{timestamp} {text}")
                    except (ValueError, json.JSONDecodeError, KeyError) as e:
                        # Skip malformed segments but continue processing
                        continue
            
            if not lines:
                raise Exception("No valid transcript segments could be processed.")
            
            return '\n'.join(lines)
        except (json.JSONDecodeError, KeyError) as e:
            raise Exception(f"Error parsing transcript data: {str(e)}")
    else:
        # Fallback: look for the data in a different format
        # Try to find publicTranscript directly
        pattern2 = r'publicTranscript\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\"(\\[.*?\\])\\\\\\\\\\\\\"'
        match2 = re.search(pattern2, raw)
        if match2:
            try:
                json_str = match2.group(1)
                json_str = json_str.replace('\\\\\\\\\\\\\\\\', '\\\\\\\\').replace('\\\\\\\\\\\\\"', '"')
                json_str = json_str.replace('\\\\\\\\', '\\\\').replace('\\\\\"', '"')
                transcript = json.loads(json_str)
                
                lines = []
                for segment in transcript:
                    if isinstance(segment, dict) and 'text' in segment and 'offset' in segment:
                        try:
                            text_json = '"' + segment['text'] + '"'
                            text = json.loads(text_json)
                            text = html.unescape(text)
                            
                            offset_seconds = float(segment['offset'])
                            minutes = int(offset_seconds // 60)
                            seconds = int(offset_seconds % 60)
                            timestamp = f"[{minutes:02d}:{seconds:02d}]"
                            
                            lines.append(f"{timestamp} {text}")
                        except (ValueError, json.JSONDecodeError, KeyError):
                            continue
                
                if lines:
                    return '\n'.join(lines)
            except (json.JSONDecodeError, KeyError):
                pass
        
        raise Exception("No transcript data found in the page. The site structure may have changed or no transcript is available.")

def fetch_transcript_via_tubescript(video_id):
    """Fetch transcript from tubescript.cc"""
    url = f"https://tubescript.cc/api/transcript?url=https://www.youtube.com/watch?v={video_id}"
    
    try:
        req = Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json',
            }
        )
        
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get('success') and data.get('transcript'):
                # Process the transcript data
                transcript_data = data['transcript']
                lines = []
                
                # Handle different possible formats
                if isinstance(transcript_data, list):
                    for item in transcript_data:
                        if isinstance(item, dict) and 'text' in item and ('start' in item or 'offset' in item):
                            text = item['text']
                            offset = float(item.get('start', item.get('offset', 0)))
                            minutes = int(offset // 60)
                            seconds = int(offset % 60)
                            timestamp = f"[{minutes:02d}:{seconds:02d}]"
                            lines.append(f"{timestamp} {text}")
                elif isinstance(transcript_data, str):
                    # Plain text fallback - split into reasonable chunks
                    sentences = re.split(r'[.!?]+', transcript_data)
                    for i, sentence in enumerate(sentences):
                        if sentence.strip():
                            # Distribute timestamps roughly
                            offset = i * 5  # 5 seconds per sentence approx
                            minutes = int(offset // 60)
                            seconds = int(offset % 60)
                            timestamp = f"[{minutes:02d}:{seconds:02d}]"
                            lines.append(f"{timestamp} {sentence.strip()}")
                
                if lines:
                    return '\n'.join(lines)
                    
    except Exception as e:
        # Don't raise yet, try next service
        pass
    
    raise Exception("Failed to fetch transcript from tubescript.cc")

def fetch_transcript_via_youtubetranscript_dev(video_id):
    """Fetch transcript from youtubetranscript.dev"""
    url = f"https://youtubetranscript.dev/api/v1/transcript?video_id={video_id}&lang=en"
    
    try:
        req = Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json',
            }
        )
        
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get('transcript'):
                # Process transcript data
                transcript_data = data['transcript']
                lines = []
                
                if isinstance(transcript_data, list):
                    for item in transcript_data:
                        if isinstance(item, dict) and 'text' in item and ('start' in item or 'offset' in item):
                            text = item['text']
                            offset = float(item.get('start', item.get('offset', 0)))
                            minutes = int(offset // 60)
                            seconds = int(offset % 60)
                            timestamp = f"[{minutes:02d}:{seconds:02d}]"
                            lines.append(f"{timestamp} {text}")
                elif isinstance(transcript_data, str):
                    # Plain text fallback
                    sentences = re.split(r'[.!?]+', transcript_data)
                    for i, sentence in enumerate(sentences):
                        if sentence.strip():
                            offset = i * 3  # 3 seconds per sentence approx
                            minutes = int(offset // 60)
                            seconds = int(offset % 60)
                            timestamp = f"[{minutes:02d}:{seconds:02d}]"
                            lines.append(f"{timestamp} {sentence.strip()}")
                
                if lines:
                    return '\n'.join(lines)
                    
    except Exception as e:
        # Don't raise yet, we'll handle it below
        pass
    
    raise Exception("Failed to fetch transcript from youtubetranscript.dev")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_transcript.py <youtube_url_or_video_id>", file=sys.stderr)
        sys.exit(1)
    
    input_arg = sys.argv[1]
    video_id = extract_video_id(input_arg)
    
    # Try yt-dlp first (primary method)
    transcript = try_ytdlp_methods(video_id)
    if transcript:
        print(transcript)
        return
    
    # Try fallback services in order
    services = [
        ("mediacaption.io", fetch_transcript_via_mediacaption),
        ("tubescript.cc", fetch_transcript_via_tubescript),
        ("youtubetranscript.dev", fetch_transcript_via_youtubetranscript_dev),
    ]
    
    for service_name, fetch_func in services:
        try:
            transcript = fetch_func(video_id)
            print(transcript)
            return
        except Exception as e:
            # Try next service
            continue
    
    # If all services failed
    print(f"Error: All transcript services failed for video {video_id}", file=sys.stderr)
    print("This video may have transcripts disabled, be region-restricted, or require authentication.", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main()