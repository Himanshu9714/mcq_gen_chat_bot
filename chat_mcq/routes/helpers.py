def generate_mcqs(text, num_mcqs, subject, complexity):
    # Mock function to simulate MCQ generation
    mcqs = {
        str(i + 1): {
            "mcq": f"Sample question {i+1}?",
            "options": {
                "a": "Option A",
                "b": "Option B",
                "c": "Option C",
                "d": "Option D",
            },
            "correct": "a",
        }
        for i in range(num_mcqs)
    }
    review = "This is a sample complexity analysis for the generated MCQs."
    return mcqs, review
