# Python Quiz App

A command-line Python quiz app with local account login that loads questions from a JSON bank, quizzes users interactively, computes difficulty-weighted scores and performance stats, stores history/feedback in non-human-readable files, and uses feedback to influence future question selection.

## Features

- Dragon-like terminal welcome banner for a playful first-time experience.
- Local user system: register and login with hashed passwords.
- Question bank loaded from `questions.json`.
- Supports 3 question types across multiple categories and difficulties:
  - `multiple_choice`
  - `true_false`
  - `short_answer`
- Questions are tagged by category (for example, Python Basics, Data Structures, OOP, Concurrency) and can be targeted by category/difficulty when starting a quiz.
- Difficulty-aware scoring (`easy`, `medium`, `hard` with different weights).
- Quiz history and question feedback persistence.
- Global quick exit: type `goquit` at any prompt to exit safely.

## Project Structure

- `quiz.py` - main CLI entry point
- `questions.json` - question bank (JSON format)
- `users.json` - local user database (hashed credentials)
- `history.dat` - historical quiz records
- `feedback.dat` - question preference/feedback records
- `SPEC.md` - project specification

## Requirements

- Python 3.9+ (3.10+ recommended)

No external dependencies are required (standard library only).

## How to Start

From the project root:

```bash
python quiz.py
```

If your system uses `python3`:

```bash
python3 quiz.py
```

## Basic Usage Flow

1. Launch app.
2. Register or login.
3. Choose quiz count and optional category/difficulty filters.
4. Answer questions.
5. Rate each question (1-5) after seeing the correct answer.
6. Review score summary and continue or exit.

## Question Bank Format

`questions.json` uses:

```json
{
  "questions": [
    {
      "question": "What keyword is used to define a function in Python?",
      "type": "multiple_choice",
      "options": ["func", "define", "def", "function"],
      "answer": "def",
      "category": "Python Basics",
      "difficulty": "easy"
    }
  ]
}
```

Notes:
- `multiple_choice` must include an `options` array.
- `true_false` answers should be `true` or `false` (stored as strings in this project).
- `short_answer` compares text answers case-insensitively.

## Error Handling (Implemented)

- Missing `questions.json`:
  - `Error: questions.json not found.`
- Invalid or empty `questions.json`:
  - `Error: Invalid format of questions.json.`
- Invalid user input:
  - `Invalid input. Please enter a valid option.`
- Login failure:
  - `Login failed. Please try again.`
- Requesting too many questions:
  - `Requested number exceeds available questions. Will use maximum available.`