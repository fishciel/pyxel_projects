# Flashcard Study App

A simple flashcard application built with Python and Pyxel for studying and memorizing content.

## Features

- Create multiple flashcard sets
- Add, edit, and delete flashcards
- Practice mode with answer reveal
- Import flashcards from text files
- Intuitive user interface with keyboard and mouse support
- Text cursor navigation for easy editing
- Scrolling through large card sets

## Project Structure

```
flashcard_app/
├── main.py               # Main entry point
├── db.py                 # Database operations
├── app_state.py          # Application state enum
├── flashcard_app.py      # Main application class
├── ui_renderer.py        # UI rendering functions
├── input_handler.py      # Input handling utilities
├── screen_handlers.py    # Screen-specific logic
├── add_back_button.py    # Back button component
└── README.md             # Documentation
```

## Key Controls

### Global Controls
- **ESC**: Exit application (with confirmation)
- **Back Button**: Navigate back to previous screen

### Viewing Sets
- **Arrow Keys**: Scroll through sets
- **Mouse Click**: Select a set

### Viewing Cards
- **Arrow Keys**: Scroll through cards
- **Mouse Wheel**: Scroll through cards
- **P**: Practice mode
- **A**: Add new card
- **I**: Import cards from file
- **Mouse Click**: Edit card or delete (X button)

### Practice Mode
- **Space**: Reveal/hide answer
- **Left/Right Arrows**: Navigate through cards

### Card Editing
- **Arrow Keys**: Move cursor within text
- **Home/End**: Jump to start/end of text
- **Ctrl+Left/Right**: Navigate by words
- **Backspace/Delete**: Delete characters
- **Tab**: Switch between question and answer fields
- **Enter**: Save or move to next field

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

## Text Editing Features

The application includes a sophisticated text editing system that allows:
- Moving the cursor with arrow keys
- Jumping to word boundaries with Ctrl+arrow keys
- Positioning the cursor with mouse clicks
- Handling multi-line text with proper wrapping
- Preserving cursor position across text edits

## Development Notes

- The codebase is modular and organized for maintainability
- The text wrapping algorithm optimizes space usage for displaying flashcard content
- Navigation has been improved with dedicated back buttons and intuitive keyboard controls
- All text input fields support proper cursor navigation for easy editing
- Scrolling support enables handling large numbers of flashcards