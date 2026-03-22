# Deep Research Agent

An open-source implementation of the AI-powered deep research workflow popularized by [OpenAI's Deep Research](https://openai.com/index/introducing-deep-research/) and [Anthropic's Research feature for Claude](https://support.claude.com/en/articles/11088861-using-research-on-claude).

This project recreates the core research loop (query refinement, iterative web search, result evaluation, and report generation) using entirely free and open-source tools. This is a learning-oriented implementation. It's designed as a hands-on exploration of how these systems work under the hood, not as a full replacement for production-grade research products.

## How It Works

The agent uses four specialized AI "agents" working together in a loop:

1. **Query Rewriter** — Takes your natural language question and rewrites it into an optimized web search query
2. **Web Searcher** — Searches the internet using Tavily and returns clean article summaries
3. **Result Evaluator** — Reviews the research and decides if it adequately answers your question. If not, it identifies *what's missing* so the next search is targeted
4. **Report Writer** — Synthesizes all findings into a structured, sourced markdown report

If the evaluator finds gaps, it tells the query rewriter what's missing, which produces a more targeted follow-up search. This runs up to 3 times before writing the final report.

```
Question → Rewrite → Search → Evaluate → [Gap found?] → Rewrite again → Search again → ... → Write Report
```

## Tech Stack

| Component | Tool | Role |
|-----------|------|------|
| LLM | [Llama 3.3 70B](https://llama.meta.com/) via [Groq](https://groq.com/) | Powers all 4 agents (query rewriting, evaluation, report writing) |
| Search | [Tavily](https://tavily.com/) | Web search API built for AI agents. Returns clean text, not raw HTML. |
| UI | [Streamlit](https://streamlit.io/) | Turns the Python script into an interactive web app |

All three services offer free tiers. No credit card required to get started.

## Getting Your API Keys

You need two free API keys before setting up the project.

### Groq API Key (runs the AI model)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with Google or email
3. In the left sidebar, click **API Keys**
4. Click **Create API Key** and give it any name
5. Copy the key (starts with `gsk_`) — you only see it once

### Tavily API Key (runs the web searches)

1. Go to [tavily.com](https://tavily.com)
2. Sign up with Google or email
3. On the Dashboard, your API key is displayed (starts with `tvly-`)
4. Copy it

Save both keys somewhere safe. You'll need them in a few steps.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/typewires/deep-research-agent.git
cd deep-research-agent
```

### 2. Create a virtual environment

A virtual environment isolates this project's packages from the rest of your system.

```bash
# Mac/Linux
python3 -m venv venv

# Windows
python -m venv venv
```

### 3. Activate the virtual environment

```bash
# Mac/Linux
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate
```

You should see `(venv)` appear at the beginning of your terminal prompt. This means it's active.

> **Note:** You need to activate the virtual environment every time you open a new terminal session.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set your API keys

```bash
# Mac/Linux
export GROQ_API_KEY="gsk_paste_your_key_here"
export TAVILY_API_KEY="tvly-paste_your_key_here"

# Windows (PowerShell)
$env:GROQ_API_KEY="gsk_paste_your_key_here"
$env:TAVILY_API_KEY="tvly-paste_your_key_here"
```

> **Note:** These environment variables reset when you close your terminal. You'll need to export them again each session.

### 6. Run the app

```bash
streamlit run app.py
```

Your browser will open to `http://localhost:8501`. Type a research question, click **Research**, and watch the agent work.

Press `Ctrl+C` in the terminal to stop the app.

## Project Structure

```
deep-research-agent/
├── app.py               # Main application — all 4 agents + Streamlit UI
├── requirements.txt     # Python dependencies (pinned versions)
├── .gitignore           # Keeps venv/, __pycache__/, and .env out of git
└── README.md
```


## License

MIT

## Acknowledgments

- [Meta](https://llama.meta.com/) for the open-source Llama 3.3 model
- [Groq](https://groq.com/) for fast, free inference
- [Tavily](https://tavily.com/) for the AI-native search API
- [Streamlit](https://streamlit.io/) for the instant web UI framework
