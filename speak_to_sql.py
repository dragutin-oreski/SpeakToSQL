from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain_community.callbacks import StreamlitCallbackHandler
import streamlit as st

def get_user_input():
    """Prompt the user for necessary configurations."""
    open_ai_api_key = st.sidebar.text_input("Enter your OpenAI API key:", "")
    model_choice = st.sidebar.selectbox("Choose your ChatOpenAI model:", ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"], index=0)
    db_uri = st.sidebar.text_input("Enter your database URI:", "")
    return open_ai_api_key, model_choice, db_uri

def setup_agent(open_ai_api_key, model_choice, db_uri):
    """Setup the ChatGPT model, SQL database, and SQL agent."""
    llm = ChatOpenAI(model=model_choice, temperature=0, api_key=open_ai_api_key)
    db = SQLDatabase.from_uri(db_uri)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    return agent_executor

def main():
    """Main function to run the SpeakToSQL application."""
    st.title("SpeakToSQL")
    st.sidebar.subheader("Chat with Your Database")
    st.sidebar.image("logo.png")

    open_ai_api_key, model_choice, db_uri = get_user_input()

    # Proceed only if key and URI are provided
    if not open_ai_api_key and not db_uri:
        return   
    
    agent_executor = setup_agent(open_ai_api_key, model_choice, db_uri)
    query = st.text_area("Your question", "")
    st_callback = StreamlitCallbackHandler(st.container())

    if st.button("Submit"):
        if not query.strip():
            st.error("Please provide your question.")
        else:
            try:
                agent_executor.invoke({"input": query}, {"callbacks": [st_callback]})
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
