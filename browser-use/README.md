# Browser-Use AI Agents

This repository contains a collection of AI agents that use the `browser-use` library to perform various web-based tasks. Each agent uses Azure OpenAI language models to interact with websites in an automated fashion.

https://github.com/browser-use/browser-use

## Setup

1. Copy `.env.sample` to `.env` and fill in your Azure OpenAI credentials:
   ```
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

We highly recommend `uv` instead of pip, for its speed and ease of use - https://docs.astral.sh/uv/

Example use for this project:
```bash
$ uv venv
$ source .venv/bin/activate
(browser-use) $ uv pip install -r requirements.txt
```

You'll need a vision enabled model like **GPT-4.1** or **GPT-4o** to use `use_vision=True` in the agent configuration.

## Sample Agents

### Elections Research ([elections.py](elections.py))

This agent researches the latest developments on the Romanian presidential elections from multiple reputable news sources. For each source, it:
1. Navigates to search functions to find recent articles (past week)
2. Extracts headlines, publication dates, and authors
3. Summarizes key points from each article
4. Synthesizes findings into a comprehensive summary, noting differences in reporting perspectives

### Puzzle Captcha Solver ([puzzlecaptcha.py](puzzlecaptcha.py))

This agent demonstrates the ability to solve puzzle captchas by:
- Visiting a specific CodePen page containing a puzzle captcha
- Using vision capabilities to analyze the puzzle
- Manipulating the browser to solve the sliding puzzle challenge

### Captcha Game Player ([captchagame.py](captchagame.py))

This agent plays the CAPTCHA game by:
- Visiting captchagame.com
- Using OCR capabilities to read distorted characters (which may be skewed, rotated, or otherwise mangled)
- Submitting the correct answers to progress through the game

## Usage

To run any of the agents, use:

```bash
python <script_name>.py
```

For example:
```bash
python elections.py
```

Each agent will open a browser window and perform its assigned task, generating a GIF of the interaction and printing the results to the console.
