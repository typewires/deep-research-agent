import os
import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

# Setup: connect to Groq and Tavily
llm = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

#  Helper: send a prompt to the AI and get text back
def chat(prompt, temperature=0):
    r = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return r.choices[0].message.content.strip()
