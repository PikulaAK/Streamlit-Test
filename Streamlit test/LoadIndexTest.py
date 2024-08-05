import streamlit as st
import os
import pickle
import asyncio

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama

def save_uploadedfile(uploadedfile):
    with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{} to tempDir".format(uploadedfile.name))

def initialize_chat():
    print('start initial')
    # ollama
    Settings.llm = Ollama(
        model="llama3.1", 
        base_url="http://localhost:11434",
        request_timeout=360.0)
    
def Index():
    with st.sidebar:
        load_name = st.query_params.get("load")
        if load_name is None:
            st.write("No filename provided")
        else:
            load_direcory = str(load_name) + ".pkl"
            #save_uploadedfile(load_direcory)
            st.write("Loading index file...")
            file_path = r"Index Files\\" + load_direcory
            index = load_index_from_file(file_path)
            st.write("Loaded index file")
            st.session_state.chat_engine_mem = index.as_chat_engine(
            chat_mode="condense_plus_context" #, streaming=True, 
            )
        initialize_chat() 
        #index = VectorStoreIndex.from_documents(documents,)    
        #print (documents)
        prompt = ""

def load_index_from_file(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)
    
####Left Side Bar###
with st.sidebar:
    with st.expander("Prompts"):
        qa_prompt_template = st.text_area("QA Prompt", height=300,  key="qa_prompt_template",value="")    

def reset_conversation():
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]
    st.session_state.chat_history = '[]'
    st.session_state.chat_engine_mem.reset()

async def chat_stream_api():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])  
    if user_query := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)
        with st.spinner("preparing your information."):
            # Display chatbot response in Streamlit chat UI
            with st.chat_message('assistant'):
                # Get chatbot response
                streaming_response = st.session_state.chat_engine_mem.stream_chat(user_query)
                st.write_stream(streaming_response.response_gen)
                st.session_state.messages.append({"role": "assistant", "content": streaming_response.response})
            
    st.button('New Conversation', on_click=reset_conversation)            
st.empty()    
st.caption("🚀 To infinity and beyond.")

if __name__ == "__main__":  
    if "chat_engine_mem" not in st.session_state: 
        print ("doc not in")
        initialize_chat()
    
    asyncio.run (chat_stream_api())

    
Index()