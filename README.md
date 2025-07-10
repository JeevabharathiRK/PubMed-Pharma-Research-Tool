# PubMed-Pharma-Research-Tool

A Python command-line tool to fetch, filter, and export PubMed research papers with a focus on non-academic (industry) authors, such as those from pharmaceutical and biotech companies.

## Features

- **Fetches PubMed papers** for any search query.
- **Filters authors** to highlight those affiliated with industry (biotech, pharma, CRO, etc.), using both keyword and LLM-based matching.
- **Outputs results** as CSV or JSON, with the following columns in CSV:
  - PubmedID
  - Title
  - Publication Date
  - Non-academic Author(s)
  - Company Affiliation(s)
  - Corresponding Author Email
- **Command-line options** for query, debug output, and output file selection.
- **Batch processing** to respect API and LLM rate limits.
- **Robust error handling** and debug logging.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/JeevabharathiRK/PubMed-Pharma-Research-Tool.git
   cd PubMed-Pharma-Research-Tool
   ```

2. **Install dependencies using Poetry:**
   ```sh
   poetry install
   ```

3. **(Optional) Build the package:**
   ```sh
   poetry build
   ```

## Environment Variables

Before running the tool, you must set your environment variables for LLM-based filtering (such as your LLM API key).

- **On Windows:**  
  Edit the provided `set-envs.ps1` and run the script:
  ```powershell
  .\set-envs.ps1
  ```

- **On Mac/Linux:**  
  Edit the provided `set-envs.sh` and run the script:
  ```sh
  source set-envs.sh
  ```

These scripts will set the necessary environment variables required for LLM API access.

## Usage

After installation, you can run the tool from the command line:

```sh
poetry run get-papers-list "your pubmed query here" -f results.csv
```

### Command-line Options

- `-h`, `--help` : Show usage instructions.
- `-d`, `--debug` : Enable debug logging.
- `-f`, `--file` : Specify output filename (CSV or JSON). If omitted, prints to console.

**Example:**

```sh
poetry run get-papers-list "micrornas genomics biogenesis mechanism inc" -f results.csv
```

## Output

- **CSV**: Contains columns for PubmedID, Title, Publication Date, Non-academic Author(s), Company Affiliation(s), Corresponding Author Email.
- **JSON**: Full structured output with all matched papers and authors.

## Development

- **Project structure:**  
  - Source code: `src/pubmed_papers/`
  - CLI entry point: `src/pubmed_papers/main.py`
  - Utilities and pipeline: `src/pubmed_papers/pipe/`
- **Version control:**  
  - Managed with Git and hosted on GitHub.
- **Dependency management:**  
  - Managed with Poetry (`pyproject.toml`).

## Notes

- Requires a valid PubMed API connection (no API key needed for basic usage).
- For LLM-based filtering, you must set the appropriate API key as an environment variable (see code for details).
- Respects PubMed and LLM API rate limits.

## License

MIT License

---

**For questions or contributions, please open an issue or pull request on GitHub.**
