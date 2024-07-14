import json
import os
import traceback

import PyPDF2
from flask import current_app
from langchain.callbacks import get_openai_callback
from werkzeug.datastructures.file_storage import FileStorage

from .model.openai_model.mcq_generator import generate_evaluate_chain


def read_file(file: FileStorage):
    if file.filename.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

        except Exception as e:
            raise Exception("error reading the PDF file")

    elif file.filename.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception("unsupported file format only pdf and text file suppoted")


def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
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
    try:
        text = read_file(file)
        response_json_file = os.path.join(
            current_app.config["DATA_DIR"], "response.json"
        )
        with open(response_json_file, "r") as file:
            response_json = json.load(file)

        # Count tokens and cost of the API call
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
        traceback.print_exception(type(e), e, e.__traceback__)
        return {
            "data": {},
            "message": f"Error generating MCQS. Error is {str(e)}.",
            "review": "NA",
            "status_code": 400,
        }

    else:
        print(f"Total Tokens:{cb.total_tokens}")
        print(f"Prompt Tokens:{cb.prompt_tokens}")
        print(f"Completion Tokens:{cb.completion_tokens}")
        print(f"Total Cost:{cb.total_cost}")

        if isinstance(response, dict):
            quiz = response.get("quiz", None)
            if not quiz:
                return {
                    "data": {},
                    "message": "Quiz doesn't gets generated!",
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
