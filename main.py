import os
import time
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from streamlit_chat import message as chat_message_box
from langchain.schema import (
    HumanMessage,
    AIMessage
)
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from helpers import clean_chat

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
ASSISTANT_NAME = "Alfredo 🐹"
clean_chat(st, ASSISTANT_NAME, "initialize")


def main():
    st.set_page_config(layout="wide")
    st.title("Vestibular Unicamp 2024 💬")
    chat_container = st.container()
    query = st.chat_input(f'Ask a question to {ASSISTANT_NAME}')

    if query:
        docs = st.session_state['knowledge_base'].similarity_search(query)
        llm = ChatOpenAI(model='gpt-3.5-turbo')
        st.session_state['chat_history'].append(HumanMessage(content=query))
        chain = load_qa_chain(llm, chain_type='stuff')

        with get_openai_callback() as callback:
            response = chain.run(input_documents=docs, question=st.session_state['chat_history'])
            current_timestamp = int(time.time())
            st.session_state['chat_history'].append(AIMessage(content=response))
            st.session_state['total_tokens'].append(callback.total_tokens)
            st.session_state['timestamp'].append(str(current_timestamp))
            st.session_state['cost'].append(callback.total_cost)
            st.session_state['total_cost'] += callback.total_cost

    if len(st.session_state['chat_history']) > 1:
        with chat_container:
            for index, message in enumerate(st.session_state['chat_history']):
                if message.type != "system":
                    chat_message_box(message.content, is_user=message.type == "human", key=f"{message.type}_{index}")
                if message.type == "ai":
                    st.text(f'timestamp: {st.session_state["timestamp"][(index // 2) - 1]}')

            st.text(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
            if st.button("Clear Chat", type="primary"):
                st.session_state['chat_history'] = []
                clean_chat(st, ASSISTANT_NAME, "reset")


if __name__ == "__main__":
    main()
