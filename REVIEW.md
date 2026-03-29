1. [PASS] **Acceptance #1: `python quiz.py` starts the app without immediate startup errors.**  
   Evidence: App entrypoint is present and calls `main()` under `if __name__ == "__main__"` in `quiz.py:420-425`; startup banner and welcome flow are executed in `quiz.py:394-399`.

2. [PASS] **Acceptance #2: New user registration and subsequent login are implemented correctly.**  
   Evidence: Registration path creates a salted+hashed password and writes it to `users.json` in `quiz.py:190-200`; login verifies credentials and loops on failure in `quiz.py:202-210`.

3. [PASS] **Acceptance #3: Passwords are stored hashed (securely).**  
   Evidence: Password hashing uses `hashlib.pbkdf2_hmac("sha256", ..., 200_000)` with random 16-byte salt in `quiz.py:43-47`; verification uses constant-time comparison in `quiz.py:58-59`; stored format is `salt$digest` in `quiz.py:197`.

4. [PASS] **Acceptance #4: Questions load from `questions.json` and all three types are supported.**  
   Evidence: Loader validates required schema and allows only `multiple_choice`, `true_false`, `short_answer` in `quiz.py:101-140`; answer input handlers for each type are implemented in `quiz.py:239-279`.

5. [PASS] **Acceptance #5: Invalid input is handled gracefully for quiz interaction and menu flows.**  
   Evidence: Invalid answer/menu inputs are rejected with the required message and re-prompted across handlers in `quiz.py:171-177`, `quiz.py:223-231`, `quiz.py:244-253`, `quiz.py:266-271`, `quiz.py:273-278`, `quiz.py:287-293`, `quiz.py:383-390`.

6. [PASS] **Acceptance #6: End-of-quiz report includes total score, correct/wrong counts, and weighted score.**  
   Evidence: Final analysis prints `Total score`, `Correct answers`, `Wrong answers`, and `Weighted score` in `quiz.py:331-337`; result payload includes these values in `quiz.py:345-353`.

7. [PASS] **Acceptance #7: Feedback rating (1–5) is recorded and influences future question selection.**  
   Evidence: Rating is collected each question in `quiz.py:287-293` and recorded in `quiz.py:295-301`; selection bias uses feedback-derived weights in `quiz.py:148-168` and is applied in `quiz.py:379-380`.

8. [PASS] **Acceptance #8: Missing/invalid `questions.json` handling matches the spec behavior.**  
   Evidence: Missing file prints `Error: questions.json not found.` and exits code 1 in `quiz.py:102-104`; invalid/empty JSON prints `Error: Invalid format of questions.json.` and returns safely in `quiz.py:106-123`.

9. [PASS] **Acceptance #9: Difficulty-based scoring assigns higher weight to harder questions.**  
   Evidence: Difficulty weights are `easy=1`, `medium=2`, `hard=3` in `quiz.py:19-23`; weighted score increments by difficulty on correct answers in `quiz.py:315-323`.

10. [FAIL] **Security concern: unsafe deserialization via `pickle` for `.dat` files.**  
    Risk: `load_secure_dat()` decodes Base64 then calls `pickle.loads(...)` on file content in `quiz.py:88-89`. A tampered `history.dat` or `feedback.dat` can execute arbitrary code during load. This is a high-severity local code execution risk.  
    Recommendation: Replace pickle-based persistence with safe formats (`json`), with explicit schema validation.

11. [WARN] **Data integrity issue: corrupted `.dat` files are silently overwritten, causing potential data loss.**  
    Evidence: On decode/load errors, code immediately rewrites default values in `quiz.py:90-92`; empty file also gets overwritten in `quiz.py:85-87`.  
    Impact: History/feedback can be erased without user warning or backup.

12. [WARN] **Missing EOF handling can crash the app on unexpected input stream termination.**  
    Evidence: The app calls `input(...)` in many places (e.g., `quiz.py:173`, `quiz.py:188`, `quiz.py:224`, `quiz.py:245`, `quiz.py:267`) but only catches `KeyboardInterrupt` in `quiz.py:421-425`; `EOFError` is not handled.  
    Impact: Piped/automated runs or terminal EOF (`Ctrl-D`) can terminate with traceback.

13. [WARN] **Question schema validation is incomplete for logical correctness.**  
    Evidence: For multiple-choice questions, loader verifies `options` exists and is non-empty (`quiz.py:135-138`) but does not verify `answer` is one of the listed options.  
    Impact: Invalid banks can pass validation and create impossible/incorrectly graded questions.

14. [WARN] **Code quality: repeated hard-coded error message and repeated input-validation patterns reduce maintainability.**  
    Evidence: `"Invalid input. Please enter a valid option."` is duplicated in many blocks (`quiz.py:176`, `quiz.py:193`, `quiz.py:212`, `quiz.py:230`, `quiz.py:247`, `quiz.py:251`, `quiz.py:269`, `quiz.py:276`, `quiz.py:292`, `quiz.py:390`).  
    Recommendation: Centralize prompt validation/error reporting helpers to reduce repetition and drift.
