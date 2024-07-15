import time

from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import request

from ..model.llama_model.llama_qa import get_qa_object

# Create a Blueprint named 'question_answer'
question_answer = Blueprint("question_answer", __name__)


@question_answer.route("/chat")
def index():
    """
    Renders the chat.html template.

    This function is responsible for handling the route '/chat' and rendering
    the chat interface.

    Returns:
        str: The rendered HTML template for the chat interface.
    """
    return render_template("chat.html")


@question_answer.route("/chat/get", methods=["GET", "POST"])
def chat():
    """
    Processes a chat message and returns the response from the QA system.

    This function handles the route '/chat/get' and processes a chat message
    received via a form. It utilizes the QA system to get a response and logs
    the time taken for the process.

    Methods:
        GET, POST: Accepts both GET and POST requests.

    Returns:
        str: The response from the QA system.
    """
    # Extract the message from the form
    msg = request.form["msg"]

    # Get the QA object for processing the query
    qa = get_qa_object()

    # Record the start time for processing the query
    start_time = time.time()

    # Log the received query
    current_app.logger.info(f"Query received: {msg}")

    # Process the query using the QA system
    result = qa({"query": msg})

    # Record the end time after processing the query
    end_time = time.time()

    # Log the time taken to process the query and the result
    current_app.logger.info(
        f"{round(end_time - start_time, 2)}s time taken to process the output: {result['result']}"
    )

    # Return the result from the QA system as a string
    return str(result["result"])
