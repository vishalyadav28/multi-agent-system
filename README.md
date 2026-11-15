# 🔎 Multi-Agent Research Assistant

A multi-agent AI system that researches any topic on the web, reads the best sources, writes a structured report, and then critiques its own work, all from a ChatGPT-style Streamlit chat UI with live streaming responses.

Built with **LangChain**, **Ollama**, **Tavily**, and **Streamlit**.

---

## ✨ How it works

Four specialised agents work together in a pipeline, each passing its output to the next:

```mermaid
flowchart LR
    U([🧑 User topic]) --> S[🔍 Search Agent<br/><sub>Tavily web search</sub>]
    S --> R[📖 Reader Agent<br/><sub>scrapes best URL</sub>]
    R --> W[✍️ Writer<br/><sub>drafts report</sub>]
    W --> C[🧐 Critic<br/><sub>scores & reviews</sub>]
    C --> O([📄 Report + Feedback])
```

| Step | Component | What it does |
|------|-----------|--------------|
| 1 | **Search Agent** | Uses the `web_search` tool (Tavily) to find recent, reliable information on the topic |
| 2 | **Reader Agent** | Picks the most relevant URL from the search results and scrapes it with `scrape_url` for deeper content |
| 3 | **Writer Chain** | Combines search results and scraped content into a structured report: Introduction, Key Findings, Conclusion, Sources |
| 4 | **Critic Chain** | Reviews the report and returns a score out of 10, strengths, areas to improve, and a one-line verdict |

The search and reader steps are **tool-using agents** (`create_agent`), so the LLM decides how to call its tool. The writer and critic are **prompt chains** (`prompt | llm | parser`).

### Robust web scraping

`scrape_url` tries three extraction strategies in turn, so it still gets text from pages that one method can't parse:

1. **trafilatura**: best for articles and blogs
2. **readability-lxml**: pulls out the main content block
3. **BeautifulSoup**: falls back to the full page text, with nav, header, footer and scripts stripped out

---

## 🛠️ Tech stack

| Layer | Tools |
|-------|-------|
| Agents & chains | [LangChain](https://python.langchain.com/) |
| LLM | [Ollama](https://ollama.com/) (`llama3.2:3b`, runs fully locally; any Ollama model works) |
| Web search | [Tavily](https://tavily.com/) |
| Scraping | trafilatura, readability-lxml, BeautifulSoup |
| Frontend | [Streamlit](https://streamlit.io/) |
| Language | Python 3.12 |

---

## 📁 Project structure

```
multi-agents/
├── src/
│   ├── agent/
│   │   └── agents.py        # LLM setup, search & reader agents, writer & critic chains
│   ├── pipelines/
│   │   └── pipeline.py      # gather_research() (steps 1-2) + run_research_pipeline() (all 4 steps)
│   ├── tools/
│   │   └── tools.py         # web_search (Tavily) and scrape_url tools
│   ├── app.py               # Streamlit chat UI (streams the report + critique)
│   └── main.py              # CLI entry point for quick testing
├── pyproject.toml           # makes `src` an installable package
├── requirements.txt
└── .env                     # API keys (not committed)
```

---

## 🚀 Getting started

### Prerequisites

- Python 3.12+
- [Ollama](https://ollama.com/download) installed and running
- A free [Tavily API key](https://app.tavily.com/)

### 1. Clone and install

```bash
git clone https://github.com/vishalyadav28/multi-agent-system.git
cd multi-agent-system

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # also installs this project in editable mode
```

### 2. Set up the model

```bash
ollama pull llama3.2:3b
```

> To use a different model, change the `model=` value in `src/agent/agents.py`. Models ending in `-cloud` (e.g. `gemma4:31b-cloud`) run on Ollama's servers, not your machine: they need `ollama signin` and Ollama usage credits (otherwise you get a `402` error).

### 3. Add your API key

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key
```

### 4. Run

**Streamlit UI**

```bash
streamlit run src/app.py
```

Open http://localhost:8501 and type a topic in the chat box.

- A status box shows live progress while the search and reader agents work (~1 min).
- The report then **streams in word by word**, followed by the critic's feedback.
- Search results and scraped content are available in expandable sections under each answer.

#### How streaming works

The writer and critic are LangChain chains, so they support `.stream()` (yields text chunks) as well as `.invoke()` (returns the full text at the end). The app passes the stream to `st.write_stream()`, which renders chunks as they arrive and returns the full text:

```python
state = gather_research(topic)   # steps 1-2: agents (tool calls, not streamed)
report = st.write_stream(writer_chain.stream({"topic": topic, "research": state["research"]}))
feedback = st.write_stream(critic_chain.stream({"report": report}))
```

**Command line**

```bash
python src/main.py
```

---

## 🧩 Using the tools directly

The tools are LangChain `StructuredTool`s, so call them with `.invoke()`:

```python
from src.tools.tools import web_search, scrape_url

web_search.invoke({"query": "latest news on AI agents"})
scrape_url.invoke({"url": "https://example.com/article"})
```

Or run the whole pipeline from Python:

```python
from src.pipelines.pipeline import run_research_pipeline

state = run_research_pipeline("Impact of AI on jobs")
print(state["report"])
print(state["feedback"])
```

---

## 🗺️ Roadmap

- [ ] Feed the critic's feedback back to the writer (self-improvement loop)
- [ ] Scrape multiple sources instead of one
- [x] Stream the report and critique live in a chat UI
- [ ] Expose the pipeline as a FastAPI endpoint
- [ ] Export reports as PDF / Markdown

---

## 🙌 Acknowledgements

Built while learning multi-agent systems with LangChain. Feedback and suggestions are welcome.
