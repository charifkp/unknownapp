import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
STUDENTS_FILE = DATA_DIR / "students.json"


@dataclass
class Student:
    id: str
    name: str
    major: str
    enrolledCourses: List[str]
    completedCourses: List[str]


def load_students() -> Dict[str, Student]:
    if not STUDENTS_FILE.exists():
        return {}

    with STUDENTS_FILE.open("r", encoding="utf-8") as file:
        try:
            raw_students = json.load(file)
        except json.JSONDecodeError:
            return {}

    students: Dict[str, Student] = {}
    for item in raw_students:
        student = Student(
            id=item.get("id", "").strip(),
            name=item.get("name", "").strip(),
            major=item.get("major", "Undeclared").strip() or "Undeclared",
            enrolledCourses=item.get("enrolledCourses", []),
            completedCourses=item.get("completedCourses", []),
        )
        if student.id:
            students[student.id] = student
    return students


def save_students(students: Dict[str, Student]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with STUDENTS_FILE.open("w", encoding="utf-8") as file:
        json.dump([asdict(student) for student in students.values()], file, indent=2)


def prompt_non_empty(prompt_text: str) -> str:
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Value cannot be empty. Please try again.")


def create_student_profile(students: Dict[str, Student]) -> Student:
    print("\n--- Create New Student Profile ---")
    while True:
        student_id = prompt_non_empty("Enter new student ID: ")
        if student_id in students:
            print(f"Student ID '{student_id}' already exists. Please enter a different ID.")
        else:
            break

    student_name = prompt_non_empty("Enter full name: ")
    major = input("Enter major (leave blank for Undeclared): ").strip() or "Undeclared"

    student = Student(
        id=student_id,
        name=student_name,
        major=major,
        enrolledCourses=[],
        completedCourses=[],
    )
    students[student.id] = student
    save_students(students)
    print("\nStudent profile created successfully:\n")
    print_student_summary(student)
    return student


def print_student_summary(student: Student) -> None:
    print(f"ID: {student.id}")
    print(f"Name: {student.name}")
    print(f"Major: {student.major}")
    print(f"Enrolled Courses: {student.enrolledCourses}")
    print(f"Completed Courses: {student.completedCourses}")
    print()


def view_all_students(students: Dict[str, Student]) -> None:
    if not students:
        print("No student profiles are available.")
        return

    print("\n--- Existing Student Profiles ---")
    for student in students.values():
        print_student_summary(student)


def main() -> None:
    print("Student Profile Manager")
    students = load_students()

    while True:
        print("\nChoose an option:")
        print("1. Create a new student profile")
        print("2. Lookup existing student profile")
        print("3. View all student profiles")
        print("4. Exit")

        choice = input("Enter choice [1-4]: ").strip()
        if choice == "1":
            create_student_profile(students)
        elif choice == "2":
            query_id = prompt_non_empty("Enter student ID to lookup: ")
            student = students.get(query_id)
            if student:
                print("\nStudent profile found:")
                print_student_summary(student)
            else:
                print(f"Student ID '{query_id}' was not found.")
                if input("Would you like to create a new profile? (y/n): ").strip().lower() == "y":
                    create_student_profile(students)
        elif choice == "3":
            view_all_students(students)
        elif choice == "4":
            print("Exiting. Goodbye.")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
