# Research Digger
Research Digger is an intelligent tool designed to streamline the process of academic research. 
By taking a research topic or area as input, Research Digger automatically fetches all relevant research papers from Semantic Scholar, analyzes their content, and provides concise, comprehensive summaries of the findings. 
This tool is ideal for researchers, students, and professionals who need to quickly grasp the key insights from large volumes of academic literature in a certain area.

Blog Post: https://kickitlikeshika.github.io/2024/09/05/research-digger.html

## How to Use the Project

### Prerequisites
1. **Python 3.7+**: Ensure you have Python 3.7 or higher installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

2. **Virtual Environment**: It is recommended to use a virtual environment to manage dependencies. You can create one using `venv` or `virtualenv`.

### Setting Up

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/KickItLikeShika/research-digger/tree/main
    cd research_digger
    ```

2. **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:
    ```sh
    source venv/bin/activate
    ```

4. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

### Configuration

1. **Set Up OpenAI API Key**:
    - You need an OpenAI API key to use the language model for generating summaries. Set the `OPENAI_API_KEY` environment variable:
    ```sh
    export OPENAI_API_KEY='your_openai_api_key'
    ```

2. **(Optional) Set Up Semantic Scholar API Key**:
    - If you want to fetch papers from Semantic Scholar, you can set the `S2_API_KEY` environment variable. This step is optional.
    ```sh
    export S2_API_KEY='your_semantic_scholar_api_key'
    ```

### Running the Research Digger

1. **Run the Script**:
    - You can run the main script with the following command:
    ```sh
    python launch_research_digger.py --research_area="Your Research Area" --papers_limit=20 --summary_length "short" --model "gpt-4o-mini"
    ```

    - **Arguments**:
        - `--research_area`: The research area to run Research Digger on.
        - `--papers_limit`: Limit of the number of papers returned from Semantic Scholar (default is 20).
        - `--summary_length`: Length of the summary to generate. Choices are `short`, `medium`, `long` (default is `short`).
        - `--model`: LLM to use for Research Digger. Choices are `gpt-4o`, `gpt-4o-mini` (default is `gpt-4o-mini`).

2. **Output**:
    - The script will generate individual summaries for each paper and a generic summary. The results will be saved in a file named `summaries.md`.

### Example Command
```sh
python research_digger/main.py --research_area "Natural Language Processing" --papers_limit 10 --summary_length "medium" --model "gpt-4o"
```

### Limitations and Future Work

1. **Model Support**:
    - Currently, Research Digger only supports OpenAI models (`gpt-4o` and `gpt-4o-mini`). This limits the flexibility for users who may prefer or have access to other language models. In future updates, we aim to support a wider range of models, including but not limited to models from other providers such as Hugging Face, Cohere, and custom-trained models.

2. **Dependency on API Keys and Commercial Models**:
    - The tool requires API keys for both OpenAI and Semantic Scholar. This dependency means that users must have valid API keys and may incur costs associated with API usage. Future versions could explore integrating with other free or open-access APIs to reduce this dependency.

3. **Error Handling**:
    - The current implementation has basic error handling, primarily raising exceptions when required arguments are missing or when API calls fail. More robust error handling and user-friendly messages could be added to improve the user experience.

4. **Customization Options**:
    - While the tool provides some customization options (e.g., summary length, model choice), there is room for more advanced customization. Future updates could include options for different summary styles, more detailed configuration of the summarization process, and user-defined templates for the output.

5. **Documentation and Examples**:
    - The current documentation provides basic instructions for setup and usage. More comprehensive documentation, including detailed examples, troubleshooting tips, and advanced usage scenarios, would be beneficial for users.

6. **User Interface**:
    - At present, Research Digger is a command-line tool. Developing a graphical user interface (GUI) or a web-based interface could make the tool more accessible to non-technical users.

By addressing these limitations in future updates, we aim to make Research Digger a more versatile, user-friendly, and powerful tool for academic research and summarization tasks.

### Contributing

We welcome contributions from the community to help improve Research Digger. Whether it's fixing bugs, adding new features, improving documentation, or providing feedback, your contributions are highly valued.

If you have any feedback or suggestions, feel free to open an issue on GitHub. We appreciate your input and look forward to your contributions.
