from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import FAISS
from PyPDF2 import PdfReader
from langchain.schema import (
    SystemMessage,
)


def generate_knowledge_base():
    pdf_reader = PdfReader("./vestibular_unicamp_2024_infos.pdf")
    text = "".join(page.extract_text() for page in pdf_reader.pages)

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings()

    knowledge_base = FAISS.from_texts(chunks, embeddings)

    return knowledge_base


def clean_chat(st, assistant_name, action):
    if action == "initialize" and 'chat_history' not in st.session_state or action == "reset":
        st.session_state['knowledge_base'] = generate_knowledge_base()
        st.session_state['chat_history'] = [
            SystemMessage(content=f"Seu nome é {assistant_name}. Você é um assistente de futuros estudantes da unicamp que participarão do vestibular de 2024.")
        ]
        st.session_state['timestamp'] = []
        st.session_state['cost'] = []
        st.session_state['total_tokens'] = []
        st.session_state['total_cost'] = 0
