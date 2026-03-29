import base64
import hashlib
import json
import os
import pickle
import random
import secrets
import sys
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
QUESTIONS_FILE = BASE_DIR / "questions.json"
USERS_FILE = BASE_DIR / "users.json"
HISTORY_FILE = BASE_DIR / "history.dat"
FEEDBACK_FILE = BASE_DIR / "feedback.dat"

DIFFICULTY_WEIGHTS = {
    "easy": 1,
    "medium": 2,
    "hard": 3,
}


def print_dragon_banner():
    dragon = r"""
          / \  //\
   |\___/|      \
   /0  0  \      \
  /     /  \     *
  \_^_\'/   \____/
  //_^_/     \\
 ( //) |      |
  ""  /       |
   ""         |
Python Quiz Dragon welcomes you!
"""
    print(dragon)


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return base64.b64encode(salt).decode("utf-8"), base64.b64encode(digest).decode("utf-8")


def verify_password(stored_value, password):
    try:
        salt_b64, digest_b64 = stored_value.split("$", 1)
        salt = base64.b64decode(salt_b64.encode("utf-8"))
        expected = base64.b64decode(digest_b64.encode("utf-8"))
    except Exception:
        return False

    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return secrets.compare_digest(actual, expected)


def read_json_file(path, default):
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return default
    return data


