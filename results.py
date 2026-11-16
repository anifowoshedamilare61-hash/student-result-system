"""Score validation, grading logic and class statistics."""

# At least five subjects are required by the brief.
SUBJECTS = ["Mathematics", "English", "Physics", "Chemistry", "Biology"]

# (minimum average, grade) - checked from the top down.
GRADE_BANDS = [
    (70, "A"),
    (60, "B"),
    (50, "C"),
    (45, "D"),
    (40, "E"),
    (0, "F"),
]


def grade_for_average(average):
    """Return the letter grade for an average score."""
    for minimum, grade in GRADE_BANDS:
        if average >= minimum:
            return grade
    return "F"


def validate_score(text):
    """Convert text to a score between 0 and 100.

    Raises ValueError if the text is not a number or is out of range.
    """
    score = float(text)  # raises ValueError for non-numbers
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100.")
    return score


def class_statistics(students):
    """Return class statistics, or None if no student has scores yet.

    Result is a dictionary with the highest score, lowest score,
    class average and the average of every subject.
    """
    scored = [s for s in students if s.scores]
    if not scored:
        return None

    highest = None  # (score, student name, subject)
    lowest = None
    subject_totals = {}
    subject_counts = {}

    for student in scored:
        for subject, score in student.scores.items():
            if highest is None or score > highest[0]:
                highest = (score, student.name, subject)
            if lowest is None or score < lowest[0]:
                lowest = (score, student.name, subject)
            subject_totals[subject] = subject_totals.get(subject, 0) + score
            subject_counts[subject] = subject_counts.get(subject, 0) + 1

    class_average = sum(s.average for s in scored) / len(scored)
    subject_averages = {
        subject: subject_totals[subject] / subject_counts[subject]
        for subject in subject_totals
    }

    return {
        "students_with_scores": len(scored),
        "highest": highest,
        "lowest": lowest,
        "class_average": class_average,
        "subject_averages": subject_averages,
    }
