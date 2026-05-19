When web scraping arxiv.org fails due to unauthorized access (common with automated tools), use the arXiv API endpoint:
https://export.arxiv.org/api/query?search_query=id:<paper_id>&max_results=1

Replace <paper_id> with the arXiv identifier (e.g., 2603.20617v1).

This returns XML metadata including title, authors, abstract, and links to PDF/HTML versions.