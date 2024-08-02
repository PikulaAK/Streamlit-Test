import streamlit as st
import os
import pickle
import random

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.ollama import OllamaEmbedding



def save_index_to_file(index, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(index, f)
        

def Document():
    with st.form("Document_Form"):
        DocumentDirectory = st.file_uploader("Choose document(s)",type=['pdf','txt'])
        #IndexDirectory = st.text_input("Directory to save index file")
        submitted = st.form_submit_button("Index")
        if submitted:
            file_details = {"FileName":DocumentDirectory.name,"FileType":DocumentDirectory.type}
            st.write(file_details)
            save_uploadedfile(DocumentDirectory)
            st.write("Reading Documents...")
            documents = SimpleDirectoryReader("tempDir").load_data()
            #documents

            index_file_name = ''.join(str(random.randint(0, 9)) for _ in range(5))

            index_file_path = r"Index Files\\" + index_file_name + r".pkl"

            Settings.embed_model = OllamaEmbedding(
                model_name="nomic-embed-text",
                base_url="http://localhost:11434",
                ollama_additional_kwargs={"mirostat": 0},
            )

            #vectorize the documents
            st.write("Vectorizing Documents...")
            index = VectorStoreIndex.from_documents(
                documents,
            )

            # Save the index to a file
            st.write("Saving index file...\n")
            save_index_to_file(index, index_file_path)
            st.write("Saved index file successfuly")
            os.remove("tempDir\\"+DocumentDirectory.name)

def save_uploadedfile(uploadedfile):
    with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{} to tempDir".format(uploadedfile.name))




# DocOrIndex()
Document()