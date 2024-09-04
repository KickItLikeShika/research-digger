import os
import time
from typing import List, Dict, Union

import backoff
import requests
from tqdm import tqdm

from research_digger.utils import on_backoff

S2_API_KEY = os.getenv("S2_API_KEY")


@backoff.on_exception(
    backoff.expo, requests.exceptions.HTTPError, on_backoff=on_backoff
)
def search_for_papers(query, result_limit=20) -> Union[None, List[Dict]]:
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


def generate_individual_summaries(papers, client, client_model, summary_length):
    summaries = []
    
    for paper in tqdm(papers, total=len(papers)):

        title = paper.get("title", "")
        if not title:
            print("Missing key: title")

        abstract = paper.get("abstract", "")
        if not abstract:
            print("Missing key: abstract")

        tldr = paper.get("tldr", {})
        if not tldr:
            print("Missing key: tldr")
        else: 
            tldr = tldr.get("text", "")

        prompt = f"""
        Title: {title}
        Abstract: {abstract}
        Quick Summary: {tldr}
        """

        # print(f"Prompt: {prompt}")

        stream = client.chat.completions.create(
            model=client_model,
            messages=[
                # {"role": "system", "content": "You are an academic researcher. You are given a paper and asked to summarize it. Do not hallucinate or mention things that are not in the paper. Make sure the output looks like this: Title: {title of the paper}, then bullet points about what's in the paper."},
                {"role": "system", "content": f"You are an academic researcher. You are given a paper and asked to summarize it. Follow a chain of thought process to ensure accuracy and completeness. First, identify the main points of the paper. Then, list the key findings. Finally, discuss the significance of these findings in the field. The summary length should be {summary_length}. Do not hallucinate or mention things that are not in the paper. Make sure the output looks like this: Title: <title of the paper>, then bullet points about what's in the paper."},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )

        summary = []
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                summary.append(chunk.choices[0].delta.content)
        # print(f"Summary: {summary}")
        summaries.append("".join(summary).strip())

    return summaries


def generate_generic_summary(papers_summaries, client, client_model):
    prompt = f"""
    Here are the papers summaries:
    {papers_summaries}
    """

    generic_summary = client.chat.completions.create(
        model=client_model,
        messages=[
            # {"role": "system", "content": "You are an academic researcher. You are given a list of papers and a summary of each one. Your task is to produce a final single summary paragraph that encapsulates the main points and findings from all the paper summaries. Do not hallucinate or mention things that are not in the summaries."},
            {"role": "system", "content": "You are an academic researcher. You are given a list of papers and a summary of each one. Follow a chain of thought process to ensure accuracy and completeness. First, identify the main points of each paper summary. Then, list the key findings from each paper summary. Finally, ONLY produce a final single summary paragraph that encapsulates all the main points and findings from all the paper summaries. Do not hallucinate or mention things that are not in the summaries."},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )

    summary = []    
    for chunk in generic_summary:
        if chunk.choices[0].delta.content is not None:
            summary.append(chunk.choices[0].delta.content)

    return "".join(summary).strip()

