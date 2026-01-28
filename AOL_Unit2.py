"""
ICS4U – AOL Unit 2 Project
Student Performance Data Management System (StudentsPerformance dataset)
Author: Alice Nahyun Kim

Requirements met:
A) Data structures: records stored as a LIST of OBJECTS (class-based records)
B) User interface: menu options 1–10 included
C) Searching: manual linear search (no list.index / no "in" shortcuts)
D) Sorting: one manual sorting algorithm (Insertion Sort) + one Python built-in sorter (sorted)
E) File I/O: load + save CSV
F) Validation + error handling: safe inputs, avoids crashes
G) Modular design: functions + clean structure

Important note:
- This dataset has NO student_id column, so this program GENERATES a unique student_id
  (1, 2, 3, ...) when loading the file.

Fix included:
- Uses a RELATIVE default path (same folder as this .py file) instead of /mnt/data/
- Prints clear diagnostics if 0 records load or file cannot be found
"""

from __future__ import annotations
from dataclasses import dataclass
import csv
import math
import os
from typing import Callable


# =========================
# A) DATA STRUCTURES
# =========================

@dataclass
class StudentRecord:
    """One row from StudentsPerformance, stored as an object."""
    student_id: int
    gender: str
    race_ethnicity: str
    parental_education: str
    lunch: str
    prep_course: str
    math_score: int
    reading_score: int
    writing_score: int

    def average(self) -> float:
        return (self.math_score + self.reading_score + self.writing_score) / 3.0

    def to_row(self) -> dict:
        """Convert record to a CSV row dict (includes generated student_id)."""
        return {
            "student_id": self.student_id,
            "gender": self.gender,
            "race/ethnicity": self.race_ethnicity,
            "parental level of education": self.parental_education,
            "lunch": self.lunch,
            "test preparation course": self.prep_course,
            "math score": self.math_score,
            "reading score": self.reading_score,
            "writing score": self.writing_score,
        }


# =========================
# INPUT / VALIDATION HELPERS
# =========================

def prompt_menu_choice() -> int:
    while True:
        raw = input("Enter choice (1-10): ").strip()
        if raw.isdigit():
            n = int(raw)
            if 1 <= n <= 10:
                return n
        print("Invalid choice. Enter a number from 1 to 10.")


def prompt_nonempty(prompt: str) -> str:
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Input cannot be empty.")


def prompt_int_range(prompt: str, lo: int, hi: int) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            n = int(raw)
            if lo <= n <= hi:
                return n
            print(f"Out of range. Enter {lo} to {hi}.")
        except ValueError:
            print("Invalid number. Try again.")


def prompt_yes_no(prompt: str) -> bool:
    while True:
        raw = input(prompt + " (y/n): ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please type y or n.")


# =========================
# E) FILE I/O
# =========================

REQUIRED_COLS = {
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
    "math score",
    "reading score",
    "writing score",
}

# Default: CSV is expected to be in the SAME FOLDER as this .py file
DEFAULT_CSV_FILENAME = "StudentsPerformance (1).csv"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV_PATH = os.path.join(SCRIPT_DIR, DEFAULT_CSV_FILENAME)


