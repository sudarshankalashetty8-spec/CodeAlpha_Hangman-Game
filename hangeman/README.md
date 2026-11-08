# WordQuest — Hangman Website

A responsive Hangman word game website inspired by the Python-based Gallows project at https://github.com/Chennaipy/hangman. This is an original web implementation of the classic word-guessing concept, with category selection, hints, keyboard and physical-key input, mistake tracking, and win/loss states.

## Run locally

1. Install Python 3.9 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the website:
   ```bash
   python app.py
   ```
6. Open http://127.0.0.1:5000 in your browser.

## Notes

- Game state is stored in the Flask session.
- Change `app.secret_key` before deploying publicly.
- This project is an independent implementation; the referenced repository is credited as inspiration. See its BSD-2-Clause license at the source repository for the original project's terms.
