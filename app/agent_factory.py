from __future__ import annotations

import logging
from langchain.agents import initialize_agent, AgentType, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from app.config import settings
from app.tools import calculator_tool, file_reader_tool, build_web_search_tool

logger = logging.getLogger(__name__)

REACT_PROMPT = PromptTemplate(
    input_variables=["input", "tools", "tool_names"],
    template=(
        "You are a tool-using assistant.\n"
        "Follow the format EXACTLY. No JSON. No code blocks.\n"
        "Use AT MOST 1 tool call unless absolutely required.\n\n"
        "TOOLS:\n{tools}\n\n"
        "FORMAT:\n"
        "Thought: short\n"
        "Action: one of [{tool_names}]\n"
        "Action Input: plain text\n"
        "Observation: tool output\n"
        "Final: answer in 2-4 lines\n\n"
        "User question: {input}\n"
    ),
)

def build_agent_executor() -> AgentExecutor:
    llm = ChatOllama(
        model=settings.model_name,     # llama3.2:3b
        temperature=settings.temperature,
    )

    tools = [
        calculator_tool,
        build_web_search_tool(use_mock=settings.use_mock_search),
        file_reader_tool,
    ]

    temp_executor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        prompt=REACT_PROMPT,
        verbose=True,
        handle_parsing_errors=True,
    )

    executor = AgentExecutor(
        agent=temp_executor.agent,
        tools=tools,
        verbose=True,
        max_iterations=3,                 # ✅ FAST
        early_stopping_method="generate", # ✅ always returns something
        return_intermediate_steps=False,
        handle_parsing_errors=True,
    )

    logger.info(
        "Agent configured (OFFLINE): model=%s | temp=%s | max_iterations=%s | mock_search=%s",
        settings.model_name,
        settings.temperature,
        3,
        settings.use_mock_search,
    )
    return executor
