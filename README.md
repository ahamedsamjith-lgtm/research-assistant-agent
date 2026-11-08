# Research Assistant Agent

An AI agent that searches the web, writes a short research report, saves it as a file, and remembers follow-up questions.

## Features
- Web search tool (Tavily)
- Save-report tool (writes a .txt file)
- Follow-up memory (LangGraph MemorySaver)
- Step limit of 10 so the agent never loops forever
- Chat interface built with Streamlit

## Tech stack
Python, LangGraph, LangChain, Gemini, Tavily, Streamlit

## How to run
1. pip install -r requirements.txt
2. Get a free Gemini key (aistudio.google.com) and a free Tavily key (tavily.com)
3. Set them as environment variables: GOOGLE_API_KEY and TAVILY_API_KEY
4. streamlit run app.py

## Example
Ask: "Research the latest trends in agentic AI"
Follow up: "Which of those is best for beginners?"

Built by Ahamed Samjith Z
