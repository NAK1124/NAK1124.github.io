from __future__ import annotations

import csv
from dataclasses import dataclass
from typing import List, Optional, Callable, Dict


# Responsible / Real-World Connection (8–12 lines)
"""
Real-world use: Libraries (schools, cities, universities) track books so staff can
quickly find titles, monitor what is issued vs available, and keep records accurate.
This type of system helps prevent lost items, supports budgeting decisions, and
improves service for students and community members.
Responsible practice: even “simple” datasets can become sensitive if linked to
borrowers. A responsible system avoids storing personal borrower identity unless
necessary, protects saved files from unauthorized access, and validates inputs to
prevent corrupted records. Also, it should not assume data is correct (e.g., missing
fields) and must handle file errors safely to avoid data loss.
"""


# A) DATA STRUCTURES (A1)

@dataclass
class Book:
    """Represents one library book record."""
    bid: int
    title: str
    author: str
    category: str
    status: str  # expected: "issued" or "available"

    def to_row(self) -> List[str]:
        """Convert the Book into a CSV row (all strings)."""
        return [str(self.bid), self.title, self.author, self.category, self.status]


class LibrarySystem:
    """Manages a list of Book objects and provides search/sort/analysis/update tools."""

    def __init__(self) -> None:
        self._books: List[Book] = []
        self._loaded_file: Optional[str] = None

    # Utility / Validation (A4)

    @staticmethod
    def _clean_text(s: str) -> str:
        return " ".join(s.strip().split())

    @staticmethod
    def _normalize_status(s: str) -> str:
        s = LibrarySystem._clean_text(s).lower()
        if s in ("issued", "issue"):
            return "issued"
        if s in ("available", "avail", "in", "in stock"):
            return "available"
        return s  # keep as-is; validation happens elsewhere

    @staticmethod
    def _is_valid_status(s: str) -> bool:
        return s in ("issued", "available")

    def _next_id(self) -> int:
        """Generate a new unique ID (max existing ID + 1)."""
        if not self._books:
            return 1
        return max(b.bid for b in self._books) + 1

    def _find_by_id_linear(self, target_id: int) -> Optional[Book]:
        """Manual linear search by book ID (A3)."""
        for b in self._books:
            if b.bid == target_id:
                return b
        return None

    def _find_all_by_title_linear(self, title: str) -> List[Book]:
        """Manual linear search by title (case-insensitive) (A3)."""
        t = self._clean_text(title).lower()
        matches: List[Book] = []
        for b in self._books:
            if b.title.lower() == t:
                matches.append(b)
        return matches

   
    # File I/O (A3)
  

    def load_from_csv(self, filepath: str) -> None:
        """
        Load book records from a CSV file using try/except.
        Expected headers: bid,title,author,category,status
        """
        try:
            with open(filepath, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                required = {"bid", "title", "author", "category", "status"}
                if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
                    raise ValueError("Invalid CSV format: missing required headers.")

                loaded: List[Book] = []
                for row in reader:
                    bid_str = (row.get("bid") or "").strip()
                    title = self._clean_text(row.get("title") or "")
                    author = self._clean_text(row.get("author") or "")
                    category = self._clean_text(row.get("category") or "")
                    status = self._normalize_status(row.get("status") or "")

                    if not bid_str.isdigit():
                        # skip invalid rows safely (could also raise error)
                        continue
                    bid = int(bid_str)

                    if title == "" or author == "" or category == "" or not self._is_valid_status(status):
                        # skip incomplete/invalid rows
                        continue

                    loaded.append(Book(bid, title, author, category, status))

                self._books = loaded
                self._loaded_file = filepath

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except Exception as e:
            raise RuntimeError(f"Could not load file. Reason: {e}")

    def save_to_csv(self, filepath: str) -> None:
        """Save current records to CSV using try/except."""
        try:
            with open(filepath, mode="w", newline="", encoding="utf-8") as f:
                fieldnames = ["bid", "title", "author", "category", "status"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for b in self._books:
                    writer.writerow({
                        "bid": b.bid,
                        "title": b.title,
                        "author": b.author,
                        "category": b.category,
                        "status": b.status
                    })
            self._loaded_file = filepath
        except Exception as e:
            raise RuntimeError(f"Could not save file. Reason: {e}")

 
    # Display
 

    def display_all(self) -> None:
        """Display all records in a readable format."""
        if not self._books:
            print("\nNo records loaded.\n")
            return

        print("\n--- Library Books ---")
        for b in self._books:
            print(f"ID: {b.bid:<3} | {b.title} | {b.author} | {b.category} | {b.status}")
        print(f"Total records: {len(self._books)}\n")

    # -------------------------
    # Manual Sort (A3)
    # -------------------------

    def insertion_sort_by_title(self) -> None:
        """Manual insertion sort by title (A3)."""
        for i in range(1, len(self._books)):
            key_item = self._books[i]
            j = i - 1
            while j >= 0 and self._books[j].title.lower() > key_item.title.lower():
                self._books[j + 1] = self._books[j]
                j -= 1
            self._books[j + 1] = key_item

    # Python built-in sorter (allowed alongside manual sort)
    def sort_by_id_builtin(self) -> None:
        """Sort by ID using Python built-in sort (A3 integration)."""
        self._books.sort(key=lambda b: b.bid)


    # Analysis Outputs (A3)


    def analysis_summary(self) -> None:
        """Show at least two analysis outputs (we provide several)."""
        if not self._books:
            print("\nNo records loaded.\n")
            return

        total = len(self._books)

        # Frequency: status
        status_counts: Dict[str, int] = {"issued": 0, "available": 0}
        for b in self._books:
            if b.status in status_counts:
                status_counts[b.status] += 1

        # Frequency: categories (1 3)
        cat_counts: Dict[str, int] = {}
        for b in self._books:
            cat_counts[b.category] = cat_counts.get(b.category, 0) + 1
        top_categories = sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        # Frequency: authors (top 3)
        author_counts: Dict[str, int] = {}
        for b in self._books:
            author_counts[b.author] = author_counts.get(b.author, 0) + 1
        top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        # Min/Max ID
        min_id = min(b.bid for b in self._books)
        max_id = max(b.bid for b in self._books)

        print("\n--- Analysis Summary ---")
        print(f"Total books: {total}")
        print(f"Issued: {status_counts['issued']} | Available: {status_counts['available']}")
        print(f"Min ID: {min_id} | Max ID: {max_id}")

        print("\nTop 3 Categories:")
        for cat, count in top_categories:
            print(f"- {cat}: {count}")

        print("\nTop 3 Authors:")
        for a, count in top_authors:
            print(f"- {a}: {count}")

        print()


    # CRUD (Add / Update / Delete)
   

    def add_book(self, title: str, author: str, category: str, status: str) -> Book:
        """Add a new record with a generated unique ID."""
        title = self._clean_text(title)
        author = self._clean_text(author)
        category = self._clean_text(category)
        status = self._normalize_status(status)

        if title == "" or author == "" or category == "":
            raise ValueError("Title/author/category cannot be empty.")
        if not self._is_valid_status(status):
            raise ValueError("Status must be 'issued' or 'available'.")

        new_book = Book(self._next_id(), title, author, category, status)
        self._books.append(new_book)
        return new_book

    def update_book(self, bid: int, title: str, author: str, category: str, status: str) -> None:
        """Update an existing record by ID."""
        book = self._find_by_id_linear(bid)
        if book is None:
            raise LookupError("Book ID not found.")

        title = self._clean_text(title)
        author = self._clean_text(author)
        category = self._clean_text(category)
        status = self._normalize_status(status)

        if title == "" or author == "" or category == "":
            raise ValueError("Title/author/category cannot be empty.")
        if not self._is_valid_status(status):
            raise ValueError("Status must be 'issued' or 'available'.")

        book.title = title
        book.author = author
        book.category = category
        book.status = status

    def delete_book(self, bid: int) -> None:
        """Delete a record by ID."""
        for i in range(len(self._books)):
            if self._books[i].bid == bid:
                del self._books[i]
                return
        raise LookupError("Book ID not found.")



# User Interface (Menu)


def prompt_int(msg: str) -> int:
    """Prompt until a valid integer is entered."""
    while True:
        raw = input(msg).strip()
        if raw.isdigit():
            return int(raw)
        print("Invalid input. Please enter a whole number.")


def prompt_nonempty(msg: str) -> str:
    """Prompt until a non-empty string is entered."""
    while True:
        s = input(msg)
        s2 = " ".join(s.strip().split())
        if s2 != "":
            return s2
        print("Invalid input. This value cannot be empty.")


def prompt_status(msg: str) -> str:
    """Prompt until status is valid."""
    while True:
        s = input(msg).strip().lower()
        s = " ".join(s.split())
        if s in ("issued", "available"):
            return s
        print("Invalid status. Enter 'issued' or 'available'.")


def main() -> None:
    system = LibrarySystem()

    while True:
        print("=== Library Books Data Management System ===")
        print("1) Load data from file")
        print("2) Display all records")
        print("3) Search by key field (ID or Title)")
        print("4) Sort by one field (Manual: Title / Built-in: ID)")
        print("5) Show analysis summary")
        print("6) Add a new record")
        print("7) Update an existing record")
        print("8) Delete a record")
        print("9) Save data to file")
        print("10) Exit")

        choice = input("Choose an option (1-10): ").strip()

        if choice == "1":
            filepath = input("Enter CSV filename (default: Books_data - Sheet1.csv): ").strip()
            if filepath == "":
                filepath = "Books_data - Sheet1.csv"
            try:
                system.load_from_csv(filepath)
                print(f"\nLoaded {len(system._books)} records from '{filepath}'.\n")
            except Exception as e:
                print(f"\nERROR: {e}\n")

        elif choice == "2":
            system.display_all()

        elif choice == "3":
            if not system._books:
                print("\nNo records loaded.\n")
                continue
            print("\nSearch by:")
            print("1) Book ID")
            print("2) Title (exact match)")
            sub = input("Choose (1-2): ").strip()
            if sub == "1":
                bid = prompt_int("Enter book ID: ")
                found = system._find_by_id_linear(bid)
                if found:
                    print(f"\nFOUND: ID {found.bid} | {found.title} | {found.author} | {found.category} | {found.status}\n")
                else:
                    print("\nNo match found.\n")
            elif sub == "2":
                t = prompt_nonempty("Enter title (exact): ")
                matches = system._find_all_by_title_linear(t)
                if matches:
                    print()
                    for b in matches:
                        print(f"FOUND: ID {b.bid} | {b.title} | {b.author} | {b.category} | {b.status}")
                    print()
                else:
                    print("\nNo match found.\n")
            else:
                print("\nInvalid choice.\n")

        elif choice == "4":
            if not system._books:
                print("\nNo records loaded.\n")
                continue
            print("\nSort options:")
            print("1) Manual insertion sort by Title")
            print("2) Built-in sort by ID")
            sub = input("Choose (1-2): ").strip()
            if sub == "1":
                system.insertion_sort_by_title()
                print("\nSorted by title (manual insertion sort).\n")
            elif sub == "2":
                system.sort_by_id_builtin()
                print("\nSorted by ID (built-in sort).\n")
            else:
                print("\nInvalid choice.\n")

        elif choice == "5":
            system.analysis_summary()

        elif choice == "6":
            try:
                title = prompt_nonempty("Title: ")
                author = prompt_nonempty("Author: ")
                category = prompt_nonempty("Category: ")
                status = prompt_status("Status (issued/available): ")
                new_book = system.add_book(title, author, category, status)
                print(f"\nAdded: ID {new_book.bid} | {new_book.title}\n")
            except Exception as e:
                print(f"\nERROR: {e}\n")

        elif choice == "7":
            if not system._books:
                print("\nNo records loaded.\n")
                continue
            try:
                bid = prompt_int("Enter book ID to update: ")
                if system._find_by_id_linear(bid) is None:
                    print("\nNo match found.\n")
                    continue
                title = prompt_nonempty("New Title: ")
                author = prompt_nonempty("New Author: ")
                category = prompt_nonempty("New Category: ")
                status = prompt_status("New Status (issued/available): ")
                system.update_book(bid, title, author, category, status)
                print("\nRecord updated.\n")
            except Exception as e:
                print(f"\nERROR: {e}\n")

        elif choice == "8":
            if not system._books:
                print("\nNo records loaded.\n")
                continue
            try:
                bid = prompt_int("Enter book ID to delete: ")
                system.delete_book(bid)
                print("\nRecord deleted.\n")
            except Exception as e:
                print(f"\nERROR: {e}\n")

        elif choice == "9":
            if not system._books:
                print("\nNo records loaded.\n")
                continue
            filepath = input("Enter output CSV filename (default: library_output.csv): ").strip()
            if filepath == "":
                filepath = "library_output.csv"
            try:
                system.save_to_csv(filepath)
                print(f"\nSaved {len(system._books)} records to '{filepath}'.\n")
            except Exception as e:
                print(f"\nERROR: {e}\n")

        elif choice == "10":
            print("\nGoodbye!\n")
            break

        else:
            print("\nInvalid menu option. Choose 1–10.\n")


if __name__ == "__main__":
    main()

"""
TEST LOG 1
----------------------------------------
Test Type: Normal
Feature: Load CSV + Display Records
Input:
- Menu option: 1
- Filename: "Books_data - Sheet1.csv"
- Menu option: 2
Expected Output:
- Loaded 61 records from 'Books_data - Sheet1.csv
- Each record displays ID, title, author, category, status
Actual Output:
- Matches the expected output


TEST LOG 2
----------------------------------------
Test Type: Normal
Feature: Manual Linear Search by ID
Input:
- Menu option: 3
- Search type: ID
- Book ID: 3
Expected Output:
- Book with ID 3 is found and displayed
Actual Output:
- Matches the expected output


TEST LOG 3
----------------------------------------
Test Type: Normal
Feature: Manual Insertion Sort by Title
Input:
- Menu option: 4
- Sort option: Manual insertion sort by title
Expected Output:
- Records sorted by title (manual insertion sort)
Actual Output:
- Matches the expected output

TEST LOG 4
----------------------------------------
Test Type: Edge Case
Feature: Analysis on Empty Dataset
Input:
- Menu option: 5 (before loading any file)
Expected Output:
- System reports that no records are loaded
- Program does not crash
Actual Output:
- Message "No records loaded." displayed


TEST LOG 5
----------------------------------------
Test Type: Edge Case
Feature: Search ID Not Found
Input:
- Menu option: 3
- Search type: ID
- Book ID: 999
Expected Output:
- System reports no match found
Actual Output:
- Message "No match found." displayed


TEST LOG 6
----------------------------------------
Test Type: Edge Case
Feature: Boundary Value (Lowest ID)
Input:
- Menu option: 3
- Search type: ID
- Book ID: 1
Expected Output:
- Book with lowest ID is found successfully
Actual Output:
- Correct book record displayed


TEST LOG 7
----------------------------------------
Test Type: Invalid Input
Feature: Invalid Status Entry
Input:
- Menu option: 6 (Add new record)
- Status entered: "borrowed"
Expected Output:
- System rejects invalid status
- Prompts user to re-enter status
Actual Output:
- Error message shown
- User prompted again for valid status


TEST LOG 8
----------------------------------------
Test Type: Invalid Input
Feature: Non-numeric ID Input
Input:
- Menu option: 3
- Search type: ID
- Input: "abc"
Expected Output:
- System rejects input
- Prompts user to enter a whole number
Actual Output:
- Message "Invalid input. Please enter a whole number."

"""