from db import FlashcardDB
from flashcard_app import FlashcardApp


def main():
    """Initialize database and start the application."""
    # Create database instance
    db = FlashcardDB()
    
    # Create and run application
    app = FlashcardApp(db)


if __name__ == "__main__":
    main()