import os
import time
import re
import json
from typing import List, Dict
from tqdm import tqdm
from groq import Groq
from pubmed_papers.utils import DebugUtil

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable not set")
client = Groq(api_key=GROQ_API_KEY)

def extract_first_email(text: str) -> str:
    """
    Extracts the first email address from a string, or returns 'none' if not found.
    """
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    return emails[0] if emails else "none"

def filter_industry_papers_llama3(papers: List[Dict]) -> List[Dict]:
    """
    Sends all paper metadata to LLM in batches.
    Returns only papers with at least one industry-matched author,
    with authors structured as {"name": ..., "affiliation": {"company": ..., "email": ...}}
    """
    DebugUtil.debug_print(f"Total papers received: {len(papers)}")
    batch_size = 10  # adjust as needed to stay within token/request limits

    matched_papers: List[Dict] = []
    for i in tqdm(range(0, len(papers), batch_size), desc="Classifying papers"):
        batch = papers[i:i+batch_size]
        # Prepare prompt
        system_prompt = (
            "You are an expert in biomedical research and precise data extraction. "
            "Your primary goal is to identify and extract details of 'industry-oriented' authors from scientific papers. "
            "Industry-oriented affiliations explicitly include: biotech firms, pharmaceutical corporations, contract research organizations (CROs), and any other private companies. "
            "Academic institutions (universities, colleges, university hospitals, academic research institutes) and government research centers/agencies are NOT considered industry-oriented."
            "\n\nFor each paper provided in the 'INPUT PAPERS' section, perform the following steps:"
            "\n1. Analyze all authors and their affiliations."
            "\n2. Identify authors whose affiliations are 'industry-oriented' as defined above."
            "\n3. For each identified industry-oriented author, extract their full name."
            "\n4. From their affiliation text, accurately extract ONLY the most prominent company or institution name. Prioritize names that clearly indicate a private company, typically found between commas. If an affiliation lists multiple entities, focus on the core industry name."
            "\n5. Extract the *first* valid email address associated with *that specific author's* affiliation if present. If no email is found, use 'none'."
            "\n\n'OUTPUT JSON FORMAT':"
            "\nReturn a JSON list. Each item in the list must represent a paper that contains at least one industry-oriented author. Papers with no industry-oriented authors MUST be omitted."
            "\nEach paper object in the JSON list must have the following structure:"
            "\n{"
            "\n  \"pubmed_id\": \"<Unique identifier for the paper>\","
            "\n  \"title\": \"<Title of the paper>\","
            "\n  \"publication_date\": \"<Date the paper was published> (YYYY-MM-DD format preferred)\","
            "\n  \"authors\": ["
            "\n    {"
            "\n      \"name\": \"<Full name of the industry-oriented author>\","
            "\n      \"affiliation\": {"
            "\n        \"company\": \"<Extracted industry company name or 'none' if not applicable>\","
            "\n        \"email\": \"<Extracted email address or 'none'>\""
            "\n      }"
            "\n    },"
            "\n    // ... other industry-oriented authors from the same paper"
            "\n  ]"
            "\n}"
            "\n\nConstraints:"
            "\n- Ensure the output is valid, strictly-formed JSON."
            "\n- Do not include any conversational text or explanations outside the JSON."
            "\n- For 'publication_date', provide it in 'YYYY-MM-DD' format if possible from the input."
            "\n- If an author is industry-oriented, but no specific company name can be extracted, use 'none' for 'company'."
            "\n- The 'authors' list for each paper in the output should ONLY contain industry-oriented authors."
            "\n- Emails should be valid email formats. If only partially captured, aim for the full valid email."
        )
        user_content = json.dumps(batch, ensure_ascii=False, indent=2)
        try:
            response = client.chat.completions.create(
                model="deepseek-r1-distill-llama-70b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                max_tokens=4000,
                temperature=0
            )
            raw = response.choices[0].message.content

            # Uncommed only if you want to debug the raw response
            # DebugUtil.debug_print(f"LLM batch response: {raw}")
            try:
                json_str = re.search(r'\[.*\]', raw, re.DOTALL).group(0)
                results = json.loads(json_str)
                matched_papers.extend(results)
            except Exception as e:
                DebugUtil.debug_print(f"Failed to parse LLM response: {e}", error=True)
                continue
        except Exception as e:
            DebugUtil.debug_print(f"Error during LLM API call: {e}", error=True)
            continue
        time.sleep(3)  # Throttle to stay under 30 requests/min

    DebugUtil.debug_print(f"Total matched papers: {len(matched_papers)}")
    return matched_papers