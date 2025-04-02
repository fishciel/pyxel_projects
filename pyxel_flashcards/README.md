# Flashcard Study App

A simple flashcard application built with Python and Pyxel for studying and memorizing content.

## Features

- Create multiple flashcard sets
- Add, edit, and delete flashcards
- Practice mode with answer reveal
- Import flashcards from text files
- Intuitive user interface with keyboard and mouse support

## Project Structure

```
flashcard_app/
├── main.py             # Application entry point
├── db.py               # Database operations
├── app_state.py        # Application state enum
├── flashcard_app.py    # Core application class
├── ui_renderer.py      # UI rendering functions
├── input_handler.py    # Input handling utilities
├── screen_handlers.py  # Screen-specific logic
├── add_back_button.py  # Back button component
└── README.md           # Documentation
```

## Key Controls

- **ESC**: Exit application (with confirmation)
- **B**: Navigate back to previous screen
- **Arrow Keys**: Navigate through cards in practice mode
- **SPACE**: Reveal/hide answer in practice mode
- **TAB**: Switch between question and answer fields when editing
- **ENTER**: Confirm current action

## Getting Started

1. Install Python 3.6 or higher
2. Install Pyxel: `pip install pyxel`
3. Run the application: `python main.py`

## Importing Flashcards

You can import flashcards from text files using the following format:

```
Q: What is the capital of France?
A: Paris

Q: What is the largest planet in our solar system?
A: Jupiter
```

Cards should be separated by blank lines, and each card should have lines starting with "Q:" for the question and "A:" for the answer.

## Database

The application uses SQLite to store flashcard sets and cards. The database file `flashcards.db` will be created in the same directory as the application.

## Development Notes

- The codebase has been refactored for modularity and maintainability
- The text wrapping algorithm optimizes space usage for displaying flashcard content
- Navigation has been improved with dedicated back buttons and better keyboard controls