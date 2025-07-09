# src/pubmed_papers/pipe/keymatch.py

import re
from typing import List, Dict

class KeyMatch:
    def __init__(self):
        self.company_keywords = [
            # Corporate suffixes
            'inc', 'ltd', 'llc', 'llp', 'plc', 'pvt', 's.a.', 's.r.l', 'gmbh', 'co.', 'corporation', 'incorporated',
            # Industry-specific indicators
            'therapeutics', 'pharmaceutical', 'pharmaceuticals', 'biopharmaceuticals', 'biopharma', 'biotech', 'biotherapeutics',
            # CRO/Clinical indicators
            'cro', 'contract research organization', 'clinical trials inc', 'clinical research ltd',
            # Safe modifiers
            'drug development', 'drug discovery',
            # Highly specific
            'rx', 'holdings', 'ventures', 'biosolutions inc', 'biosciences ltd', 'diagnostics inc', 'healthtech ltd',
            'medtech inc', 'life sciences inc', 'oncology ltd', 'vaccines inc', 'genomics inc'
        ]
        self.pattern = r'(' + '|'.join([rf'\b{re.escape(k)}\b' for k in self.company_keywords]) + r')'

    def get_filter(self, papers: List[Dict]) -> List[Dict]:
        matched = []
        for paper in papers:
            for author in paper.get('authors', []):
                affiliation = author.get('affiliation', '').lower()
                if re.search(self.pattern, affiliation):
                    matched.append(paper)
                    break  # No need to check more authors for this paper
        un_matched = [paper for paper in papers if paper not in matched]
        return (matched,un_matched)