import json
import os
import traceback

import PyPDF2
from flask import current_app
from langchain.callbacks import get_openai_callback
from werkzeug.datastructures.file_storage import FileStorage

from .model.openai_model.mcq_generator import generate_evaluate_chain


def read_file(file: FileStorage):
    """
    Read the content of the uploaded file.

    Args:
        file (FileStorage): The uploaded file.

    Returns:
        str: The extracted text from the file.

    Raises:
        Exception: If there is an error reading the PDF file or the file format is unsupported.
    """
    if file.filename.endswith(".pdf"):
        try:
            # Read and extract text from the PDF file.
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

        except Exception as e:
            raise Exception("Error reading the PDF file")

    elif file.filename.endswith(".txt"):
        # Read and decode text from the text file.
        return file.read().decode("utf-8")

    else:
        raise Exception(
            "Unsupported file format. Only PDF and text files are supported."
        )


def get_table_data(quiz_str):
    """
    Convert the quiz string to a dictionary.

    Args:
        quiz_str (str): The quiz string in JSON format.

    Returns:
        dict: The quiz data as a dictionary.

    """
    try:
        # Convert the quiz from a string to a dictionary.
        quiz_dict = json.loads(quiz_str)
        return quiz_dict

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return {}


def generate_mcqs(
    file,
    mcq_count,
    subject,
    tone,
):
    """
    Generate MCQs from the provided file content.

    Args:
        file (FileStorage): The uploaded file.
        mcq_count (int): The number of MCQs to generate.
        subject (str): The subject of the MCQs.
        tone (str): The tone of the MCQs.

    Returns:
        dict: A response containing the generated MCQs, a message, a review, and a status code.
    """
    try:
        # Read the content of the file.
        text = read_file(file)

        # Load the response JSON from a file.
        response_json_file = os.path.join(
            current_app.config["DATA_DIR"], "response.json"
        )
        with open(response_json_file, "r") as file:
            response_json = json.load(file)

        # Count tokens and cost of the API call.
        with get_openai_callback() as cb:
            response = generate_evaluate_chain(
                {
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(response_json),
                }
            )
            current_app.logger.debug(
                f"Response for \ntext: {text}\nMCQ Count: {mcq_count}\nSubject: {subject}\nTone: {tone}\n\n\nResponse: {response}."
            )

    except Exception as e:
        # Handle exceptions and return an error response.
        traceback.print_exception(type(e), e, e.__traceback__)
        return {
            "data": {},
            "message": f"Error generating MCQs. Error is {str(e)}.",
            "review": "NA",
            "status_code": 400,
        }

    else:
        # Print token and cost details.
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost: {cb.total_cost}")

        if isinstance(response, dict):
            quiz = response.get("quiz", None)
            if not quiz:
                return {
                    "data": {},
                    "message": "Quiz wasn't generated!",
                    "review": "NA",
                    "status_code": 400,
                }

            quiz_dict = get_table_data(quiz)
            return {
                "data": quiz_dict,
                "message": "Quiz created successfully!",
                "review": response.get("review", ""),
                "status_code": 200,
            }
