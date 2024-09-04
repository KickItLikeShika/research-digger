import time


def on_backoff(details):
    print(
        f"Backing off {details['wait']:0.1f} seconds after {details['tries']} tries "
        f"calling function {details['target'].__name__} at {time.strftime('%X')}"
    )


def save_summaries_to_md(individual_summaries, generic_summary, filename="summaries.md"):
    with open(filename, "w") as f:
        f.write(f"## Generic Summary\n")
        f.write(generic_summary)
        
        f.write("\n\n")
        
        f.write(f"## Individual Summaries\n")
        for i, summary in enumerate(individual_summaries):
            f.write(summary)
            f.write("\n\n")