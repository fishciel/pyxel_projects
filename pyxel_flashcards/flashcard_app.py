import pyxel
from app_state import AppState
import ui_renderer as ui
import screen_handlers as screens
from add_back_button import is_back_button_clicked
from input_handler import TextInputState

class FlashcardApp:
    def __init__(self, db):
        """Initialize the Pyxel application with a database instance."""
        # Initialize Pyxel with larger dimensions for better readability
        pyxel.init(400, 300, title="Flashcard Study App")
        
        # Store database instance
        self.db = db
        
        # Application state
        self.state = AppState.MAIN_MENU
        self.current_set_id = None
        self.current_set_name = ""
        self.cards = []
        self.card_index = 0
        self.show_answer = False
        self.show_exit_confirmation = False
        
        # Text input variables with cursor support
        self.input_state = TextInputState("")  # For general text input
        self.input_state_question = TextInputState("")  # For question field
        self.input_state_answer = TextInputState("")  # For answer field
        self.input_field = "set_name"  # Can be "set_name", "question", "answer"
        self.new_card = {"question": "", "answer": ""}
        
        # UI variables
        self.scroll_y = 0
        self.max_sets_visible = 8
        self.cards_scroll_y = 0
        self.max_cards_visible = 8  # Maximum cards visible on view cards screen
        self.sets = []
        self.back_button_area = None
        
        # Start the application
        pyxel.run(self.update, self.draw)
    
    def load_sets(self):
        """Load all flashcard sets from the database."""
        self.sets = self.db.get_all_sets()
    
    def load_cards(self, set_id):
        """Load all flashcards for a specific set."""
        self.cards = self.db.get_cards_for_set(set_id)
        self.card_index = 0
        self.show_answer = False
        self.cards_scroll_y = 0  # Reset scroll position
    
    def import_cards_from_file(self, filename, set_id):
        """Import flashcards from a text file in the format 'Q: {question} A: {answer}'."""
        try:
            with open(filename, 'r') as file:
                content = file.read()
                
                # Split content into individual cards
                cards = content.split("\n\n")
                
                for card in cards:
                    if "Q:" in card and "A:" in card:
                        q_part = card.split("A:")[0].strip()
                        a_part = card.split("A:")[1].strip()
                        
                        question = q_part.replace("Q:", "").strip()
                        answer = a_part.strip()
                        
                        if question and answer:
                            self.db.add_card(set_id, question, answer)
                
                return True
        except Exception as e:
            print(f"Error importing cards: {e}")
            return False
    
    def update(self):
        """Update game logic."""
        # ESC key now only handles application exit
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            if self.state == AppState.MAIN_MENU:
                # In main menu, ESC shows exit confirmation
                self.show_exit_confirmation = True if not hasattr(self, 'show_exit_confirmation') else not self.show_exit_confirmation
            else:
                # Store current state to return to after canceling exit
                self.previous_state = self.state
                self.state = AppState.MAIN_MENU
                self.show_exit_confirmation = True
        
        # Handle exit confirmation
        if hasattr(self, 'show_exit_confirmation') and self.show_exit_confirmation:
            if pyxel.btnp(pyxel.KEY_Y):  # Y to confirm exit
                pyxel.quit()
            elif pyxel.btnp(pyxel.KEY_N) or pyxel.btnp(pyxel.KEY_B):  # N or B to cancel exit
                self.show_exit_confirmation = False
                # Return to previous state if not already in main menu
                if hasattr(self, 'previous_state') and self.state == AppState.MAIN_MENU:
                    self.state = self.previous_state
                    delattr(self, 'previous_state')
            return  # Skip other updates while showing confirmation
        
        # Check if back button was clicked (set in draw method)
        if self.back_button_area and is_back_button_clicked(self.back_button_area):
            if self.state == AppState.VIEW_SETS:
                self.state = AppState.MAIN_MENU
            elif self.state in [AppState.VIEW_CARDS, AppState.PRACTICE_CARDS, AppState.ADD_CARD, AppState.EDIT_CARD]:
                self.state = AppState.VIEW_SETS
            elif self.state == AppState.CREATE_SET:
                self.state = AppState.MAIN_MENU
            elif self.state == AppState.IMPORT_CARDS:
                self.state = AppState.VIEW_CARDS
            
            # Skip the rest of the update to prevent any text input processing
            return
            
        # State-specific updates
        if self.state == AppState.MAIN_MENU:
            screens.update_main_menu(self)
        elif self.state == AppState.VIEW_SETS:
            screens.update_view_sets(self)
        elif self.state == AppState.CREATE_SET:
            screens.update_create_set(self)
        elif self.state == AppState.VIEW_CARDS:
            screens.update_view_cards(self)
        elif self.state == AppState.PRACTICE_CARDS:
            screens.update_practice_cards(self)
        elif self.state == AppState.ADD_CARD:
            screens.update_add_card(self)
        elif self.state == AppState.EDIT_CARD:
            screens.update_edit_card(self)
        elif self.state == AppState.IMPORT_CARDS:
            screens.update_import_cards(self)
    
    def draw(self):
        """Draw the current screen."""
        pyxel.cls(0)
        
        # Reset back button area
        self.back_button_area = None
        
        if self.state == AppState.MAIN_MENU:
            ui.draw_main_menu(self.show_exit_confirmation)
        elif self.state == AppState.VIEW_SETS:
            self.back_button_area = ui.draw_view_sets(self.sets, self.scroll_y, self.max_sets_visible)
        elif self.state == AppState.CREATE_SET:
            self.back_button_area = ui.draw_create_set_with_cursor(self.input_state)
        elif self.state == AppState.VIEW_CARDS:
            # Pass scroll position and max visible cards
            self.back_button_area = ui.draw_view_cards(
                self.current_set_name, 
                self.cards, 
                self.cards_scroll_y, 
                self.max_cards_visible
            )
        elif self.state == AppState.PRACTICE_CARDS:
            self.back_button_area = ui.draw_practice_cards(self.cards, self.card_index, self.show_answer)
        elif self.state == AppState.ADD_CARD:
            self.back_button_area = ui.draw_add_card_with_cursor(
                self.current_set_name, self.input_field, 
                self.input_state_question, self.input_state_answer
            )
        elif self.state == AppState.EDIT_CARD:
            self.back_button_area = ui.draw_edit_card_with_cursor(
                self.current_set_name, self.input_field, 
                self.input_state_question, self.input_state_answer
            )
        elif self.state == AppState.IMPORT_CARDS:
            self.back_button_area = ui.draw_import_cards_with_cursor(self.current_set_name, self.input_state)
        
        # Draw the mouse cursor
        pyxel.pset(pyxel.mouse_x, pyxel.mouse_y, 7)