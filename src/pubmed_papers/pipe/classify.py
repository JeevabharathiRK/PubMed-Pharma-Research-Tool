# src/pubmed_papers/pipe/classify.py

from pubmed_papers.pipe.keymatch import KeyMatch
from typing import List, Dict

def filter_biotech_papers(papers: List[Dict]) -> List[Dict]:
    keymatch = KeyMatch()
    matched, un_matched = keymatch.get_filter(papers)
    return matched
