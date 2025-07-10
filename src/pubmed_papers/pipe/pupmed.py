# src/pubmed_papers/pipe/pupmed.py

import xml.etree.ElementTree as ET
from datetime import datetime
import requests
import time
from typing import List, Dict, Any
from pubmed_papers.utils import DebugUtil

def fetch_pmids(query: str, batch_size: int = 1000) -> List[str]:
    """
    Fetch PubMed IDs (PMIDs) for a given query.
    Returns a list of PMIDs.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retstart": 0,
        "retmax": 0
    }

    try:
        # Step 1: Get total count
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        total = int(data['esearchresult']['count'])
        DebugUtil.debug_print(f"Total results: {total}")
    except Exception as e:
        DebugUtil.debug_print(f"Error fetching total count: {e}")
        return []

    all_pmids: List[str] = []

    # Step 2: Fetch in batches
    for start in range(0, total, batch_size):
        DebugUtil.debug_print(f"Fetching {start} to {start + batch_size}")
        params.update({"retstart": start, "retmax": batch_size})
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            pmids = data['esearchresult']['idlist']
            all_pmids.extend(pmids)
        except Exception as e:
            DebugUtil.debug_print(f"Failed to fetch PMIDs batch starting at {start}: {e}")
            continue
        time.sleep(0.34)  # Be nice to NCBI (max 3 requests/second)

    return all_pmids

def parse_date(article_node: ET.Element) -> str:
    """
    Parse the publication date from an article XML node.
    Returns a date string in YYYY-MM-DD format.
    """
    month_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }

    # Try ArticleDate first
    article_date = article_node.find(".//ArticleDate")
    if article_date is not None:
        year = article_date.findtext("Year", "1900")
        month = article_date.findtext("Month", "01").zfill(2)
        day = article_date.findtext("Day", "01").zfill(2)
        return f"{year}-{month}-{day}"

    # Fallback to PubDate
    pub_date = article_node.find(".//Journal/JournalIssue/PubDate")
    if pub_date is not None:
        year = pub_date.findtext("Year", "1900")
        month_raw = pub_date.findtext("Month", "01")
        day = pub_date.findtext("Day", "01").zfill(2)

        # Normalize month
        month = (
            month_map.get(month_raw, month_raw).zfill(2)
            if not month_raw.isdigit()
            else month_raw.zfill(2)
        )
        return f"{year}-{month}-{day}"

    return "1900-01-01"

def fetch_metadata(pubmed_ids: List[str], batch_size: int = 100) -> List[Dict[str, Any]]:
    """
    Fetch metadata for a list of PubMed IDs.
    Returns a list of dictionaries containing metadata for each article.
    """
    all_metadata: List[Dict[str, Any]] = []

    for i in range(0, len(pubmed_ids), batch_size):
        batch = pubmed_ids[i:i + batch_size]
        ids_param = ",".join(batch)

        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": ids_param,
            "retmode": "xml"
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                DebugUtil.debug_print(f"Failed to fetch batch starting at index {i}")
                continue
            root = ET.fromstring(response.content)
        except Exception as e:
            DebugUtil.debug_print(f"Error fetching or parsing metadata batch at index {i}: {e}")
            continue

        for article in root.findall(".//PubmedArticle"):
            try:
                pmid = article.findtext(".//PMID")
                title = article.findtext(".//ArticleTitle")
                pub_date = parse_date(article)

                authors = []
                for author in article.findall(".//AuthorList/Author"):
                    last = author.findtext("LastName", "")
                    first = author.findtext("ForeName", "")
                    name = f"{first} {last}".strip()
                    aff = author.findtext(".//Affiliation", "")
                    authors.append({"name": name, "affiliation": aff})

                all_metadata.append({
                    "pubmed_id": pmid,
                    "title": title,
                    "publication_date": pub_date,
                    "authors": authors
                })
            except Exception as e:
                DebugUtil.debug_print(f"Error parsing article metadata: {e}")
                continue

        time.sleep(0.34)  # Respect NCBI rate limits (3 requests/sec)

    return all_metadata
