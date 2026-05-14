# Last30Days Skill Overview

Based on examination of https://github.com/mvanhorn/last30days-skill

## Core Approach
The last30days skill researches what people are saying about any topic across multiple platforms in the last 30 days, then synthesizes a grounded summary.

## Source Detection Logic
The skill automatically detects available sources based on:
- Installed binaries (node, python3, yt-dlp)
- Available API keys (SCRAPECREATORS, OPENAI, XAI, etc.)
- CLI tool availability (xurl for Twitter/X)

## Source Coverage Matrix

| Source | Requirement | Notes |
|--------|-------------|-------|
| Reddit | SCRAPECREATORS_API_KEY (primary) or OPENAI_API_KEY (fallback) | Uses scrapecreators as backup when public Reddit unavailable |
| X/Twitter | AUTH_TOKEN+CT0, XAI_API_KEY, or xurl CLI | Multiple authentication methods supported |
| YouTube | yt-dlp binary | No API key needed, uses public data |
| TikTok | SCRAPECREATORS_API_KEY | Pay-as-you-go after 10k free calls |
| Instagram | SCRAPECREATORS_API_KEY | Pay-as-you-go after 10k free calls |
| Hacker News | None | Always available via Algolia API |
| Polymarket | None | Always available via Gamma API |
| GitHub | None | Public API, rate limited without auth |
| Web Search | BRAVE_API_KEY, PARALLEL_API_KEY, or OPENROUTER_API_KEY | Optional enhancement |

## Output Format
- Mandatory first-line badge: `🌐 last30days v{VERSION} · synced {YYYY-MM-DD}`
- Structured sections with citations
- Source breakdown showing percentage from each platform
- Links to original sources when available

## Key Features
- Parallel source searching for efficiency
- Engagement-based ranking for quality filtering
- Automatic source detection and fallback handling
- Local SQLite database for watchlist mode (optional)
- Markdown output files saved to LAST30DAYS_MEMORY_DIR

## Limitations
- Requires SCRAPECREATORS_API_KEY for full social media coverage
- Some sources have rate limits (GitHub, web search APIs)
- Content requires filtering for signal-to-noise ratio
- Best suited for topics with recent social discussion