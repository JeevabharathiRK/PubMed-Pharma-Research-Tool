# src/pubmed_papers/pipe/controller.py

from pubmed_papers.pipe.pupmed import *
from pubmed_papers.pipe.classify import *

class PubMedController:
    def __init__(self, query: str):
        self.query = query

    def results(self, query: str) -> list:
        # Fetch all PMIDs based on the query
        pmids = fetch_pmids(self.query)
        if not pmids:
            return []

        # Fetch metadata for the PMIDs (all papers for the query)
        metadata = fetch_metadata(pmids)

        # Filter papers affiliated with Biotech or Pharmaceuticals
        filtered_papers = filter_biotech_papers(metadata)

        return filtered_papers