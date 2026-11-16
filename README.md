# Student Result Management System

A menu-driven Python application that lets a school register students,
record subject scores, calculate totals/averages/grades, produce reports
and save everything to a JSON file.

Built for the New Horizon *Introduction to Python Programming* project.

## Features
- **Students:** add, view, search (by ID or name), update, delete
- **Scores:** record five subjects, update a score, individual report card
- **Reports:** ranked results list, sort by average or name, class
  statistics (highest, lowest, class average, subject averages),
  save a text report to a file
- **Persistence:** data saved to `data/students.json` and loaded on start;
  works even when the file does not exist yet

## Requirements
- Python 3.8 or newer (standard library only, nothing to install)

## How to run
```bash
git clone https://github.com/anifowoshedamilare61-hash/student-result-system.git
cd student-result-system
python main.py
```

## Project structure
```
main.py       Entry point and menu
student.py    Student class, ID/date validation (regex)
results.py    Subjects, grading, score validation, class statistics
storage.py    Load/save JSON with error handling
reports.py    Tables, report cards, text report export
data/         students.json is created here
reports/      saved text reports go here
```

## Grading scale
| Average | Grade |
|---|---|
| 70 - 100 | A |
| 60 - 69 | B |
| 50 - 59 | C |
| 45 - 49 | D |
| 40 - 44 | E |
| 0 - 39 | F |

## Python concepts used
Variables and type conversion, if/elif/else, for and while loops, lists,
tuples and dictionaries, functions with parameters and return values,
sorting with `sorted()` and `key`, try/except/else/finally-style error
handling, JSON file handling, multiple modules, a `Student` class (OOP),
`datetime` for result dates, `os`/`json`/`re` from the standard library,
and regular expressions for Student ID validation.

## Author
Anifowoshe Damilare - 24/SCI01/039 - Computer Science
