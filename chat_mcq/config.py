import os

from dotenv import load_dotenv

load_dotenv()

# Secret Key
SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))

# Openai API Key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Sqlalchemy DB
SQLALCHEMY_DATABASE_URI = "sqlite:///mcqs.db"

# Upload folder
UPLOAD_FOLDER = r"path/to/uploads"

# Data directory
DATA_DIR = r"path/to/data"

# Flask log level
FLASK_LOGLEVEL = "INFO"

# Flask log file
# FLASK_LOGFILE=

# Pinecone index name
PINECONE_INDEX_NAME = ""

# Model path where pre trained opensource model is stored
OPEN_SOURCE_PRETRAINED_MODEL_PATH = r"\model\llama-2-7b-chat.ggmlv3.q4_0.bin"
