import argparse

from research_digger.core import search_for_papers, generate_individual_summaries, generate_generic_summary
from research_digger.utils import save_summaries_to_md


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Research Digger")

    parser.add_argument(
        "--research_area",
        type=str,
        help="Research area to run Research Digger on."
    )

    parser.add_argument(
        "--papers_limit",
        type=int,
        default=20,
        help="Limit of number of papers returned from Semantic Scholar."
    )
    
    parser.add_argument(
        "--summary_length",
        type=str,
        default="short",
        choices=["short", "medium", "long"],
        help="Length of the summary to generate."
    )

    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini",
        choices=[
            "gpt-4o",
            "gpt-4o-mini"
        ],
        help="LLM to use for Research Digger."
    )

    args = parser.parse_args()

    if args.model == "gpt-4o":
        import openai

        print(f"Using OpenAI API with model {args.model}.")

        client_model = "gpt-4o"
        client = openai.OpenAI()

    elif args.model == "gpt-4o-mini":
        import openai

        print(f"Using OpenAI API with model {args.model}.")

        client_model = "gpt-4o-mini"
        client = openai.OpenAI()

    else:
        raise ValueError(f"Model {args.model} not supported.")


    if args.research_area is None:
        raise ValueError("Research area is required.")

    papers = search_for_papers(args.research_area, args.papers_limit)

    print(f"Generating individual summaries for {len(papers)} papers...")
    individual_summaries = generate_individual_summaries(papers, client, client_model, args.summary_length)

    print(f"Generating generic summary...")
    generic_summary = generate_generic_summary(individual_summaries, client, client_model)

    save_summaries_to_md(individual_summaries, generic_summary, filename=f"summaries.md")
