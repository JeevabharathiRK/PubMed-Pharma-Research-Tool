# src/pubmed_papers/main.py

from pubmed_papers.pipe.controller import PubMedController
import argparse
import sys
import json
import csv
from typing import List, Dict, Any
from pubmed_papers.utils import DebugUtil

def save_results_csv(papers: List[Dict[str, Any]], filename: str) -> None:
    """
    Save the list of paper dictionaries to a CSV file with the required columns.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "PubmedID", "Title", "Publication Date",
            "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"
        ])
        for paper in papers:
            pubmed_id = paper.get("pubmed_id", "")
            title = paper.get("title", "")
            pub_date = paper.get("publication_date", "")
            authors = paper.get("authors", [])
            non_acad_authors = []
            companies = []
            emails = []
            for author in authors:
                aff = author.get("affiliation", {})
                if aff.get("company"):
                    non_acad_authors.append(author.get("name", ""))
                    companies.append(aff.get("company", ""))
                    if aff.get("email", "none") != "none":
                        emails.append(aff.get("email"))
            writer.writerow([
                pubmed_id,
                title,
                pub_date,
                "; ".join(non_acad_authors),
                "; ".join(companies),
                emails[0] if emails else ""
            ])

def print_readable(papers: List[Dict[str, Any]]) -> None:
    """
    Print a human-readable summary of the papers.
    """
    if not papers:
        print("No Matched papers found.")
        return
    print("Matched papers ↓")
    print("-" * 40)
    for paper in papers:
        pubmed_id = paper.get("pubmed_id", "")
        title = paper.get("title", "")
        pub_date = paper.get("publication_date", "")
        authors = paper.get("authors", [])
        non_acad_authors = []
        companies = []
        emails = []
        for author in authors:
            aff = author.get("affiliation", {})
            if aff.get("company"):
                non_acad_authors.append(author.get("name", ""))
                companies.append(aff.get("company", ""))
                if aff.get("email", "none") != "none":
                    emails.append(aff.get("email"))
        print(f"PubmedID: {pubmed_id}")
        print(f"Title: {title}")
        print(f"Publication Date: {pub_date}")
        print(f"Non-academic Author(s): {', '.join(non_acad_authors)}")
        print(f"Company Affiliation(s): {', '.join(companies)}")
        print(f"Corresponding Author Email: {emails[0] if emails else ''}")
        print("-" * 40)

def main() -> None:
    """
    Main entry point for the command-line PubMed paper search tool.
    """
    parser = argparse.ArgumentParser(description="Search PubMed papers.")

    parser.add_argument("query", help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("-f", "--file", help="Save result to a file")

    args = parser.parse_args()

    DebugUtil.enabled = args.debug

    DebugUtil.debug_print(f"Query: {args.query}")
    if args.file:
        DebugUtil.debug_print(f"Will write to file: {args.file}")

    # Initialize the PubMed controller with the query
    controller = PubMedController()
    papers: List[Dict[str, Any]] = controller.results(args.query)
    if papers is None:
        papers = []

    # Save as CSV if requested
    if args.file and args.file.endswith('.csv'):
        save_results_csv(papers, args.file)
        DebugUtil.debug_print(f"Saved results to {args.file}")
    else:
        # Save as JSON or print human-readable summary to console
        if args.file:
            result = json.dumps(papers, indent=2)
            try:
                with open(args.file, 'w', encoding='utf-8') as f:
                    f.write(result)
                DebugUtil.debug_print(f"Saved results to {args.file}")
            except Exception as e:
                DebugUtil.debug_print(f"Error saving to file: {e}", error=True)
                sys.exit(1)
        else:
            print_readable(papers)

if __name__ == "__main__":
    main()
