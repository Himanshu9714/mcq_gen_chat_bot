from .extensions import db


class MCQ(db.Model):
    __tablename__ = "mcqs"

    id = db.Column(db.Integer, primary_key=True)
    mcqs = db.Column(db.Text, nullable=False)
    review = db.Column(db.Text, nullable=False)
