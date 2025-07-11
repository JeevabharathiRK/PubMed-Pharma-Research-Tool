# src/pubmed_papers/pipe/classify.py

from pubmed_papers.pipe.keymatch import KeyMatch
from pubmed_papers.pipe.LLMmatch import filter_industry_papers_llama3
from typing import List, Dict, Any
from pubmed_papers.utils import DebugUtil

def filter_biotech_papers(papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter papers for biotech/pharma industry affiliations using two layers:
    1. KeyMatch for fast keyword-based filtering.
    2. LLM-based filtering for unmatched papers.
    Returns a list of matched papers.
    """
    keymatch = KeyMatch()
    try:
        # Layer 1: Fast keyword-based matching
        matched, un_matched = keymatch.get_filter(papers)
        DebugUtil.debug_print(f"Layer 1 matched: {len(matched)}, unmatched: {len(un_matched)}")
    except Exception as e:
        DebugUtil.debug_print(f"Error in KeyMatch filtering: {e}", error=True)
        return []

    # If all papers matched in layer 1, return them
    if not un_matched:
        return matched

    # Layer 2: Use LLM to match remaining papers
    try:
        llm_matched = filter_industry_papers_llama3(un_matched)
        DebugUtil.debug_print(f"Layer 2 LLM matched: {len(llm_matched)}")
    except Exception as e:
        DebugUtil.debug_print(f"Error in LLM filtering: {e}", error=True)
        llm_matched = []

    return matched + llm_matched