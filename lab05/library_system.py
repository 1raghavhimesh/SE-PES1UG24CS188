"""Track library loans, calculate overdue fines, and manage renewals."""

import ast
import json
import operator
from datetime import datetime
from pathlib import Path

FINE_CONFIG = {"per_day": 2}
loans = {}


def add_book_loan(student_id, book_id, dates=None):
    """Record a book loan for a student."""
    if not student_id:
        return
    if not isinstance(book_id, str):
        raise TypeError("book_id must be a string")
    if dates is None:
        dates = []
    dates.append(datetime.now().isoformat(timespec="seconds"))
    loans[student_id] = loans.get(student_id, []) + [book_id]
    print(
        f"{student_id} borrowed {book_id} "
        f"(loan dates on record: {len(dates)})"
    )


def return_book(student_id, book_id):
    """Remove a returned book from a student's active loans."""
    if student_id not in loans:
        return
    try:
        loans[student_id].remove(book_id)
    except ValueError:
        return
    if not loans[student_id]:
        del loans[student_id]


def calculate_fine(days_overdue):
    """Calculate the fine for a non-negative number of overdue days."""
    if not isinstance(days_overdue, int) or isinstance(days_overdue, bool):
        raise TypeError("days_overdue must be an integer")
    if days_overdue < 0:
        raise ValueError("days_overdue cannot be negative")
    return days_overdue * FINE_CONFIG["per_day"]


def renew_book(student_id, book_id, extra_days):
    """Renew a book and adjust the daily fine rate for long renewals."""
    if extra_days < 0:
        raise ValueError("extra_days cannot be negative")
    if extra_days > 14:
        FINE_CONFIG["per_day"] += 1
    print(f"Renewed {book_id} for {student_id} by {extra_days} days")


def load_records(file="loans.json"):
    """Load loan records from a JSON file, replacing current records."""
    path = Path(file)
    if not path.exists():
        loans.clear()
        return
    with path.open("r", encoding="utf-8") as record_file:
        records = json.load(record_file)
    if not isinstance(records, dict):
        raise ValueError("Loan records must contain a JSON object")
    loans.clear()
    loans.update(records)


def save_records(file="loans.json"):
    """Save current loan records to a JSON file."""
    with Path(file).open("w", encoding="utf-8") as record_file:
        json.dump(loans, record_file, indent=2)


def fine_from_rule(rule, days):
    """Evaluate a restricted arithmetic rule using the variable 'days'."""
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.Name) and node.id == "days":
            return days
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = evaluate(node.left)
            right = evaluate(node.right)
            division_ops = (ast.Div, ast.FloorDiv, ast.Mod)
            if isinstance(node.op, division_ops) and right == 0:
                raise ValueError("Division by zero is not allowed")
            return allowed_operators[type(node.op)](left, right)
        raise ValueError("Unsupported expression in fine rule")

    try:
        return evaluate(ast.parse(rule, mode="eval"))
    except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as error:
        raise ValueError("Invalid fine calculation rule") from error


def print_report():
    """Print all currently active loan records."""
    print("Loan Report")
    for student_id, book_ids in loans.items():
        print(f"{student_id} -> {book_ids}")


def main():
    """Run a small demonstration of the library loan system."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 21)
    print("Fine for 5 days:", calculate_fine(5))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))
    prompt = "Days overdue for S102 (press Enter for 0): "
    days_text = input(prompt).strip() or "0"
    try:
        days_overdue = int(days_text)
        print("S102 owes:", calculate_fine(days_overdue))
    except (ValueError, TypeError) as error:
        print(f"Invalid overdue days: {error}")
    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()
