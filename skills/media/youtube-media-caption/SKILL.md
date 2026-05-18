---
name: youtube-media-caption
description: "Fetch YouTube transcripts via public transcript sites when direct API access is blocked"
platforms: [linux, macos, windows]
---

# YouTube Media Caption Skill

This skill provides a robust method to fetch YouTube transcripts when the standard YouTube API is blocked (e.g., due to bot protection). It implements the approach discovered by OpenClaw:

1. First attempts to get subtitles via yt-dlp with alternative players (android, web_embedded)
2. If that fails, falls back to parsing transcript data from public transcript sites like mediacaption.io
3. Outputs a timestamped markdown transcript

## Usage

```bash
# Fetch transcript for a YouTube video
python3 -m youtube_media_caption.scripts.fetch_transcript <youtube_url_or_video_id>

# Or run the script directly
python3 /path/to/skill/scripts/fetch_transcript.py <youtube_url_or_video_id>
```

## Methods

### Method 1: yt-dlp with Alternative Players
Tries to download auto-generated subtitles using different YouTube embedded players to bypass bot detection:
- android player
- web_embedded player
- Default player (as fallback)

### Method 2: Medi caption.io Fallback
When yt-dlp fails, fetches the transcript from mediacaption.io by:
1. Downloading the page
2. Extracting the `initialTranscriptState` JSON from the HTML
3. Parsing the `publicTranscript` array
4. Converting offsets to MM:SS timestamps
5. Unescaping HTML entities in the text

## Installation

The skill is self-contained. Requires:
- Python 3.x
- yt-dlp (for primary method)
- urllib (standard library)
- json, re, html (standard library)

## Example

```bash
$ python3 fetch_transcript.py "https://youtu.be/Hxzfvz1zyos?si=p3Vf9A2bENyhng9-"
[00:00] Willkommen zu Skobel, Philosophie,
[00:02] Wissenschaft und Leben im Gespräch. Und
[00:04] aus der Ferne sieht's ja häufig so aus,
...
```

## Notes

- The skill outputs to stdout; redirect to a file to save: `python3 fetch_transcript.py URL > transcript.md`
- If both methods fail, an error message is printed to stderr
- The mediacaption.io parser is specific to their current HTML structure and may break if the site changes
- **YouTube IP blocking**: YouTube often blocks requests from cloud provider IPs (AWS, GCP, Azure). When this happens, the fallback to mediacaption.io or similar sites is essential.
- **Workflow preference**: When analyzing YouTube transcripts (for summaries, explanations, etc.), prefer to use the Gemini API via GEMINI_API_KEY in .env as specified by the user.