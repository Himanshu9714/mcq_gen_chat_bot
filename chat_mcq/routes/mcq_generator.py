import csv
import json
import os

from flask import Blueprint
from flask import Flask
from flask import abort
from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_file
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import MCQ
from ..utils import generate_mcqs

mcq_generator = Blueprint("mcq_generator", __name__)


@mcq_generator.route("/generate_mcqs", methods=["POST"])
def generate_mcqs_route():
    file = request.files["file"]
    num_mcqs = int(request.form["num_mcqs"])
    subject = request.form["subject"]
    complexity = request.form["complexity"]

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    response = generate_mcqs(
        file,
        num_mcqs,
        subject,
        complexity,
    )
    print("Response", response)
    if response["status_code"] == 200:
        mcqs = response["data"]
        review = response["review"]
        mcq_entry = MCQ(mcqs=json.dumps(mcqs), review=review)
        db.session.add(mcq_entry)
        db.session.commit()

    return jsonify(response)


@mcq_generator.route("/download/<int:mcq_id>")
def download(mcq_id):
    mcq_entry = MCQ.query.get_or_404(mcq_id)
    mcqs = json.loads(mcq_entry.mcqs)
    filepath = f"mcqs_{mcq_id}.csv"

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

    return send_file(filepath, as_attachment=True)
