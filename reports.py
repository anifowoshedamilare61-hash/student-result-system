"""Report generation: tables, report cards and saved text reports."""

import os
from datetime import datetime

from results import class_statistics

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")


def sort_students(students, by="average"):
    """Sort by average (highest first) or by name (A-Z)."""
    if by == "name":
        return sorted(students, key=lambda s: s.name.lower())
    return sorted(students, key=lambda s: s.average, reverse=True)


def format_table(students):
    """Return a table of students with totals, averages and grades."""
    if not students:
        return "No students to display."

    header = (f"{'No.':<4}{'ID':<14}{'Name':<24}{'Class':<10}"
              f"{'Total':>8}{'Average':>10}{'Grade':>7}")
    lines = [header, "-" * len(header)]
    for position, s in enumerate(students, start=1):
        lines.append(
            f"{position:<4}{s.student_id:<14}{s.name[:22]:<24}"
            f"{s.class_name[:8]:<10}{s.total:>8.1f}{s.average:>10.2f}"
            f"{s.grade:>7}"
        )
    return "\n".join(lines)


def format_report_card(student):
    """Return an individual report card as text."""
    line = "=" * 46
    lines = [
        line,
        "STUDENT REPORT CARD".center(46),
        line,
        f"Name      : {student.name}",
        f"Student ID: {student.student_id}",
        f"Class     : {student.class_name}",
        f"Gender    : {student.gender}",
        f"Date Born : {student.dob}",
        "-" * 46,
    ]
    if not student.scores:
        lines.append("No scores have been recorded yet.")
    else:
        lines.append(f"{'Subject':<28}{'Score':>8}")
        for subject, score in student.scores.items():
            lines.append(f"{subject:<28}{score:>8.1f}")
        lines += [
            "-" * 46,
            f"{'Total':<28}{student.total:>8.1f}",
            f"{'Average':<28}{student.average:>8.2f}",
            f"{'Grade':<28}{student.grade:>8}",
            f"Result entered: {student.result_date}",
        ]
    lines.append(line)
    return "\n".join(lines)


def format_statistics(students):
    """Return class statistics as text."""
    stats = class_statistics(students)
    if stats is None:
        return "No scores recorded yet, so there are no statistics."

    high_score, high_name, high_subject = stats["highest"]
    low_score, low_name, low_subject = stats["lowest"]
    lines = [
        f"Students with scores : {stats['students_with_scores']}",
        f"Class average        : {stats['class_average']:.2f}",
        f"Highest score        : {high_score:.1f} ({high_name}, {high_subject})",
        f"Lowest score         : {low_score:.1f} ({low_name}, {low_subject})",
        "",
        "Subject averages:",
    ]
    for subject, average in stats["subject_averages"].items():
        lines.append(f"  {subject:<20}{average:>6.2f}")
    return "\n".join(lines)


def build_full_report(students):
    """Build the complete class report (ranked table + statistics)."""
    ranked = sort_students(students, "average")
    stamp = datetime.now().strftime("%d %B %Y, %H:%M")
    parts = [
        "STUDENT RESULT REPORT",
        f"Generated: {stamp}",
        "",
        format_table(ranked),
        "",
        "CLASS STATISTICS",
        "-" * 16,
        format_statistics(students),
    ]
    return "\n".join(parts)


def save_report(text):
    """Save report text to the reports folder. Returns the file path."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    filename = datetime.now().strftime("report_%Y%m%d_%H%M%S.txt")
    path = os.path.join(REPORT_DIR, filename)
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)
    return path
