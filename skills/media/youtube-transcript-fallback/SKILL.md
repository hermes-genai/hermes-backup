---
name: youtube-transcript-fallback
description: "Comprehensive YouTube transcript fallback system - tries multiple public transcript sites when YouTube API is blocked"
platforms: [linux, macos, windows]
---

# YouTube Transcript Fallback Skill

This skill provides a robust method to fetch YouTube transcripts when the standard YouTube API is blocked (e.g., due to bot protection). It implements a multi-service fallback approach:

1. First attempts to get subtitles via yt-dlp with alternative players
2. If that fails, tries multiple public transcript sites in order:
   - mediacaption.io
   - tubescript.cc
   - youtubetranscript.dev
3. Outputs a timestamped markdown transcript

## Usage

```bash
# Fetch transcript for a YouTube video
python3 -m youtube_transcript_fallback.scripts.fetch_transcript <youtube_url_or_video_id>

# Or run the script directly
python3 /path/to/skill/scripts/fetch_transcript.py <youtube_url_or_video_id>
```

## Methods

### Method 1: yt-dlp with Alternative Players
Tries to download auto-generated subtitles using different YouTube embedded players to bypass bot detection:
- android player
- web_embedded player
- Default player (as fallback)

### Method 2: Public Transcript Sites Fallback
When yt-dlp fails, tries multiple public transcript sites:
- mediacaption.io (parses initialTranscriptState JSON)
- tubescript.cc (extracts transcript from response)
- youtubetranscript.dev (uses their API endpoint)

## Installation

The skill is self-contained. Requires:
- Python 3.x
- yt-dlp (for primary method)
- urllib, json, re, html (standard library)

## Example

```bash
$ python3 fetch_transcript.py "https://youtu.be/exampleID"
[00:00] Transcript text here...
[00:05] More transcript text...
```

## Notes

- The skill outputs to stdout; redirect to a file to save: `python3 fetch_transcript.py URL > transcript.md`
- Tries services in order until one succeeds
- If all methods fail, provides clear error message with suggestions