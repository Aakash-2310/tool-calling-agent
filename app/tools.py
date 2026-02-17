from __future__ import annotations

import os
import requests
from langchain.tools import Tool


# ----------------
# Calculator tool
# ----------------
def calculator(expression: str) -> str:
    try:
        allowed = set("0123456789+-*/(). %")
        if any(c not in allowed for c in expression):
            return "Invalid expression (only numbers and + - * / ( ) . % allowed)."
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return f"Calculation error: {type(e).__name__}: {e}"


calculator_tool = Tool(
    name="calculator",
    func=calculator,
    description="Solve math expressions. Input: '3+4*(2-1)'.",
)


# ----------------
# File reader tool
# ----------------
def file_reader(path: str) -> str:
    try:
        if not os.path.exists(path):
            return "File not found."
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"File error: {type(e).__name__}: {e}"


file_reader_tool = Tool(
    name="file_reader",
    func=file_reader,
    description="Read a text file. Input: 'sample_files/notes.txt'.",
)


# ----------------
# Web search tool (FAST): Wikipedia summary
# ----------------
def build_web_search_tool(use_mock: bool = False) -> Tool:
    if use_mock:
        return Tool(
            name="web_search",
            func=lambda q: "",
            description="Mock web search (returns empty).",
        )

    def wiki_search(query: str) -> str:
        """
        Fast + reliable 'web search' using Wikipedia REST summary API.
        This avoids slow DDG scraping and prevents agent looping.
        """
        try:
            q = (query or "").strip()
            if not q:
                return "Empty query."

            # Clean common prefixes like "who is"
            lowered = q.lower()
            for prefix in ["who is ", "what is ", "tell me about "]:
                if lowered.startswith(prefix):
                    q = q[len(prefix):].strip()

            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(q)}"
            r = requests.get(url, timeout=8, headers={"User-Agent": "tool-calling-agent/1.0"})
            if r.status_code != 200:
                return f"No Wikipedia summary found for '{q}'."

            data = r.json()
            title = data.get("title", q)
            extract = data.get("extract", "")
            page = data.get("content_urls", {}).get("desktop", {}).get("page", "")

            if extract and len(extract) > 700:
                extract = extract[:700] + "..."

            return f"{title}\n{extract}\nSource: {page}"

        except Exception as e:
            return f"Search error: {type(e).__name__}: {e}"

    return Tool(
        name="web_search",
        func=wiki_search,
        description="Fast web search using Wikipedia summary. Input: query string.",
    )
