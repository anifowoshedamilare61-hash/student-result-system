"""Load and save student data as JSON."""

import json
import os

from student import Student

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def load_students():
    """Return {student_id: Student}. Returns {} if the file is missing."""
    if not os.path.exists(DATA_FILE):
        return {}  # first run: no data file yet

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            raw = json.load(file)
        students = {item["student_id"]: Student.from_dict(item) for item in raw}
    except (json.JSONDecodeError, KeyError, TypeError):
        # Keep the damaged file as a backup instead of overwriting it.
        backup = DATA_FILE + ".bak"
        os.replace(DATA_FILE, backup)
        print(f"Warning: data file was damaged. Saved a copy as {backup}.")
        return {}
    except OSError as error:
        print(f"Could not read data file: {error}")
        return {}
    else:
        return students


def save_students(students):
    """Write all students to the JSON file. Returns True on success."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        temp_path = DATA_FILE + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump([s.to_dict() for s in students.values()], file, indent=4)
        os.replace(temp_path, DATA_FILE)  # replace only after a full write
    except OSError as error:
        print(f"Could not save data: {error}")
        return False
    else:
        return True
