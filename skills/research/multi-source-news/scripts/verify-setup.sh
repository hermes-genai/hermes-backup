#!/bin/bash
# Verify multi-source-news skill setup
# Checks API keys and binary dependencies

echo "🔍 Verifying multi-source-news skill setup..."
echo "============================================"

# Check for required binaries
echo "📦 Checking required binaries:"
if command -v python3 &> /dev/null; then
    echo "  ✅ python3: $(python3 --version)"
else
    echo "  ❌ python3: NOT FOUND (required)"
fi

if command -v node &> /dev/null; then
    echo "  ✅ node: $(node --version)"
else
    echo "  ❌ node: NOT FOUND (required)"
fi

# Recommended binaries
echo ""
echo "📦 Checking recommended binaries:"
if command -v yt-dlp &> /dev/null; then
    echo "  ✅ yt-dlp: $(yt-dlp --version 2>/dev/null || echo 'version unknown')"
else
    echo "  ⚠️  yt-dlp: NOT FOUND (recommended for YouTube)"
fi

if command -v xurl &> /dev/null; then
    echo "  ✅ xurl: $(xurl --version 2>/dev/null || echo 'version unknown')"
else
    echo "  ⚠️  xurl: NOT FOUND (alternative to Twitter/X API keys)"
fi

# Check API keys from environment
echo ""
echo "🔑 Checking API keys:"
SCRAPECREATORS_KEY="${SCRAPECREATORS_API_KEY:-}"
if [[ -n "$SCRAPECREATORS_KEY" && "$SCRAPECREATORS_KEY" != *"*"* ]]; then
    echo "  ✅ SCRAPECREATORS_API_KEY: SET (length: ${#SCRAPECREATORS_KEY})"
else
    echo "  ❌ SCRAPECREATORS_API_KEY: NOT SET or placeholder (REQUIRED)"
fi

OPENAI_KEY="${OPENAI_API_KEY:-}"
if [[ -n "$OPENAI_KEY" && "$OPENAI_KEY" != *"*"* ]]; then
    echo "  ✅ OPENAI_API_KEY: SET (length: ${#OPENAI_KEY})"
else
    echo "  ⚠️  OPENAI_API_KEY: NOT SET (recommended for Reddit fallback)"
fi

XAI_KEY="${XAI_API_KEY:-}"
if [[ -n "$XAI_KEY" && "$XAI_KEY" != *"*"* ]]; then
    echo "  ✅ XAI_API_KEY: SET (length: ${#XAI_KEY})"
else
    echo "  ⚠️  XAI_API_KEY: NOT SET (optional for Twitter/X)"
fi

OPENROUTER_KEY="${OPENROUTER_API_KEY:-}"
if [[ -n "$OPENROUTER_KEY" && "$OPENROUTER_KEY" != *"*"* ]]; then
    echo "  ✅ OPENROUTER_API_KEY: SET (length: ${#OPENROUTER_KEY})"
else
    echo "  ⚠️  OPENROUTER_API_KEY: NOT SET (optional for web search)"
fi

BRAVE_KEY="${BRAVE_API_KEY:-}"
if [[ -n "$BRAVE_KEY" && "$BRAVE_KEY" != *"*"* ]]; then
    echo "  ✅ BRAVE_API_KEY: SET (length: ${#BRAVE_KEY})"
else
    echo "  ⚠️  BRAVE_API_KEY: NOT SET (optional for web search)"
fi

# Check .env file if keys not in environment
if [[ -z "$SCRAPECREATORS_KEY" || "$SCRAPECREATORS_KEY" == *"*"* ]]; then
    echo ""
    echo "📄 Checking .hermes/.env for API keys:"
    if [[ -f "/home/hermes/.hermes/.env" ]]; then
        if grep -q "SCRAPECREATORS_API_KEY=" "/home/hermes/.hermes/.env" && ! grep -q "^#.*SCRAPECREATORS_API_KEY=" "/home/hermes/.hermes/.env"; then
            echo "  ✅ SCRAPECREATORS_API_KEY: Found in .env"
        else
            echo "  ❌ SCRAPECREATORS_API_KEY: Not properly set in .env"
        fi
    else
        echo "  ❌ .hermes/.env: File not found"
    fi
fi

# Overall assessment
echo ""
echo "📋 SUMMARY:"
REQUIRED_MISSING=0
if [[ -z "$SCRAPECREATORS_KEY" || "$SCRAPECREATORS_KEY" == *"*"* ]]; then
    if [[ ! -f "/home/hermes/.hermes/.env" || ! $(grep -q "SCRAPECREATORS_API_KEY=" "/home/hermes/.hermes/.env" && ! grep -q "^#.*SCRAPECREATORS_API_KEY=" "/home/hermes/.hermes/.env") ]]; then
        echo "  ❌ REQUIRED: SCRAPECREATORS_API_KEY missing"
        ((REQUIRED_MISSING++))
    fi
fi

if ! command -v python3 &> /dev/null; then
    echo "  ❌ REQUIRED: python3 missing"
    ((REQUIRED_MISSING++))
fi

if ! command -v node &> /dev/null; then
    echo "  ❌ REQUIRED: node missing"
    ((REQUIRED_MISSING++))
fi

if [[ $REQUIRED_MISSING -eq 0 ]]; then
    echo "  ✅ All required dependencies satisfied"
    echo "  🚀 Skill is ready to use!"
else
    echo "  ❌ $REQUIRED_MISSING required dependency(ies) missing"
    echo "  🔧 Please install missing items and configure API keys"
fi

echo ""
echo "💡 TIPS:"
echo "  - Get SCRAPECREATORS_API_KEY from https://scrapecreators.com/"
echo "  - Install yt-dlp: pip install -U yt-dlp"
echo "  - Install xurl: npm install -g xurl"
echo "  - Store keys in .hermes/.env or export as environment variables"