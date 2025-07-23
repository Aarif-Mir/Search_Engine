import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Tool Setup ---
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)

search = DuckDuckGoSearchRun(name="Search")

# --- UI ---
st.title("🔎 LangChain - Chat with search")

# Sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

# Model selection
model_options = ["Llama3-8b-8192", "Gemma2-9b-it"]
selected_model = st.sidebar.selectbox("Select Groq Model", model_options)

# Tool selection
tool_options = {
    "Web Search (DuckDuckGo)": search,
    "Arxiv": arxiv,
    "Wikipedia": wiki
}

selected_tools = st.sidebar.multiselect(
    "Select tools to use:", list(tool_options.keys()), default=list(tool_options.keys())
)
tools = [tool_options[name] for name in selected_tools]

# Prompt suggestions
suggestions = [
    "What is machine learning?",
    "Summarize the latest research on quantum computing.",
    "Who won the Nobel Prize in Physics in 2023?",
    "Find recent papers about transformers in NLP.",
    "Tell me about the history of the internet."
]

st.sidebar.markdown("**Prompt Suggestions:**")
for s in suggestions:
    if st.sidebar.button(s, key=s):
        st.session_state["suggested_prompt"] = s

# --- Chat State Management ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

# Reset chat button
if st.sidebar.button("Reset Chat"):
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]
    st.experimental_rerun()

# Display chat history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Get prompt (from suggestion or user input)
def get_prompt():
    if "suggested_prompt" in st.session_state:
        prompt = st.session_state["suggested_prompt"]
        del st.session_state["suggested_prompt"]
        return prompt
    return st.chat_input(placeholder="Ask me anything...")

prompt = get_prompt()

# --- Main Chat Logic ---
if prompt:
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar.")
    elif not tools:
        st.warning("Please select at least one tool in the sidebar.")
    else:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        llm = ChatGroq(groq_api_key=api_key, model_name=selected_model, streaming=True)
        search_agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handling_parsing_errors=True
        )

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        with st.spinner("Searching and thinking..."):
            try:
                response = search_agent.run(st.session_state["messages"], callbacks=[st_cb])
                st.session_state["messages"].append({'role': 'assistant', "content": response})
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")

