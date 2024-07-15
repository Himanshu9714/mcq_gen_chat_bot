import os

from dotenv import load_dotenv
from langchain.vectorstores import Pinecone as PC

from chat_mcq.utils.opensource_utils import download_hugging_face_embeddings
from chat_mcq.utils.opensource_utils import load_pdf
from chat_mcq.utils.opensource_utils import text_split

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
DATA_TO_EXTRACT_DIR = os.environ.get("DATA_TO_EXTRACT_DIR")

# Extract the data from the PDF source
extracted_data = load_pdf(DATA_TO_EXTRACT_DIR)

# Divides the data into chunks, so we can create the embeddings
text_chunks = text_split(extracted_data)

# Embeddings method for embedding
embeddings = download_hugging_face_embeddings()

# Pinecone index name
index_name = "chat-bot"

# Creating Embeddings for Each of The Text Chunks & storing
docsearch = PC.from_texts(
    [t.page_content for t in text_chunks], embeddings, index_name=index_name
)
