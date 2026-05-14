# API Key Requirements for Multi-Source News

## 🔑 Required API Keys

### **SCRAPECREATORS_API_KEY** (PRIMARY - REQUIRED for full functionality)
- **Source**: https://scrapecreators.com/
- **Purpose**: Enables TikTok, Instagram, and Reddit backup search
- **Free Tier**: 10,000 API calls/month
- **After Free Tier**: Pay-as-you-go pricing
- **Impact if Missing**: 
  - No TikTok/Instagram content
  - Reddit falls back to OPENAI_API_KEY (if available) or is skipped
  - Significantly reduced social media coverage

### **OPENAI_API_KEY** (OPTIONAL but RECOMMENDED)
- **Source**: https://platform.openai.com/api-keys
- **Purpose**: 
  - Reddit discovery fallback when ScrapeCreators unavailable/unsuccessful
  - Can be used for web search via OpenAI's Responses API
- **Impact if Missing**: 
  - Reduced Reddit coverage if ScrapeCreators fails
  - No OpenAI-powered web search fallback

### **XAI_API_KEY** (OPTIONAL)
- **Source**: https://console.x.ai/
- **Purpose**: X/Twitter search via xAI's API
- **Impact if Missing**:
  - Falls back to AUTH_TOKEN+CT0 or xurl CLI for Twitter/X
  - May miss real-time Twitter conversations if no other auth available

### **OPENROUTER_API_KEY** (OPTIONAL)
- **Source**: https://openrouter.ai/keys
- **Purpose**: 
  - Perplexity/web search via OpenRouter
  - Access to 100+ LLMs for search enhancement
- **Impact if Missing**: 
  - No OpenRouter-powered web search
  - Relies on other web search options or basic fallback

### **PARALLEL_API_KEY** (OPTIONAL)
- **Source**: https://parallel.ai/
- **Purpose**: Parallel AI web search API
- **Impact if Missing**: 
  - No Parallel AI web search
  - Less robust web search coverage

### **BRAVE_API_KEY** (OPTIONAL)
- **Source**: https://brave.com/search/api/
- **Purpose**: Brave Search API
- **Impact if Missing**: 
  - No Brave Search results
  - Reduced web search diversity

### **APIFY_API_TOKEN** (OPTIONAL)
- **Source**: https://apify.com/
- **Purpose**: Additional web scraping and automation capabilities
- **Impact if Missing**: 
  - No Apify-powered scraping
  - Limited to built-in source methods

### **AUTH_TOKEN + CT0** (OPTIONAL - for Twitter/X)
- **Source**: Obtained from logged-in Twitter/X web session
- **Purpose**: Twitter/X GraphAPI search
- **How to Get**: 
  1. Log into twitter.com/x.com in browser
  2. Open DevTools → Application → Cookies → https://twitter.com
  3. Find `auth_token` and `ct0` cookie values
- **Impact if Missing**: 
  - Falls back to XAI_API_KEY or xurl CLI
  - May miss Twitter/X content if no other auth available

### **BSKY_HANDLE + BSKY_APP_PASSWORD** (OPTIONAL - for Bluesky)
- **Source**: 
  - Handle: Your Bluesky username (e.g., user.bsky.social)
  - App Password: Generated in Bluesky Settings → App Passwords
- **Purpose**: Bluesky social search
- **Impact if Missing**: 
  - No Bluesky content
  - Missing emerging social platform discussions

### **TRUTHSOCIAL_TOKEN** (OPTIONAL - for Truth Social)
- **Source**: Obtained from logged-in Truth Social session
- **Purpose**: Truth Social search
- **Impact if Missing**: 
  - No Truth Social content
  - Missing niche social platform discussions

## 📊 Source Availability Matrix

| Source | Required Key/Binary | Free Tier | Notes |
|--------|-------------------|-----------|-------|
| Reddit | SCRAPECREATORS or OPENAI | Limited | Scrapecreators preferred |
| X/Twitter | XAI or AUTH+CT0 or xurl | None | Multiple auth options |
| YouTube | yt-dlp binary | Unlimited | No API needed |
| TikTok | SCRAPECREATORS | 10k/mo | PAYG after free |
| Instagram | SCRAPECREATORS | 10k/mo | PAYG after free |
| Hacker News | None | Unlimited | Always available |
| Polymarket | None | Unlimited | Always available |
| GitHub | None | Limited | Rate limited without auth |
| Web Search | BRAVE/PARALLEL/OPENROUTER | Varies | Optional enhancement |

## 💰 Cost Considerations

### **Free Sources** (Always available if tools installed):
- Hacker News (hn.algolia.com)
- Polymarket (gamma-api.polymarket.com) 
- GitHub (api.github.com - rate limited)
- YouTube (via yt-dlp - public data)
- Reddit (reddit.com - rate limited)
- Web (via duckduckgo/google - if no API keys)

### **Paid/Freemium Sources**:
- **ScrapeCreators**: 10k free calls/mo, then PAYG
- **OpenAI**: Pay-per-use (if used for search/fallback)
- **xAI**: Pay-per-use (if available)
- **OpenRouter**: Pay-per-use (based on model selected)
- **Parallel AI**: Subscription-based
- **Brave Search**: Free tier available
- **Apify**: Free tier + PAYG

## 🔧 Setup Recommendations

### **Minimum Viable Setup**:
```env
SCRAPECREATORS_API_KEY=your_key_here
# Gets you: TikTok, Instagram, Reddit backup
# Plus: YouTube, HN, Polymarket, GitHub, basic web
```

### **Recommended Setup**:
```env
SCRAPECREATORS_API_KEY=your_key_here
OPENAI_API_KEY=your_openai_key_here   # Reddit fallback + web search
XAI_API_KEY=your_xai_key_here         # Better Twitter/X coverage
# Gets you: All major social platforms + web search options
```

### **Maximum Coverage**:
```env
SCRAPECREATORS_API_KEY=your_key_here
OPENAI_API_KEY=your_openai_key_here
XAI_API_KEY=your_xai_key_here
OPENROUTER_API_KEY=your_openrouter_key
PARALLEL_API_KEY=your_parallel_key
BRAVE_API_KEY=your_brave_key
APIFY_API_TOKEN=your_apify_token
AUTH_TOKEN=your_twitter_auth_token
CT0=your_twitter_ct0
BSKY_HANDLE=your_bluesky_handle
BSKY_APP_PASSWORD=your_bluesky_app_password
TRUTHSOCIAL_TOKEN=your_truthsocial_token
# Gets you: Every possible source the skill can access
```

## 📱 Binary Dependencies

### **Required**:
- `python3` - Core skill execution
- `node` - JavaScript runtime for some source connectors

### **Highly Recommended**:
- `yt-dlp` - YouTube video and transcript extraction
  - Install: `pip install -U yt-dlp`
- `xurl` - Twitter/X OAuth2 CLI (alternative to API keys)
  - Install: `npm install -g xurl`

### **Optional but Useful**:
- `jq` - JSON processing (for debugging)
- `curl` - HTTP requests (for testing)