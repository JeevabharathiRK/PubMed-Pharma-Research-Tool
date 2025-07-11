# src/pubmed_papers/pipe/controller.py

from pubmed_papers.pipe.pupmed import fetch_pmids, fetch_metadata
from pubmed_papers.pipe.classify import filter_biotech_papers
from typing import List, Dict, Any
from pubmed_papers.utils import DebugUtil

class PubMedController:
    def __init__(self) -> None:
        self.query: str = ""

    def results(self, query: str) -> List[Dict[str, Any]]:
        """
        Fetches PubMed papers for a given query, filters for biotech/pharma affiliations,
        and returns a list of matched paper dictionaries.
        """
        self.query = query
        try:
            # Fetch all PMIDs based on the query
            pmids = fetch_pmids(self.query)
            DebugUtil.debug_print(f"Fetched {len(pmids)} PMIDs for query: {self.query}")
            if not pmids:
                DebugUtil.debug_print("No PMIDs found for the query.")
                return []
        except Exception as e:
            DebugUtil.debug_print(f"Error fetching PMIDs: {e}", error=True)
            return []

        try:
            # Fetch metadata for the PMIDs (all papers for the query)
            metadata = fetch_metadata(pmids)
            DebugUtil.debug_print(f"Fetched metadata for {len(metadata)} papers.")
        except Exception as e:
            DebugUtil.debug_print(f"Error fetching metadata: {e}", error=True)
            return []

        try:
            # Filter papers affiliated with Biotech or Pharmaceuticals
            filtered_papers = filter_biotech_papers(metadata)
            DebugUtil.debug_print(f"Filtered papers, {len(filtered_papers)} matched.")
        except Exception as e:
            DebugUtil.debug_print(f"Error filtering papers: {e}", error=True)
            return []

        # Ensure always a list
        if isinstance(filtered_papers, dict):
            return filtered_papers.get("papers", [])
        return filtered_papers if filtered_papers is not None else []