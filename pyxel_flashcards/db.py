import sqlite3
import os


class FlashcardDB:
    def __init__(self, db_path="flashcards.db"):
        """Initialize database connection and setup tables if needed."""
        self.db_path = db_path
        create_tables = not os.path.exists(self.db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        if create_tables:
            self._create_tables()
    
    def _create_tables(self):
        """Create the necessary database tables."""
        self.cursor.execute('''
        CREATE TABLE flashcard_sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            set_id INTEGER,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (set_id) REFERENCES flashcard_sets(id)
        )
        ''')
        
        self.conn.commit()
    
    def get_all_sets(self):
        """Get all flashcard sets."""
        self.cursor.execute("SELECT id, name FROM flashcard_sets ORDER BY name")
        return self.cursor.fetchall()
    
    def get_cards_for_set(self, set_id):
        """Get all flashcards for a specific set."""
        self.cursor.execute("SELECT id, question, answer FROM flashcards WHERE set_id = ?", (set_id,))
        return self.cursor.fetchall()
    
    def create_set(self, name):
        """Create a new flashcard set."""
        self.cursor.execute("INSERT INTO flashcard_sets (name) VALUES (?)", (name,))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def add_card(self, set_id, question, answer):
        """Add a new flashcard to a set."""
        self.cursor.execute(
            "INSERT INTO flashcards (set_id, question, answer) VALUES (?, ?, ?)",
            (set_id, question, answer)
        )
        self.conn.commit()
    
    def update_card(self, card_id, question, answer):
        """Update an existing flashcard."""
        self.cursor.execute(
            "UPDATE flashcards SET question = ?, answer = ? WHERE id = ?",
            (question, answer, card_id)
        )
        self.conn.commit()
    
    def delete_card(self, card_id):
        """Delete a flashcard."""
        self.cursor.execute("DELETE FROM flashcards WHERE id = ?", (card_id,))
        self.conn.commit()
    
    def delete_set(self, set_id):
        """Delete a flashcard set and all its cards."""
        self.cursor.execute("DELETE FROM flashcards WHERE set_id = ?", (set_id,))
        self.cursor.execute("DELETE FROM flashcard_sets WHERE id = ?", (set_id,))
        self.conn.commit()
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()