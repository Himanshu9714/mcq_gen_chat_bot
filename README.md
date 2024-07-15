# MCQs Creator and Chatbot Application

This application allows users to generate multiple-choice questions (MCQs) based on a provided text or PDF file using a generative AI model, and also features a chatbot for answering queries.

The backend is built with Flask, and the frontend is designed using HTML, CSS, and JavaScript.

## Features

- **MCQ Generation**: Users can upload a text or PDF file, specify the number of MCQs, subject, and complexity level, and generate MCQs.
- **Chatbot**: A chatbot interface where users can ask questions and receive answers.
- **Loader**: Display a loader while the MCQs are being generated.
- **MCQ Display**: Display generated MCQs on the same page with an option to download them as a CSV file.
- **Tabbed Interface**: Separate tabs for MCQ generation and the chatbot.

## Requirements

- Python 3.7+
- Flask
- Flask-Bootstrap
- Pre commit
- OpenAI
- Langchain
- LLama2
- HuggingFace
- Pinecone vector DB
- Werkzeug
- FontAwesome
- JavaScript (Fetch API)

## Installation

1. **Clone the Repository**
```
git clone https://github.com/yourusername/mcqs-creator-chatbot.git
cd mcqs-creator-chatbot
```

2. **Virtualenv setup**
```
# Create virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the pre-commit hooks
pre-commit install
```

3. **Environment credentials**

- Copy `.env.example` to `.env`
- Add the necessary credentials in the `.env`
- In the `DATA_TO_EXTRACT_DIR`, add the path for the folders where all the docs are present for the chatbot.

4. **Flask setup**
```
# On Windows
set FLASK_APP=chat_mcq.app:app

# On Linux
export FLASK_APP=chat_mcq.app:app

# Run the app
flask run
```

5. **Store the embeddings on the Pinecode vector database**

- Create the index on the Pinecone vector database.
- Run the script `script.py` to store the embeddings of the documents present in the DATA_TO_EXTRACT_DIR to Pinecone vector DB.

        python script.py
