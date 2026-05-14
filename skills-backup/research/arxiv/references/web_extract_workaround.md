# Workaround for web_extract failures with arxiv.org

When attempting to extract content from arxiv.org PDFs using `web_extract`, you may encounter authentication errors like:
```
Unauthorized: Failed to scrape. Unauthorized: Invalid token - No additional error details provided.
```

This occurs due to OpenRouter authentication requirements for the web_extract tool when accessing certain domains.

## Solution

Use this two-step process instead:

### 1. Download the PDF manually
```bash
curl -s "https://arxiv.org/pdf/2402.03300" -o /tmp/paper.pdf
```

### 2. Extract text using the ocr-and-documents skill
```bash
# Plain text extraction (good for quick reading)
hermes ocr-and-documents --file /tmp/paper.pdf

# Markdown output (better for further processing, preserves structure)
hermes ocr-and-documents --file /tmp/paper.pdf --markdown

# Extract specific pages (e.g., first 10 pages)
hermes ocr-and-documents --file /tmp/paper.pdf --pages 0-9

# Extract tables from the paper
hermes ocr-and-documents --file /tmp/paper.pdf --tables
```

## Why this works

- The `ocr-and-documents` skill uses local PDF processing libraries (pymupdf, marker-pdf) that don't rely on external APIs with authentication requirements
- This approach gives you full control over the extraction process
- You can choose between plain text, markdown, or structured output formats
- Works reliably for arxiv.org and other academic PDF sources

## When to use this workaround

- When `web_extract(urls=["https://arxiv.org/pdf/PAPER_ID"])` returns authentication errors
- When you need more control over the extraction process (specific pages, tables, etc.)
- When batch processing multiple PDFs
- When you want to avoid dependency on external web scraping services