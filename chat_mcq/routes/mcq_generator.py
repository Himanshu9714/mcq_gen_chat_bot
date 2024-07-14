import csv
import json
import os

from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import request
from flask import send_file
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import MCQ
from ..utils import generate_mcqs

mcq_generator = Blueprint("mcq_generator", __name__)


@mcq_generator.route("/generate_mcqs", methods=["POST"])
def generate_mcqs_route():
    """
    Handle the route for generating MCQs from an uploaded file.

    This route accepts a file upload and form data to generate a specified number of MCQs
    based on the subject and complexity provided. The generated MCQs are stored in the database.

    Returns:
        JSON: A response containing the generated MCQs and a status code.
    """
    # Retrieve the file and form data from the request.
    file = request.files["file"]
    num_mcqs = int(request.form["num_mcqs"])
    subject = request.form["subject"]
    complexity = request.form["complexity"]

    # Secure the filename and save the file to the upload folder.
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Generate MCQs using the utility function.
    response = generate_mcqs(
        file,
        num_mcqs,
        subject,
        complexity,
    )

    # If the MCQs were generated successfully, save them to the database.
    if response["status_code"] == 200:
        mcqs = response["data"]
        review = response["review"]
        mcq_entry = MCQ(mcqs=json.dumps(mcqs), review=review)
        db.session.add(mcq_entry)
        db.session.commit()

    return jsonify(response)


@mcq_generator.route("/download/<int:mcq_id>")
def download(mcq_id):
    """
    Handle the route for downloading MCQs as a CSV file.

    This route retrieves the MCQs from the database based on the provided MCQ ID
    and generates a CSV file for download.

    Args:
        mcq_id (int): The ID of the MCQ entry in the database.

    Returns:
        Response: A Flask response object to send the CSV file as an attachment.
    """
    # Retrieve the MCQ entry from the database.
    mcq_entry = MCQ.query.get_or_404(mcq_id)
    mcqs = json.loads(mcq_entry.mcqs)
    filepath = f"mcqs_{mcq_id}.csv"

    # Write the MCQs to a CSV file.
    with open(filepath, "w", newline="") as csvfile:
        fieldnames = ["MCQ", "Choices", "Correct"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for key, value in mcqs.items():
            writer.writerow(
                {
                    "MCQ": value["mcq"],
                    "Choices": " || ".join(
                        [f"{k} => {v}" for k, v in value["options"].items()]
                    ),
                    "Correct": value["correct"],
                }
            )

    # Send the CSV file as an attachment.
    return send_file(filepath, as_attachment=True)
