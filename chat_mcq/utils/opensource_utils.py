from flask import current_app
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import CTransformers
from langchain_community.vectorstores import Pinecone as PC

# Opensource model to generate the embeddings
EMBEDDINGS_OPEN_SOURCE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Template for generating responses using the provided context and question
prompt_template = """
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""


def load_pdf(data):
    """
    Extracts data from PDF files located in the specified directory.

    Args:
        data (str): The directory path where the PDF files are located.

    Returns:
        list: A list of documents extracted from the PDF files.
    """
    # Initialize the DirectoryLoader with the directory and PDF loader class
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)

    # Load the documents from the specified directory
    documents = loader.load()

    return documents


def text_split(extracted_data):
    """
    Splits the extracted text data into smaller chunks for processing.

    Args:
        extracted_data (list): The list of extracted documents.

    Returns:
        list: A list of text chunks.
    """
    # Initialize the text splitter with chunk size and overlap settings
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)

    # Split the documents into text chunks
    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks


def download_hugging_face_embeddings():
    """
    Downloads the Hugging Face embeddings model.

    Returns:
        HuggingFaceEmbeddings: The Hugging Face embeddings model.
    """
    # Initialize and return the Hugging Face embeddings model
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_OPEN_SOURCE_MODEL)
    return embeddings


def get_qa_object():
    """
    Creates and returns a QA object for processing questions and answers.

    This function downloads the embeddings model, retrieves the Pinecone index,
    and initializes the QA object using the specified LLM and prompt template.

    Returns:
        RetrievalQA: The QA object for processing questions and answers.
    """
    # Download the embeddings from the Hugging Face open-source model
    embeddings = download_hugging_face_embeddings()

    # Get the Pinecone index name from the application configuration
    index_name = current_app.config["PINECONE_INDEX_NAME"]

    # Load the Pinecone index using the embeddings
    docsearch = PC.from_existing_index(index_name, embeddings)

    # Create the prompt template for the QA system
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # Initialize the LLM using CTransformers for CPU environment
    llm = CTransformers(
        model=current_app.config["OPEN_SOURCE_PRETRAINED_MODEL_PATH"],
        model_type="llama",
        config={"max_new_tokens": 1024, "temperature": 0.8},
    )

    # Create the QA object using the LLM and retriever
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
    )

    return qa
