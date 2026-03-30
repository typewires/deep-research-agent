import os
import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

# --- Setup ---
llm = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


# --- Helper: send a prompt to the AI and get text back ---
def chat(prompt, temperature=0):
    r = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return r.choices[0].message.content.strip()


# --- Agent 1: Turn a vague question into a good search query ---
def rewrite_query(question, gap=None):
    if gap:
        return chat(f"""Turn this research question into search engine keywords (3-10 words).
Add the current year if the topic is time-sensitive.
Previous search was missing: {gap}
Adjust the keywords to fill that gap.

Original question: {question}
Rewritten question:""")

    return chat(f"""Turn this research question into search engine keywords (3-10 words).
Add the current year if the topic is time-sensitive.
If it's already specific, keep it as-is.

Original question: {question}
Rewritten question:""")


# --- Agent 2: Search the web ---
def search_web(query):
    response = tavily.search(query=query, max_results=5)
    return response["results"]


# --- Agent 3: Check if the results answer the question ---
def evaluate_results(question, results):
    all_text = "\n\n".join(r["content"] for r in results)

    answer = chat(f"""Does this research adequately answer the question?
- If YES: respond with just YES
- If NO: describe what specific information is still missing (do not write NO)

Question: {question}

Research:
{all_text}""")

    if answer.upper().startswith("YES"):
        return True, None

    return False, answer


# --- Agent 4: Write the final report ---
def write_report(question, all_results):
    sources = "\n".join(f"- {r['title']}: {r['url']}" for r in all_results)
    content = "\n\n".join(r["content"] for r in all_results)

    return chat(f"""Write a clear research report in markdown.
Use ## headings and bold key terms. Keep it under 500 words.
Be specific. Use numbers, dates, and names from the research.
End with a ## Sources section.

Question: {question}

Research:
{content}

Sources:
{sources}""", temperature=0.3)


# --- Web Page ---
st.set_page_config(page_title="Deep Research Agent", page_icon="🔍")
st.title("Deep Research Agent")
st.caption("Powered by Llama 3.3 70B via Groq + Tavily")

question = st.text_input(
    "What do you want to research?",
    placeholder="e.g. What is the current state of nuclear fusion energy?",
)

if st.button("Research", type="primary") and question:

    # Step 1: Rewrite the query
    with st.spinner("Rewriting your query..."):
        query = rewrite_query(question)
        st.info(f"Searching for: {query}")

    # Step 2: Search up to 3 times until results are good enough
    all_results = []
    satisfied = False
    gap = None

    attempt = 1
    while not satisfied and attempt <= 3:

        with st.spinner(f"Searching the web (attempt {attempt}/3)..."):
            all_results = all_results + search_web(query)

        with st.spinner("Checking if results are good enough..."):
            satisfied, gap = evaluate_results(question, all_results)

        if satisfied:
            st.success("Found enough information!")

        elif attempt < 3:
            st.warning(f"Missing: {gap}")
            with st.spinner("Rewriting query to find what's missing..."):
                query = rewrite_query(question, gap=gap)
                st.info(f"New search: {query}")

        attempt = attempt + 1

    if not satisfied:
        st.warning("Used all 3 attempts. Writing with what was found...")

    # Step 3: Write the report
    with st.spinner("Writing your report..."):
        report = write_report(question, all_results)

    st.divider()
    st.markdown(report)

    with st.expander("Click to see all sources"):
        for r in all_results:
            st.markdown(f"**{r['title']}**  \n{r['url']}")