import logging

from app.logging_config import setup_logging
from app.agent_factory import build_agent_executor
from app.tools import build_web_search_tool, file_reader_tool


def main():

    setup_logging(logging.INFO)

    executor = build_agent_executor()

    web_search_tool = build_web_search_tool(use_mock=False)

    print("\nAgent Ready (OFFLINE). Type your task. Type 'exit' to quit.\n")

    while True:

        query = input("You: ").strip()

        if query.lower() in {"exit", "quit"}:

            print("Bye!")
            break

        try:

            # -----------------
            # FORCE WEB SEARCH
            # -----------------

            if query.lower().startswith("search "):

                q = query[len("search "):]

                results = web_search_tool.func(q)

                prompt = f"""
Use ONLY this information to answer.

{results}

Explain in detail.
"""

                out = executor.invoke({"input": prompt})

                print("\nAssistant:", out["output"], "\n")

                continue


            # -----------------
            # FORCE FILE READ
            # -----------------

            if query.lower().startswith("read "):

                path = query[len("read "):]

                content = file_reader_tool.func(path)

                print("\nAssistant:\n")

                print(content)

                print()

                continue


            # -----------------
            # FORCE SUMMARY
            # -----------------

            if query.lower().startswith("summarize "):

                path = query[len("summarize "):]

                content = file_reader_tool.func(path)

                prompt = f"""
Summarize this file content:

{content}
"""

                out = executor.invoke({"input": prompt})

                print("\nAssistant:", out["output"], "\n")

                continue


            # -----------------
            # NORMAL AGENT
            # -----------------

            out = executor.invoke({"input": query})

            print("\nAssistant:", out["output"], "\n")


        except Exception as e:

            print("\nError:", str(e))


if __name__ == "__main__":

    main()
