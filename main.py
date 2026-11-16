"""Student Result Management System - entry point and main menu."""

from student import Student, is_valid_student_id, is_valid_date
from results import SUBJECTS, validate_score
import storage
import reports


# ---------- input helpers ----------------------------------------------
def ask(prompt, allow_blank=False):
    """Ask until the user types something (or allow a blank answer)."""
    while True:
        value = input(prompt).strip()
        if value or allow_blank:
            return value
        print("This field cannot be empty.")


def ask_gender(allow_blank=False):
    while True:
        value = input("Gender (M/F): ").strip().upper()
        if value == "" and allow_blank:
            return ""
        if value in ("M", "F"):
            return "Male" if value == "M" else "Female"
        print("Please enter M or F.")


def ask_dob(allow_blank=False):
    while True:
        value = input("Date of birth (YYYY-MM-DD): ").strip()
        if value == "" and allow_blank:
            return ""
        if is_valid_date(value):
            return value
        print("Invalid date. Use the format YYYY-MM-DD, e.g. 2008-05-21.")


def ask_score(subject, allow_blank=False):
    while True:
        text = input(f"  {subject} (0-100): ").strip()
        if text == "" and allow_blank:
            return None
        try:
            return validate_score(text)
        except ValueError:
            print("  Invalid score. Enter a number between 0 and 100.")


def find_student(students, prompt="Enter Student ID: "):
    """Ask for an ID and return the matching Student, or None."""
    student_id = ask(prompt)
    student = students.get(student_id)
    if student is None:
        print("No student found with that ID.")
    return student


def pause():
    input("\nPress Enter to continue...")


# ---------- student management -----------------------------------------
def add_student(students):
    print("\n--- Add New Student ---")
    while True:
        student_id = ask("Student ID (e.g. NH/2026/001): ")
        if not is_valid_student_id(student_id):
            print("Invalid ID. Use 3-20 letters, digits, / _ or - only.")
        elif student_id in students:
            print("That ID is already registered.")
        else:
            break
    name = ask("Full name: ")
    class_name = ask("Class/Form: ")
    gender = ask_gender()
    dob = ask_dob()

    students[student_id] = Student(student_id, name, class_name, gender, dob)
    if storage.save_students(students):
        print(f"\nStudent '{name}' added and saved.")


def view_students(students):
    print("\n--- All Students ---")
    print(reports.format_table(reports.sort_students(students.values(), "name")))


def search_students(students):
    print("\n--- Search Student ---")
    term = ask("Enter student ID or part of the name: ").lower()
    matches = [s for s in students.values()
               if term == s.student_id.lower() or term in s.name.lower()]
    if matches:
        print(f"\n{len(matches)} match(es) found:\n")
        print(reports.format_table(matches))
    else:
        print("No matching student found.")


def update_student(students):
    print("\n--- Update Student (press Enter to keep a value) ---")
    student = find_student(students)
    if student is None:
        return
    print(f"Editing: {student}")

    name = ask(f"Full name [{student.name}]: ", allow_blank=True)
    class_name = ask(f"Class/Form [{student.class_name}]: ", allow_blank=True)
    print(f"Current gender: {student.gender}")
    gender = ask_gender(allow_blank=True)
    print(f"Current date of birth: {student.dob}")
    dob = ask_dob(allow_blank=True)

    student.name = name or student.name
    student.class_name = class_name or student.class_name
    student.gender = gender or student.gender
    student.dob = dob or student.dob
    if storage.save_students(students):
        print("Student updated and saved.")


def delete_student(students):
    print("\n--- Delete Student ---")
    student = find_student(students)
    if student is None:
        return
    confirm = ask(f"Delete {student}? (yes/no): ").lower()
    if confirm == "yes":
        del students[student.student_id]
        if storage.save_students(students):
            print("Student deleted.")
    else:
        print("Deletion cancelled.")


# ---------- score management -------------------------------------------
def record_scores(students):
    print("\n--- Record Scores ---")
    student = find_student(students)
    if student is None:
        return
    print(f"Enter scores for {student.name}:")
    for subject in SUBJECTS:
        student.set_score(subject, ask_score(subject))
    if storage.save_students(students):
        print(f"\nScores saved. Average: {student.average:.2f}, "
              f"Grade: {student.grade}")


def update_score(students):
    print("\n--- Update a Score ---")
    student = find_student(students)
    if student is None:
        return
    if not student.scores:
        print("This student has no scores yet. Use 'Record scores' first.")
        return

    subjects = list(student.scores)
    for number, subject in enumerate(subjects, start=1):
        print(f"{number}. {subject}: {student.scores[subject]:.1f}")
    try:
        choice = int(ask("Choose subject number: "))
        if choice < 1:
            raise IndexError
        subject = subjects[choice - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    student.set_score(subject, ask_score(subject))
    if storage.save_students(students):
        print(f"Updated. New average: {student.average:.2f}, "
              f"Grade: {student.grade}")


def show_report_card(students):
    print("\n--- Report Card ---")
    student = find_student(students)
    if student:
        print()
        print(reports.format_report_card(student))


# ---------- reporting --------------------------------------------------
def list_results(students):
    print("\n--- Results List ---")
    print("1. Sort by average (highest to lowest)")
    print("2. Sort by name")
    choice = ask("Choose: ")
    order = "name" if choice == "2" else "average"
    print()
    print(reports.format_table(reports.sort_students(students.values(), order)))


def show_statistics(students):
    print("\n--- Class Statistics ---")
    print(reports.format_statistics(students.values()))


def export_report(students):
    print("\n--- Save Text Report ---")
    if not students:
        print("There are no students to report on.")
        return
    text = reports.build_full_report(list(students.values()))
    try:
        path = reports.save_report(text)
    except OSError as error:
        print(f"Could not save report: {error}")
    else:
        print(f"Report saved to: {path}")


# ---------- main menu --------------------------------------------------
MENU = """
==========================================
     STUDENT RESULT MANAGEMENT SYSTEM
==========================================
 STUDENTS
  1. Add student
  2. View all students
  3. Search student
  4. Update student
  5. Delete student
 SCORES
  6. Record scores
  7. Update a score
  8. Show report card
 REPORTS
  9. Results list (sort)
 10. Class statistics
 11. Save text report to file
  0. Exit
------------------------------------------"""


def main():
    students = storage.load_students()
    print(f"Loaded {len(students)} student(s).")

    actions = {
        "1": add_student, "2": view_students, "3": search_students,
        "4": update_student, "5": delete_student, "6": record_scores,
        "7": update_score, "8": show_report_card, "9": list_results,
        "10": show_statistics, "11": export_report,
    }

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid option. Please try again.")
            continue
        try:
            action(students)
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
        pause()


if __name__ == "__main__":
    main()
