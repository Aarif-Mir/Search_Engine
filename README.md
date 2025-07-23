# LangChain Search Agent App

A Streamlit-powered conversational search assistant that leverages LangChain agents and multiple tools (DuckDuckGo, Arxiv, Wikipedia) to answer your questions with up-to-date information and research.

## Features
- **Conversational Chat UI:** Chat with an AI assistant that can search the web, Wikipedia, and Arxiv.
- **Tool Selection:** Choose which tools (Web Search, Arxiv, Wikipedia) to use for each query.
- **Model Selection:** Select from available Groq LLM models.
- **Prompt Suggestions:** Get started quickly with example prompts.
- **Session Management:** Reset chat history at any time.
- **Error Handling:** User-friendly error messages for missing API keys or agent errors.

## Setup

1. **Clone the repository** and navigate to this directory:
   ```bash
   git clone https://github.com/Aarif-Mir/Search_Engine
   cd Search_Engine 
   ```

2. **Install dependencies** (ideally in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**
   - Create a `.env` file in the project directory if you want to store API keys securely.
   - Or, enter your Groq API key in the Streamlit sidebar when prompted.

## Usage

1. **Run the app:**
   ```bash
   streamlit run app.py
   ```
2. **Open the app** in your browser (usually at http://localhost:8501).
3. **Enter your Groq API key** in the sidebar.
4. **Select your preferred LLM model and tools.**
5. **Start chatting!** Use the prompt suggestions or type your own questions.
6. **Reset the chat** at any time using the sidebar button.
