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
