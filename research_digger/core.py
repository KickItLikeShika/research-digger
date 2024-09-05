import os
import time
from typing import List, Dict, Union

import backoff
import requests
from tqdm import tqdm

from research_digger.utils import on_backoff, extract_paper_info, create_prompt, process_stream

S2_API_KEY = os.getenv("S2_API_KEY")


@backoff.on_exception(
    backoff.expo, requests.exceptions.HTTPError, on_backoff=on_backoff
)
def search_for_papers(query: str, result_limit: int = 20) -> Union[None, List[Dict]]:
    """
    Search for papers using the Semantic Scholar API.

    Args:
        query (str): The search query string.
        result_limit (int): The maximum number of results to return. Default is 20.

    Returns:
        Union[None, List[Dict]]: A list of dictionaries containing paper information, or None if no results are found.
    """
    if not query:
        return None

    rsp = requests.get(
        "https://api.semanticscholar.org/graph/v1/paper/search",
        headers={"X-API-KEY": S2_API_KEY},
        params={
            "query": query,
            "limit": result_limit,
            "fields": "title,authors,venue,year,abstract,tldr",
        },
    )

    print(f"Response Status Code: {rsp.status_code}")
    print(
        f"Response Content: {rsp.text[:500]}"
    )  # Print the first 500 characters of the response content

    rsp.raise_for_status()
    results = rsp.json()

    total = results["total"]
    time.sleep(1.0)

    return None if not total else results["data"]


def generate_individual_summaries(papers: List[Dict], client, client_model: str, summary_length: str) -> List[str]:
    """
    Generate individual summaries for a list of papers.

    Args:
        papers (List[Dict]): A list of dictionaries containing paper information.
        client: The client object to interact with the language model.
        client_model (str): The model name to use for generating summaries.
        summary_length (str): The desired length of the summary ("short", "medium", or "long").

    Returns:
        List[str]: A list of summaries for each paper.
    """
    def generate_summary(paper: Dict) -> str:
        title, abstract, tldr = extract_paper_info(paper)
        prompt = create_prompt(title, abstract, tldr)
        stream = client.chat.completions.create(
            model=client_model,
            messages=[
                {"role": "system", "content": f"You are an academic researcher. You are given a paper and asked to summarize it. Follow a chain of thought process to ensure accuracy and completeness. First, identify the main points of the paper. Then, list the key findings. Finally, discuss the significance of these findings in the field. The summary length should be {summary_length}. Do not hallucinate or mention things that are not in the paper. Make sure the output looks like this: Title: <title of the paper>, then bullet points about what's in the paper."},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )
        return process_stream(stream)

    return [generate_summary(paper) for paper in tqdm(papers, total=len(papers))]


def generate_generic_summary(papers_summaries: List[str], client, client_model: str) -> str:
    """
    Generate a generic summary from individual paper summaries.

    Args:
        papers_summaries (List[str]): A list of individual paper summaries.
        client: The client object to interact with the language model.
        client_model (str): The model name to use for generating the generic summary.

    Returns:
        str: A single summary paragraph encapsulating all the main points and findings from the individual summaries.
    """
    prompt = f"""
    Here are the papers summaries:
    {papers_summaries}
    """

    generic_summary = client.chat.completions.create(
        model=client_model,
        messages=[
            {"role": "system", "content": "You are an academic researcher. You are given a list of papers and a summary of each one. Follow a chain of thought process to ensure accuracy and completeness. First, identify the main points of each paper summary. Then, list the key findings from each paper summary. Finally, ONLY produce a final single summary paragraph that encapsulates all the main points and findings from all the paper summaries. Do not hallucinate or mention things that are not in the summaries."},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )

    return process_stream(generic_summary)
