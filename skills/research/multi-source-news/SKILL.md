---
name: multi-source-news
description: Generate current, multi-source news summaries using Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and web search
version: "1.0.0"
author: hermes-agent
license: MIT
tags: [news, research, social-media, web-search, ai-skill]
---

# Multi-Source News Generation Skill

This skill generates comprehensive, up-to-date news summaries by researching what people are saying across multiple platforms in the last 30 days. It provides significantly better coverage and recency than basic web search alone.

## 🔑 **Required API Keys**

### **⭐ PRIMARY (Required):**
- **SCRAPECREATORS_API_KEY** - Essential for TikTok, Instagram, and Reddit backup search
  - Get from: https://scrapecreators.com/
  - Includes 10,000 free API calls/month

### **🔧 OPTIONAL (Enhances Sources):**
- **OPENAI_API_KEY** - For OpenAI Responses API (Reddit discovery fallback)
- **XAI_API_KEY** - For X/Twitter search via xAI's API
- **OPENROUTER_API_KEY** - For Perplexity/web search
- **PARALLEL_API_KEY** - For Parallel AI web search
- **BRAVE_API_KEY** - For Brave Search API
- **APIFY_API_TOKEN** - For additional web scraping
- **AUTH_TOKEN** + **CT0** - For Twitter/X GraphAPI search
- **BSKY_HANDLE** + **BSKY_APP_PASSWORD** - For Bluesky search
- **TRUTHSOCIAL_TOKEN** - For Truth Social search

### **💻 REQUIRED BINARIES:**
- `node` (JavaScript runtime)
- `python3` (Python 3.x)

## 📰 **What This Skill Covers**

The skill searches and synthesizes content from:
- **Reddit** (posts & comments)
- **X/Twitter** (tweets & engagement)
- **YouTube** (videos & transcripts via yt-dlp)
- **TikTok & Instagram** (via ScrapeCreators API)
- **Hacker News** (stories & comments)
- **Polymarket** (prediction markets)
- **GitHub** (repos, issues, discussions)
- **Web search** (configurable via optional APIs)

## 🔄 **Workflow**

1. **Source Detection**: Automatically detects which sources are available based on installed tools and API keys
2. **Parallel Search**: Queries all available sources simultaneously for the topic
3. **Content Extraction**: Extracts posts, comments, videos, transcripts, and engagement metrics
4. **Relevance Filtering**: Filters results to the last 30 days and ranks by relevance/engagement
5. **Synthesis**: Combines findings into a coherent summary with citations
6. **Output**: Generates a formatted news briefing with source attribution

## 🛠️ **Usage**

### As a Hermes Skill:
```bash
# Load and use the skill
skill_view(name='multi-source-news')

# Invoke with a topic (example)
delegate_task(
  skill='multi-source-news',
  argument='latest Generative AI developments May 2026',
  context='Create a newsflash for #genai-newsflash channel'
)
```

### Direct Invocation Pattern:
The skill follows this internal pattern:
```
1. Check available sources (based on keys/tools)
2. Search each source for topic from last 30 days
3. Extract and normalize content
4. Rank by engagement/recency
5. Synthesize into structured report
6. Format with citations and source breakdown
```

## ⚠️ **Pitfalls & Best Practices**

### **Common Issues:**
- **Missing SCRAPECREATORS_API_KEY**: Will severely limit TikTok/Instagram/Reddit coverage
- **No node/python3**: Skill will fail to initialize - ensure both are installed
- **Rate limiting**: Some sources have strict limits; skill includes basic backoff
- **Content noise**: Raw social media requires filtering - skill uses engagement metrics for quality

### **Optimization Tips:**
1. **Always provide SCRAPECREATORS_API_KEY** - it unlocks the most valuable social sources
2. **Add OPENAI_API_KEY** as fallback for Reddit when scrapecreators is unavailable
3. **Consider XAI_API_KEY** for real-time Twitter/X insights
4. **Monitor API usage** - especially on paid services like scrapecreators after free tier
5. **Test with specific topics** before scheduling regular cron jobs

## 🔧 **Integration with Hermes Cron Jobs**

To enhance existing newsflash jobs:

1. **Store API keys** in `.hermes/.env`:
   ```
   SCRAPECREATORS_API_KEY=your_key_here
   # Optional but recommended:
   OPENAI_API_KEY=your_openai_key
   XAI_API_KEY=your_xai_key
   ```

2. **Update cron job** to use this skill instead of basic web search:
   - Change from general web_search to multi-source-news skill
   - Provide topic-specific arguments
   - Route output to appropriate Slack channel

3. **Schedule considerations**:
   - Newsflash: Daily (covers last 24-48 hours)
   - Research updates: Daily or every few days
   - Adjust based on topic velocity and API limits

## 📊 **Expected Output Format**

Generated reports include:
- 📰 **Headline badge** with source list and timeframe
- 🔥 **Key developments** (3-5 items with descriptions)
- 📊 **Source breakdown** (percentage from each platform)
- 🔗 **Citations** with links to original sources
- ⏱️ **Timeframe** covered (e.g., "Last 30 days" or "Last 72 hours" for fast topics)
- 🏷️ **Topic tags** for categorization

## 🔍 **Verification & Testing**

Run a test invocation before deploying to cron:
```bash
# Test with a narrow topic to verify setup
multi-source-news "specific AI model release name"

# Verify output contains:
# - Recent information (within last few days)
# - Multiple source types
# - Proper citations/links
# - No hallucinated or outdated content
```

## 📁 **Support Files**

- `references/last30days-skill-overview.md` - Summary of the underlying last30days-skill approach
- `references/api-requirements.md` - Detailed API key requirements and sources
- `templates/newsflash-template.md` - Boilerplate for formatting newsflash outputs
- `scripts/verify-setup.sh` - Script to check API keys and binary dependencies