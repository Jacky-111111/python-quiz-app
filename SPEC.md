# SPEC.md

## 1. Overview
This is a command-line Python quiz app with a local login system that import Python-related questions from a question bank (a JSON file), quizzes users, tracks scores and performance statistics in a non-human-readable format, allows users to provide feedback on questions to influence future quiz selections, and saves historical records.

## 2. App Flow
The app greets the user at first, with a cute interface that mimics the 15-112 dragon in the terminal. Guide the user to login (or register a new account). Then, asks how many questions they want this time and is there any specific category/difficulty they wish to target on. Then, the app selects questions randomly under the requirement from the question bank (make sure to label the number of questions, like saying question #3 out of 5). The user answers with either typed or selected options according to the question type. The app records the scores (more difficult questions have higher weights) and the numbers of correct and wrong an answers, and offers a detailed analysis when the quiz ends. App asks user whether to continue with more quiz questions or exit.

## 3. Question Bank Format
The questions are in the JSON format.
Examples:
<!-- Some of the questions directly copied from the 15-113 website -->
{
  "questions": [
    {
      "question": "What keyword is used to define a function in Python?",
      "type": "multiple_choice",
      "options": ["func", "define", "def", "function"],
      "answer": "def",
      "category": "Python Basics",
      "difficulty": "easy"
    },
    {
      "question": "A list in Python is immutable.",
      "type": "true_false",
      "answer": "false",
      "category": "Data Structures",
      "difficulty": "medium"
    },
    {
      "question": "What built-in function returns the number of items in a list?",
      "type": "short_answer",
      "answer": "len",
      "category": "Python Basics",
      "difficulty": "easy"
    },
    {
      "question": "Which data type is used to store True or False values in Python?",
      "type": "multiple_choice",
      "options": ["int", "str", "bool", "list"],
      "answer": "bool",
      "category": "Python Basics",
      "difficulty": "easy"
    },
      "question": "What symbol is used to start a comment in Python?",
      "type": "multiple_choice",
      "options": ["//", "#", "/*", "--"],
      "answer": "#",
      "category": "Python Basics",
      "difficulty": "easy"
  ]
}

## 4. File Structure
- quiz.py - main program entry
- questions.json - question bank in json format
- users.json - local database that stores usernames and passwords securely
- history.dat - stores score history securely
- feedback.dat - sotres question preferences securely
- SPEC.md

## 5. Login and Security
This local login system that allows users to login with a username and password (or register a new account when they wish). The passwords should be securely stored.

## 6. Score Tracking and Statistics
The number of correct and wrong answers are stored. Score is based on the difficulty level of the questions, with the more difficult question weighting more. 

## 7. Question Feedback System
Everytime the user finishes answer a question, the correct answer is shown, and gives the user options to rate their likeness on the question from 1-5.

## 8. Extension Feature
Difficulty level that affects scoring.

## 9. Error Handling
- Missing questions.json file
Print: "Error: questions.json not found."
Exit the program with code 1.

- Inappropriate formed questions.json file or empty file
Print: "Error: Invalid format of questions.json."
Exit safely without crashing.

- Invalid user input
If the user enters a non-integer or unsupported option for the question, print: "Invalid input. Please enter a valid option."
Directly the user to re-answer the question.

- Login failure
If username does not exist or password is wrong, print: "Login failed. Please try again."
Do not crashing; allow reentry.

- Requesting more questions than available
Print: "Requested number exceeds available questions. Will use maximum available."
Continue with all available questions. Use the maximum number of existing questions.

## 10. Acceptance Criteria

1.	Running python quiz.py starts the app without errors.
2.	A new user can register and then successfully log in with the correct credentials.
3.	Passwords are stored securely (hashed).
4.	The app correctly loads questions from questions.json and supports all three types: multiple_choice, true_false, and short_answer.
5.	The app handles invalid input gracefully without crashing and redirect the user.
6.	After completing a quiz, the user receives: total score, number of correct/wrong answers, weighted score based on difficulty.
7.	Question feedback (1–5 rating) is recorded and influences future question selection.
8.	The app handles missing or invalid files according to the error handling rules listed.
9.	The difficulty-based scoring system correctly assigns higher points to harder questions.