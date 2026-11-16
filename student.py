"""The Student class and validation helpers."""

import re
from datetime import datetime

from results import grade_for_average

DATE_FORMAT = "%Y-%m-%d"
# Letters, digits, / _ - only, 3 to 20 characters (e.g. NH/2026/001).
ID_PATTERN = re.compile(r"^[A-Za-z0-9/_-]{3,20}$")


def is_valid_student_id(student_id):
    """Use a regular expression to check the Student ID format."""
    return bool(ID_PATTERN.match(student_id))


def is_valid_date(text):
    """Check that text is a real date in YYYY-MM-DD format."""
    try:
        datetime.strptime(text, DATE_FORMAT)
    except ValueError:
        return False
    return True


class Student:
    """A student and their subject scores."""

    def __init__(self, student_id, name, class_name, gender, dob,
                 scores=None, result_date=None):
        self.student_id = student_id
        self.name = name
        self.class_name = class_name
        self.gender = gender
        self.dob = dob                    # string, YYYY-MM-DD
        self.scores = scores or {}        # {subject: score}
        self.result_date = result_date    # when scores were last entered

    # ----- calculated values -------------------------------------------
    @property
    def total(self):
        return sum(self.scores.values())

    @property
    def average(self):
        if not self.scores:
            return 0.0
        return self.total / len(self.scores)

    @property
    def grade(self):
        if not self.scores:
            return "-"
        return grade_for_average(self.average)

    # ----- score handling ----------------------------------------------
    def set_score(self, subject, score):
        """Record a score and stamp the date and time it was entered."""
        self.scores[subject] = score
        self.result_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ----- saving / loading --------------------------------------------
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "class_name": self.class_name,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "result_date": self.result_date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["student_id"],
            data["name"],
            data["class_name"],
            data["gender"],
            data["dob"],
            data.get("scores", {}),
            data.get("result_date"),
        )

    def __str__(self):
        return f"{self.student_id} - {self.name} ({self.class_name})"
