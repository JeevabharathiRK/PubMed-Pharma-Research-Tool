# pubmed_papers/main.py

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Search PubMed papers.")

    parser.add_argument("query", help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("-f", "--file", help="Save result to a file")

    args = parser.parse_args()

    if args.debug:
        print(f"[DEBUG] Query: {args.query}", file=sys.stderr)
        if args.file:
            print(f"[DEBUG] Will write to file: {args.file}", file=sys.stderr)

    # Dummy result simulation
    result = f"Results for PubMed query: {args.query}"

    if args.file:
        try:
            with open(args.file, 'w') as f:
                f.write(result)
            print(f"Saved results to {args.file}")
        except Exception as e:
            print(f"Error saving to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(result)
