import os, uuid
import streamlit as st
from tavily import TavilyClient
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

st.title("Research Assistant Agent")

@st.cache_resource
def build_agent():
    tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", max_retries=1, timeout=30)

    @tool
    def web_search(query: str) -> str:
        """Search the web for current information."""
        return str(tavily.search(query, max_results=3)["results"])

    @tool
    def save_report(title: str, content: str) -> str:
        """Save the final report to a file. Use only when research is complete."""
        with open(f"{title}.txt", "w") as f:
            f.write(content)
        return "Saved"

    return create_react_agent(
        llm, [web_search, save_report],
        prompt="Search the web, write a short report, then save it with save_report. Use a title with no spaces.",
        checkpointer=MemorySaver(),
    )

agent = build_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.thread = str(uuid.uuid4())

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

question = st.chat_input("Ask a research question")
if question:
    st.chat_message("user").write(question)
    st.session_state.messages.append({"role": "user", "content": question})
    with st.spinner("Researching..."):
        result = agent.invoke(
            {"messages": [("user", question)]},
            config={"configurable": {"thread_id": st.session_state.thread}, "recursion_limit": 10},
        )
    answer = result["messages"][-1].content
    if isinstance(answer, list):
        answer = "".join(c.get("text", "") for c in answer if isinstance(c, dict))
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
