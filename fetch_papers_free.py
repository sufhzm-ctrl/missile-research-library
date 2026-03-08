#!/usr/bin/env python3
"""
Fetch missile-related academic papers from arXiv.
No AI summaries - uses original abstracts (completely free).
"""

import feedparser
import requests
import json
import os
from datetime import datetime

# Configuration
ARXIV_FEED_URL = "http://export.arxiv.org/api/query?search_query=cat:cs.RO+AND+(missile+OR+ballistic+OR+guidance+OR+trajectory+OR+defense)&sortBy=submittedDate&sortOrder=descending&start=0&max_results=10"
OUTPUT_FILE = "docs/data/papers.json"

def fetch_arxiv_papers():
    """Fetch recent papers from arXiv"""
    print("Fetching papers from arXiv...")
    try:
        response = requests.get(ARXIV_FEED_URL, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        
        papers = []
        for entry in feed.entries:
            paper = {
                "title": entry.title,
                "authors": [author.name for author in entry.authors],
                "published": entry.published,
                "arxiv_id": entry.id.split('/abs/')[-1],
                "url": entry.id,
                "abstract": entry.summary.replace('\n', ' ').strip(),
                "categories": entry.get('arxiv_primary_category', {}).get('term', 'Unknown')
            }
            papers.append(paper)
        
        print(f"✓ Fetched {len(papers)} papers")
        return papers
    except Exception as e:
        print(f"✗ Error fetching papers: {e}")
        return []

def save_data(papers):
    """Save papers to JSON file"""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    data = {
        "last_updated": datetime.now().isoformat(),
        "total_papers": len(papers),
        "papers": papers
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Data saved to {OUTPUT_FILE}")

def main():
    """Main execution"""
    papers = fetch_arxiv_papers()
    if papers:
        save_data(papers)
        print("\n✓ Done! Site updated with new papers.")
    else:
        print("\n✗ No papers found or error occurred.")

if __name__ == "__main__":
    main()
