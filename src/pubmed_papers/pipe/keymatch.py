# src/pubmed_papers/pipe/keymatch.py

import re
from typing import List, Dict, Tuple
from pubmed_papers.utils import DebugUtil

class KeyMatch:
    def __init__(self) -> None:
        # List of keywords indicating company/industry affiliations
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
        # List of keywords indicating academic/non-profit affiliations
        self.exclude_keywords = [
            'institute', 'university', 'college', 'academy', 'school', 'hospital', 'centre', 'center', 'faculty'
        ]
        # Compile regex patterns for matching
        self.pattern = r'(' + '|'.join([rf'\b{re.escape(k)}\b' for k in self.company_keywords]) + r')'
        self.exclude_pattern = r'(' + '|'.join([rf'\b{re.escape(k)}\b' for k in self.exclude_keywords]) + r')'

    def get_filter(self, papers: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Filters papers for industry affiliations using keyword matching.
        Returns a tuple: (matched_papers, unmatched_papers)
        """
        matched: List[Dict] = []
        un_matched: List[Dict] = []
        email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')

        for paper in papers:
            matched_authors: List[Dict] = []
            try:
                for author in paper.get('authors', []):
                    affiliation = author.get('affiliation', '')
                    affiliation_lower = affiliation.lower()
                    match = re.search(self.pattern, affiliation_lower)
                    exclude_match = re.search(self.exclude_pattern, affiliation_lower)
                    if match and not exclude_match:
                        # Find the matched keyword (company name)
                        company = match.group(0)
                        # Extract the company name with surrounding commas
                        parts = [p.strip() for p in affiliation.split(',')]
                        company_name = None
                        for part in parts:
                            if company in part.lower():
                                company_name = part.strip()
                                break
                        if not company_name:
                            company_name = company  # fallback

                        # Extract first email if present
                        emails = email_pattern.findall(affiliation)
                        email = emails[0] if emails else "none"

                        matched_authors.append({
                            "name": author.get("name", ""),
                            "affiliation": {
                                "company": company_name,
                                "email": email
                            }
                        })
            except Exception as e:
                DebugUtil.debug_print(f"Error processing paper '{paper.get('pubmed_id', '')}': {e}", error=True)
                continue

            if matched_authors:
                new_paper = paper.copy()
                new_paper['authors'] = matched_authors
                matched.append(new_paper)
            else:
                un_matched.append(paper)

        DebugUtil.debug_print(f"KeyMatch: {len(matched)} matched, {len(un_matched)} unmatched")
        return (matched, un_matched)