def load_from_csv(path: str) -> list[StudentRecord]:
    """
    Load dataset from CSV and generate student_id (1..n) because dataset has no ID column.
    Skips invalid rows safely (prints warnings instead of crashing).
    """
    records: list[StudentRecord] = []

    # Helpful diagnostics
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        print(f"File not found: {abs_path}")
        print("Tip: Put the CSV in the same folder as this .py file, then press Enter for default.")
        print(f"Current working directory: {os.getcwd()}")
        try:
            print("Files in current working directory:", os.listdir(os.getcwd()))
        except Exception:
            pass
        return []

    try:
        with open(abs_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            if not reader.fieldnames:
                print("CSV error: missing header row.")
                return []

            headers = {h.strip() for h in reader.fieldnames if h}
            missing = REQUIRED_COLS - headers
            if missing:
                print("CSV error: missing required columns:", sorted(missing))
                print("Found columns:", sorted(headers))
                return []

            student_id = 1
            for row_idx, row in enumerate(reader, start=2):
                try:
                    gender = (row.get("gender") or "").strip()
                    race = (row.get("race/ethnicity") or "").strip()
                    parent_edu = (row.get("parental level of education") or "").strip()
                    lunch = (row.get("lunch") or "").strip()
                    prep = (row.get("test preparation course") or "").strip()

                    m_raw = (row.get("math score") or "").strip()
                    r_raw = (row.get("reading score") or "").strip()
                    w_raw = (row.get("writing score") or "").strip()

                    m = int(m_raw)
                    r = int(r_raw)
                    w = int(w_raw)

                    # validate
                    if not (gender and race and parent_edu and lunch and prep):
                        raise ValueError("Empty text field(s).")
                    if not (0 <= m <= 100 and 0 <= r <= 100 and 0 <= w <= 100):
                        raise ValueError("Score out of range 0-100.")

                    records.append(StudentRecord(
                        student_id=student_id,
                        gender=gender,
                        race_ethnicity=race,
                        parental_education=parent_edu,
                        lunch=lunch,
                        prep_course=prep,
                        math_score=m,
                        reading_score=r,
                        writing_score=w
                    ))
                    student_id += 1

                except Exception as e:
                    print(f"[Load warning] Skipped row {row_idx}: {e}")

    except PermissionError:
        print(f"Permission denied: {abs_path}")
    except UnicodeDecodeError:
        print("Encoding error: file is not UTF-8. Try saving it as UTF-8 and reloading.")
    except Exception as e:
        print(f"Unexpected load error: {e}")

    return records


def save_to_csv(path: str, records: list[StudentRecord]) -> None:
    """Save records to CSV including generated student_id."""
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            fieldnames = [
                "student_id",
                "gender",
                "race/ethnicity",
                "parental level of education",
                "lunch",
                "test preparation course",
                "math score",
                "reading score",
                "writing score",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for rec in records:
                writer.writerow(rec.to_row())
        print(f"Saved {len(records)} record(s) to: {path}")
    except PermissionError:
        print(f"Permission denied: {path}")
    except Exception as e:
        print(f"Save failed: {e}")


# =========================
# DISPLAY
# =========================

def print_record(r: StudentRecord) -> None:
    print(
        f"ID={r.student_id:>4} | {r.gender:<6} | {r.race_ethnicity:<10} | "
        f"Math={r.math_score:>3} Read={r.reading_score:>3} Write={r.writing_score:>3} | "
        f"Avg={r.average():>5.1f} | Lunch={r.lunch} | Prep={r.prep_course}"
    )


def display_records(records: list[StudentRecord]) -> None:
    if not records:
        print("No data loaded.")
        return

    print("\nDisplay Options:")
    print("1) Display ALL (first 200)")
    print("2) Filter by gender")
    print("3) Filter by lunch")
    print("4) Filter by test prep course")
    choice = prompt_int_range("Choose display option (1-4): ", 1, 4)

    filtered = records
    if choice == 2:
        g = prompt_nonempty("Gender (male/female): ").lower()
        filtered = [x for x in records if x.gender.lower() == g]
    elif choice == 3:
        l = prompt_nonempty("Lunch (standard/free/reduced): ").lower()
        filtered = [x for x in records if x.lunch.lower() == l]
    elif choice == 4:
        p = prompt_nonempty("Prep (none/completed): ").lower()
        filtered = [x for x in records if x.prep_course.lower() == p]

    print(f"\nShowing {len(filtered)} record(s):")
    for r in filtered[:200]:
        print_record(r)
    if len(filtered) > 200:
        print("(Only first 200 shown.)")


# =========================
# C) SEARCHING (MANUAL LINEAR)
# =========================

def linear_search_by_id(records: list[StudentRecord], target_id: int) -> int:
    """Return index if found, else -1."""
    for i in range(len(records)):
        if records[i].student_id == target_id:
            return i
    return -1


def search_record(records: list[StudentRecord]) -> None:
    if not records:
        print("No data loaded.")
        return

    target = prompt_int_range("Enter student_id to search: ", 1, 10**9)
    idx = linear_search_by_id(records, target)
    if idx == -1:
        print("Record not found.")
    else:
        print("Record found:")
        print_record(records[idx])


# =========================
# D) SORTING
# =========================

def insertion_sort(records: list[StudentRecord], key_fn: Callable[[StudentRecord], object], reverse: bool = False) -> None:
    """
    Manual sorting algorithm: Insertion Sort (in-place)
    Reason: great for interactive apps because after edits the list is often nearly sorted.
    """
    for i in range(1, len(records)):
        current = records[i]
        current_key = key_fn(current)
        j = i - 1

        if not reverse:
            while j >= 0 and key_fn(records[j]) > current_key:
                records[j + 1] = records[j]
                j -= 1
        else:
            while j >= 0 and key_fn(records[j]) < current_key:
                records[j + 1] = records[j]
                j -= 1

        records[j + 1] = current


def sort_records(records: list[StudentRecord]) -> None:
    if not records:
        print("No data loaded.")
        return

    print("\nSort Options:")
    print("1) Manual insertion sort by average score")
    print("2) Manual insertion sort by math score")
    print("3) Built-in sorted() by reading score")
    print("4) Built-in sorted() by writing score")
    choice = prompt_int_range("Choose sort option (1-4): ", 1, 4)
    desc = prompt_yes_no("Sort descending?")

    if choice == 1:
        insertion_sort(records, key_fn=lambda r: r.average(), reverse=desc)
        print("Sorted in-place using MANUAL insertion sort (average).")
    elif choice == 2:
        insertion_sort(records, key_fn=lambda r: r.math_score, reverse=desc)
        print("Sorted in-place using MANUAL insertion sort (math).")
    elif choice == 3:
        records[:] = sorted(records, key=lambda r: r.reading_score, reverse=desc)
        print("Sorted using Python BUILT-IN sorted() (reading).")
    else:
        records[:] = sorted(records, key=lambda r: r.writing_score, reverse=desc)
        print("Sorted using Python BUILT-IN sorted() (writing).")

    print("\nTop 10 after sort:")
    for r in records[:10]:
        print_record(r)


# =========================
# SUMMARY STATS
# =========================

def mean(values: list[int]) -> float:
    return sum(values) / len(values) if values else float("nan")


def stdev(values: list[int]) -> float:
    if not values:
        return float("nan")
    m = mean(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / len(values))


def summary_statistics(records: list[StudentRecord]) -> None:
    if not records:
        print("No data loaded.")
        return

    ms = [r.math_score for r in records]
    rs = [r.reading_score for r in records]
    ws = [r.writing_score for r in records]
    av = [r.average() for r in records]

    print("\n--- Summary Statistics ---")
    print(f"Records: {len(records)}")
    print(f"Math   : mean={mean(ms):.2f} stdev={stdev(ms):.2f} min={min(ms)} max={max(ms)}")
    print(f"Reading: mean={mean(rs):.2f} stdev={stdev(rs):.2f} min={min(rs)} max={max(rs)}")
    print(f"Writing: mean={mean(ws):.2f} stdev={stdev(ws):.2f} min={min(ws)} max={max(ws)}")
    print(f"Average: mean={sum(av)/len(av):.2f} min={min(av):.2f} max={max(av):.2f}")

    completed = [r.average() for r in records if r.prep_course.lower() == "completed"]
    none = [r.average() for r in records if r.prep_course.lower() == "none"]
    if completed and none:
        print("\nPrep-course comparison (Average Score):")
        print(f"Completed: n={len(completed)} mean={sum(completed)/len(completed):.2f}")
        print(f"None     : n={len(none)} mean={sum(none)/len(none):.2f}")


# =========================
# CRUD (ADD / UPDATE / DELETE)
# =========================

def next_available_id(records: list[StudentRecord]) -> int:
    return 1 if not records else max(r.student_id for r in records) + 1


def add_record(records: list[StudentRecord]) -> None:
    sid = next_available_id(records)
    print(f"Adding new record. Generated student_id = {sid}")

    gender = prompt_nonempty("Gender: ")
    race = prompt_nonempty("Race/ethnicity: ")
    parent_edu = prompt_nonempty("Parental level of education: ")
    lunch = prompt_nonempty("Lunch: ")
    prep = prompt_nonempty("Test preparation course: ")

    m = prompt_int_range("Math score (0-100): ", 0, 100)
    r = prompt_int_range("Reading score (0-100): ", 0, 100)
    w = prompt_int_range("Writing score (0-100): ", 0, 100)

    records.append(StudentRecord(
        student_id=sid,
        gender=gender,
        race_ethnicity=race,
        parental_education=parent_edu,
        lunch=lunch,
        prep_course=prep,
        math_score=m,
        reading_score=r,
        writing_score=w
    ))

    print("Record added:")
    print_record(records[-1])


def update_record(records: list[StudentRecord]) -> None:
    if not records:
        print("No data loaded.")
        return

    target = prompt_int_range("Enter student_id to update: ", 1, 10**9)
    idx = linear_search_by_id(records, target)
    if idx == -1:
        print("Record not found.")
        return

    rec = records[idx]
    print("Current record:")
    print_record(rec)
    print("Leave blank to keep current value.\n")

    def optional_text(label: str, current: str) -> str:
        raw = input(f"{label} [{current}]: ").strip()
        return raw if raw else current

    def optional_score(label: str, current: int) -> int:
        raw = input(f"{label} (0-100) [{current}]: ").strip()
        if not raw:
            return current
        try:
            v = int(raw)
            if 0 <= v <= 100:
                return v
        except ValueError:
            pass
        print("Invalid input. Keeping current value.")
        return current

    rec.gender = optional_text("Gender", rec.gender)
    rec.race_ethnicity = optional_text("Race/ethnicity", rec.race_ethnicity)
    rec.parental_education = optional_text("Parental education", rec.parental_education)
    rec.lunch = optional_text("Lunch", rec.lunch)
    rec.prep_course = optional_text("Prep course", rec.prep_course)
    rec.math_score = optional_score("Math score", rec.math_score)
    rec.reading_score = optional_score("Reading score", rec.reading_score)
    rec.writing_score = optional_score("Writing score", rec.writing_score)

    print("Updated record:")
    print_record(rec)


def delete_record(records: list[StudentRecord]) -> None:
    if not records:
        print("No data loaded.")
        return

    target = prompt_int_range("Enter student_id to delete: ", 1, 10**9)
    idx = linear_search_by_id(records, target)
    if idx == -1:
        print("Record not found.")
        return

    print("About to delete:")
    print_record(records[idx])
    if prompt_yes_no("Confirm delete"):
        records.pop(idx)
        print("Record deleted.")
    else:
        print("Delete cancelled.")


# =========================
# B) USER INTERFACE (MENU 1–10)
# =========================

def print_menu() -> None:
    print("\n===== Student Performance Data Tool =====")
    print("1. Load data from file")
    print("2. Display records (all or filtered)")
    print("3. Search for a record (manual linear search)")
    print("4. Sort records (manual + built-in)")
    print("5. Show summary statistics")
    print("6. Add a new record")
    print("7. Update an existing record")
    print("8. Delete a record")
    print("9. Save data to file")
    print("10. Exit")


def main() -> None:
    records: list[StudentRecord] = []

    while True:
        print_menu()
        choice = prompt_menu_choice()

        if choice == 1:
            print("\nLoad Data")
            print(f"Default CSV (same folder as this program): {DEFAULT_CSV_PATH}")
            path = input("Enter CSV path (Press Enter for default): ").strip()
            if not path:
                path = DEFAULT_CSV_PATH

            loaded = load_from_csv(path)
            if not loaded:
                print("\nLoaded 0 records.")
                print("Most common reasons:")
                print("1) Wrong path (e.g., /mnt/data only works in some notebook environments)")
                print("2) CSV not in the same folder as this .py file")
                print("3) CSV headers don't match the required columns exactly")
            else:
                records = loaded
                print(f"\nLoaded {len(records)} record(s).")

        elif choice == 2:
            display_records(records)

        elif choice == 3:
            search_record(records)

        elif choice == 4:
            sort_records(records)

        elif choice == 5:
            summary_statistics(records)

        elif choice == 6:
            add_record(records)

        elif choice == 7:
            update_record(records)

        elif choice == 8:
            delete_record(records)

        elif choice == 9:
            if not records:
                print("No data to save.")
                continue
            out_path = input("Output CSV (Enter = students_performance_updated.csv): ").strip()
            if not out_path:
                out_path = "students_performance_updated.csv"
            save_to_csv(out_path, records)

        else:  # 10
            if records and not prompt_yes_no("Exit without saving changes?"):
                print("Exit cancelled.")
                continue
            print("Goodbye.")
            break


if __name__ == "__main__":
    main()

"""
=========================
AOL Unit 2 - TEST LOG
=========================

TEST 1 (Normal Case) - Load default CSV successfully
Steps:
1) Run program
2) Choose 1 (Load data)
3) Press Enter for default path
Expected:
- Prints default path
- Loads > 0 records (likely 1000)
- "Loaded ____ record(s)."
Actual:
- Matches expected output
----Always Load the data first then follow the orders--------
TEST 2 (Normal Case) - Display filter + summary stats
Steps:
1) Choose 2 (Display records)
2) Choose option 2 (Filter by gender)
3) Enter "female"
4) Choose 5 (Summary statistics)
Expected:
- Shows "Showing ___ record(s)" and prints first 200 max
- Summary shows mean/stdev/min/max for math/reading/writing
- Average mean/min/max printed
Actual: 
- Matches expected output

TEST 3 (Edge Case) - Search for record not found
Steps:
1) Choose 3 (Search)
2) Enter student_id = 999999999
Expected:
- "Record not found."
Actual:
- Matches expected output

TEST 4 (Edge Case) - Boundary score values when adding a record
Steps:
1) Choose 6 (Add record)
2) Enter valid text fields
3) Enter Math=0, Reading=100, Writing=100
4) Choose 5 (Summary statistics) OR 2 (Display all) to confirm record exists
Expected:
- Record added successfully
- Avg shown correctly (66.7)
- No crash
Actual:
- Record gets addded successfully
- Everything shows clearly
Result:
- Matches expected output

TEST 5 (Invalid Input) - Menu input not a number
Steps:
1) At main menu, type "hello"
Expected:
- "Invalid choice. Enter a number from 1 to 10."
- Returns to prompt without crashing
Actual:
- Matches expected output
TEST 6 (Invalid Input) - Score input letters instead of number
Steps:
1) Choose 6 (Add record)
2) When asked "Math score (0-100):" type "abc"
Expected:
- "Invalid number. Try again."
- Re-prompts until a valid integer is entered
Actual: Matches expected output
- __________________________

(Optional Extra Test) - File not found handling
Steps:
1) Choose 1 (Load data)
2) Enter path: does_not_exist.csv
Expected:
- "File not found: <absolute path>"
- Prints tips + working directory + file listing
- "Loaded 0 records." + common reasons
Actual:
- Matches expected output
"""
