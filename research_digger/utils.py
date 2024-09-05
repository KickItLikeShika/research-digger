import time


def on_backoff(details: dict) -> None:
    """
    Print a backoff message with details about the retry attempt.

    Args:
        details (dict): A dictionary containing details about the retry attempt.
    """
    print(
        f"Backing off {details['wait']:0.1f} seconds after {details['tries']} tries "
        f"calling function {details['target'].__name__} at {time.strftime('%X')}\n"
        f"Please use Semantic Scholar API Key if available to avoid this"
    )


def extract_paper_info(paper: dict) -> tuple:
    """
    Extract the title, abstract, and TLDR from a paper dictionary.

    Args:
        paper (dict): A dictionary containing paper information.

    Returns:
        tuple: A tuple containing the title, abstract, and TLDR of the paper.
    """
    title = paper.get("title", "")
    abstract = paper.get("abstract", "")

    tldr = paper.get("tldr", {})
    if tldr:
        tldr = tldr.get("text", "")

    return title, abstract, tldr


def create_prompt(title: str, abstract: str, tldr: str) -> str:
    """
    Create a prompt string using the title, abstract, and TLDR of a paper.

    Args:
        title (str): The title of the paper.
        abstract (str): The abstract of the paper.
        tldr (str): The TLDR (Too Long; Didn't Read) summary of the paper.

    Returns:
        str: A formatted prompt string.
    """
    return f"""
    Title: {title}
    Abstract: {abstract}
    Quick Summary: {tldr}
    """


def process_stream(stream) -> str:
    """
    Process a stream of data to generate a summary string.

    Args:
        stream: A stream of data chunks.

    Returns:
        str: A concatenated summary string.
    """
    summary = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            summary.append(chunk.choices[0].delta.content)
    return "".join(summary).strip()


def save_summaries_to_md(individual_summaries: list, generic_summary: str, filename: str = "summaries.md") -> None:
    """
    Save individual and generic summaries to a markdown file.

    Args:
        individual_summaries (list): A list of individual paper summaries.
        generic_summary (str): A generic summary encapsulating all the main points and findings.
        filename (str): The name of the file to save the summaries to. Default is "summaries.md".
    """
    with open(filename, "w") as f:
        f.write(f"## Generic Summary\n")
        f.write(generic_summary)
        
        f.write("\n\n")
        
        f.write(f"## Individual Summaries\n")
        for i, summary in enumerate(individual_summaries):
            f.write(summary)
            f.write("\n\n")