def write_json_file(path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_secure_dat(path, default):
    if not path.exists():
        save_secure_dat(path, default)
        return default

    try:
        raw_text = path.read_text(encoding="utf-8").strip()
        if not raw_text:
            save_secure_dat(path, default)
            return default
        raw_bytes = base64.b64decode(raw_text.encode("utf-8"))
        return pickle.loads(raw_bytes)
    except Exception:
        save_secure_dat(path, default)
        return default


def save_secure_dat(path, obj):
    blob = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
    encoded = base64.b64encode(blob).decode("utf-8")
    path.write_text(encoded, encoding="utf-8")


def load_and_validate_questions():
    if not QUESTIONS_FILE.exists():
        print("Error: questions.json not found.")
        sys.exit(1)

    try:
        raw_text = QUESTIONS_FILE.read_text(encoding="utf-8")
        if not raw_text.strip():
            raise ValueError("empty")
        payload = json.loads(raw_text)
    except Exception:
        print("Error: Invalid format of questions.json.")
        return None

    if not isinstance(payload, dict) or "questions" not in payload:
        print("Error: Invalid format of questions.json.")
        return None

    questions = payload.get("questions")
    if not isinstance(questions, list) or len(questions) == 0:
        print("Error: Invalid format of questions.json.")
        return None

    required = {"question", "type", "answer", "category", "difficulty"}
    for q in questions:
        if not isinstance(q, dict):
            print("Error: Invalid format of questions.json.")
            return None
        if not required.issubset(q.keys()):
            print("Error: Invalid format of questions.json.")
            return None
        if q["type"] not in {"multiple_choice", "true_false", "short_answer"}:
            print("Error: Invalid format of questions.json.")
            return None
        if q["type"] == "multiple_choice":
            if not isinstance(q.get("options"), list) or len(q.get("options", [])) == 0:
                print("Error: Invalid format of questions.json.")
                return None

    return questions


def question_id(question):
    seed = f"{question.get('question','')}|{question.get('answer','')}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


def feedback_weight(question, feedback_store):
    qid = question_id(question)
    item = feedback_store.get(qid)
    if not item:
        return 1.0
    count = item.get("count", 0)
    total = item.get("sum", 0)
    if count <= 0:
        return 1.0
    avg = total / count
    return max(0.2, avg / 3.0)


def weighted_sample_without_replacement(pool, count, feedback_store):
    remaining = list(pool)
    selected = []
    while remaining and len(selected) < count:
        weights = [feedback_weight(q, feedback_store) for q in remaining]
        idx = random.choices(range(len(remaining)), weights=weights, k=1)[0]
        selected.append(remaining.pop(idx))
    return selected


def input_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Invalid input. Please enter a valid option.")


def authenticate_user():
    users_payload = read_json_file(USERS_FILE, {"users": {}})
    if not isinstance(users_payload, dict) or "users" not in users_payload or not isinstance(users_payload["users"], dict):
        users_payload = {"users": {}}
    users = users_payload["users"]

    while True:
        print("\n1) Login")
        print("2) Register")
        choice = input("Choose an option: ").strip()

        if choice == "2":
            username = input_non_empty("Choose a username: ")
            if username in users:
                print("Invalid input. Please enter a valid option.")
                continue
            password = input_non_empty("Choose a password: ")
            salt, digest = hash_password(password)
            users[username] = f"{salt}${digest}"
            write_json_file(USERS_FILE, {"users": users})
            print("Registration successful. Please log in.")
            continue

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            stored = users.get(username)
            if not stored or not verify_password(stored, password):
                print("Login failed. Please try again.")
                continue
            print(f"Welcome, {username}!")
            return username

        print("Invalid input. Please enter a valid option.")


def normalize_difficulty(value):
    lowered = value.strip().lower()
    if lowered in DIFFICULTY_WEIGHTS:
        return lowered
    return ""


def ask_question_count(max_count):
    while True:
        raw = input("How many questions do you want this round? ").strip()
        try:
            value = int(raw)
            if value <= 0:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a valid option.")
            continue

        if value > max_count:
            print("Requested number exceeds available questions. Will use maximum available.")
            return max_count
        return value


def get_answer_from_user(question):
    q_type = question["type"]
    if q_type == "multiple_choice":
        for i, option in enumerate(question["options"], start=1):
            print(f"{i}) {option}")
        while True:
            raw = input("Your choice: ").strip()
            if not raw.isdigit():
                print("Invalid input. Please enter a valid option.")
                continue
            idx = int(raw)
            if idx < 1 or idx > len(question["options"]):
                print("Invalid input. Please enter a valid option.")
                continue
            return question["options"][idx - 1]

    if q_type == "true_false":
        print("1) True")
        print("2) False")
        valid = {
            "1": "true",
            "2": "false",
            "true": "true",
            "false": "false",
            "t": "true",
            "f": "false",
        }
        while True:
            raw = input("Your choice: ").strip().lower()
            if raw not in valid:
                print("Invalid input. Please enter a valid option.")
                continue
            return valid[raw]

    while True:
        raw = input("Your answer: ").strip()
        if not raw:
            print("Invalid input. Please enter a valid option.")
            continue
        return raw


def is_correct_answer(question, user_answer):
    expected = str(question["answer"]).strip().lower()
    actual = str(user_answer).strip().lower()
    return expected == actual


def ask_feedback_rating():
    while True:
        raw = input("Rate this question (1-5): ").strip()
        if raw in {"1", "2", "3", "4", "5"}:
            return int(raw)
        print("Invalid input. Please enter a valid option.")


def update_feedback(feedback_store, question, rating):
    qid = question_id(question)
    item = feedback_store.get(qid, {"count": 0, "sum": 0})
    item["count"] += 1
    item["sum"] += rating
    feedback_store[qid] = item


def run_quiz_round(username, questions, feedback_store):
    correct = 0
    wrong = 0
    weighted_score = 0
    per_difficulty = {"easy": {"right": 0, "total": 0}, "medium": {"right": 0, "total": 0}, "hard": {"right": 0, "total": 0}}

    for index, question in enumerate(questions, start=1):
        print(f"\nQuestion #{index} out of {len(questions)}")
        print(f"Category: {question['category']} | Difficulty: {question['difficulty']}")
        print(question["question"])

        user_answer = get_answer_from_user(question)
        difficulty = normalize_difficulty(str(question["difficulty"])) or "easy"
        per_difficulty[difficulty]["total"] += 1

        if is_correct_answer(question, user_answer):
            print("Correct!")
            correct += 1
            per_difficulty[difficulty]["right"] += 1
            weighted_score += DIFFICULTY_WEIGHTS.get(difficulty, 1)
        else:
            print(f"Wrong. Correct answer: {question['answer']}")
            wrong += 1

        rating = ask_feedback_rating()
        update_feedback(feedback_store, question, rating)

    total_score = correct
    print("\nQuiz complete!")
    print("Detailed analysis:")
    print(f"Total score: {total_score}")
    print(f"Correct answers: {correct}")
    print(f"Wrong answers: {wrong}")
    print(f"Weighted score: {weighted_score}")

    for diff in ("easy", "medium", "hard"):
        total = per_difficulty[diff]["total"]
        if total > 0:
            right = per_difficulty[diff]["right"]
            pct = (right / total) * 100
            print(f"{diff.title()} accuracy: {right}/{total} ({pct:.1f}%)")

    return {
        "username": username,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "questions": len(questions),
        "correct": correct,
        "wrong": wrong,
        "total_score": total_score,
        "weighted_score": weighted_score,
    }


def select_questions_by_filters(all_questions, feedback_store):
    categories = sorted({q["category"] for q in all_questions})
    difficulties = sorted({str(q["difficulty"]).lower() for q in all_questions})

    print("\nAvailable categories:")
    print(", ".join(categories))
    category_filter = input("Enter category to target (or press Enter for all): ").strip()

    print("\nAvailable difficulty levels:")
    print(", ".join(difficulties))
    difficulty_filter = input("Enter difficulty to target (or press Enter for all): ").strip().lower()

    filtered = []
    for q in all_questions:
        cat_ok = (not category_filter) or (q["category"].lower() == category_filter.lower())
        diff_ok = (not difficulty_filter) or (str(q["difficulty"]).lower() == difficulty_filter)
        if cat_ok and diff_ok:
            filtered.append(q)

    if not filtered:
        print("No questions matched the selected filters. Using all questions instead.")
        filtered = list(all_questions)

    count = ask_question_count(len(filtered))
    return weighted_sample_without_replacement(filtered, count, feedback_store)


def should_continue():
    while True:
        choice = input("\nDo you want to continue with more quiz questions? (y/n): ").strip().lower()
        if choice in {"y", "yes"}:
            return True
        if choice in {"n", "no"}:
            return False
        print("Invalid input. Please enter a valid option.")


def main():
    print_dragon_banner()
    print("Welcome to the Python Quiz App!")

    questions = load_and_validate_questions()
    if questions is None:
        return

    username = authenticate_user()
    history = load_secure_dat(HISTORY_FILE, [])
    if not isinstance(history, list):
        history = []
    feedback = load_secure_dat(FEEDBACK_FILE, {})
    if not isinstance(feedback, dict):
        feedback = {}

    while True:
        selected = select_questions_by_filters(questions, feedback)
        result = run_quiz_round(username, selected, feedback)
        history.append(result)
        save_secure_dat(HISTORY_FILE, history)
        save_secure_dat(FEEDBACK_FILE, feedback)
        if not should_continue():
            print("Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting.")
        os._exit(0)
