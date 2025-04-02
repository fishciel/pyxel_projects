from add_back_button import is_back_button_clicked
import pyxel
from app_state import AppState
from input_handler import TextInputState, handle_text_input_with_cursor, is_mouse_in_area

def update_main_menu(app):
    """Handle main menu interactions."""
    # Skip normal menu handling if showing exit confirmation
    if hasattr(app, 'show_exit_confirmation') and app.show_exit_confirmation:
        return
        
    if pyxel.btnp(pyxel.KEY_V) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and is_mouse_in_area(90, 70, 150, 80):
        app.load_sets()
        app.state = AppState.VIEW_SETS
    elif pyxel.btnp(pyxel.KEY_C) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and is_mouse_in_area(90, 90, 150, 100):
        # Initialize text input state with empty text
        app.input_state = TextInputState("")
        app.state = AppState.CREATE_SET

def update_view_sets(app):
    """Handle set selection screen interactions."""
    if app.sets:
        # Scrolling
        if pyxel.btnp(pyxel.KEY_UP):
            app.scroll_y = max(0, app.scroll_y - 1)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            app.scroll_y = min(len(app.sets) - app.max_sets_visible, app.scroll_y)
        
        # Mouse clicking on sets
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for i, (set_id, set_name) in enumerate(app.sets[app.scroll_y:app.scroll_y + app.max_sets_visible]):
                if is_mouse_in_area(20, 40 + i * 15, 200, 50 + i * 15):
                    app.current_set_id = set_id
                    app.current_set_name = set_name
                    app.load_cards(set_id)
                    app.state = AppState.VIEW_CARDS
                    break

def update_create_set(app):
    """Handle creating a new flashcard set."""
    # Use the new input handling
    handle_text_input_with_cursor(app.input_state, 20, 60, 10, 70)
    
    if pyxel.btnp(pyxel.KEY_RETURN):
        if app.input_state.text.strip():
            set_id = app.db.create_set(app.input_state.text)
            app.current_set_id = set_id
            app.current_set_name = app.input_state.text
            app.cards = []
            app.state = AppState.VIEW_CARDS
            # Reset input state for next use
            app.input_state = TextInputState("")

def update_view_cards(app):
    """Handle card viewing screen interactions."""
    # Handle scrolling with arrow keys
    if pyxel.btnp(pyxel.KEY_UP):
        app.cards_scroll_y = max(0, app.cards_scroll_y - 1)
    elif pyxel.btnp(pyxel.KEY_DOWN):
        # Calculate maximum scroll based on number of cards
        max_scroll = max(0, len(app.cards) - app.max_cards_visible)
        app.cards_scroll_y = min(max_scroll, app.cards_scroll_y + 1)
    
    # Handle mouse wheel scrolling
    if pyxel.mouse_wheel != 0:
        app.cards_scroll_y = max(0, min(len(app.cards) - app.max_cards_visible, 
                                        app.cards_scroll_y - pyxel.mouse_wheel))
    
    # Other existing functionality
    if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and is_mouse_in_area(20, 265, 80, 275):
        if app.cards:
            app.card_index = 0
            app.show_answer = False
            app.state = AppState.PRACTICE_CARDS
    elif pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and is_mouse_in_area(120, 265, 180, 275):
        app.new_card = {"question": "", "answer": ""}
        app.input_field = "question"
        # Initialize text input state for question
        app.input_state_question = TextInputState("")
        app.input_state_answer = TextInputState("")
        app.state = AppState.ADD_CARD
    elif pyxel.btnp(pyxel.KEY_I) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and is_mouse_in_area(220, 265, 280, 275):
        # Initialize text input state for import
        app.input_state = TextInputState("")
        app.state = AppState.IMPORT_CARDS
    
    # Card deletion - updated for scrolling
    if app.cards and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        for i, (card_id, question, answer) in enumerate(app.cards[app.cards_scroll_y:app.cards_scroll_y + app.max_cards_visible]):
            y_pos = 75 + i * 20
            if is_mouse_in_area(380, y_pos, 390, y_pos + 10):
                app.db.delete_card(card_id)
                app.load_cards(app.current_set_id)
                # Adjust scroll position if we deleted the last card
                if app.cards_scroll_y > 0 and app.cards_scroll_y >= len(app.cards) - app.max_cards_visible:
                    app.cards_scroll_y = max(0, len(app.cards) - app.max_cards_visible)
                break
    
    # Card editing - updated for scrolling
    if app.cards and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        for i, (card_id, question, answer) in enumerate(app.cards[app.cards_scroll_y:app.cards_scroll_y + app.max_cards_visible]):
            y_pos = 75 + i * 20
            # Clicking on question or answer area allows editing
            if is_mouse_in_area(20, y_pos, 370, y_pos + 15):
                app.new_card = {"id": card_id, "question": question, "answer": answer}
                app.input_field = "question"
                # Initialize text input states with existing content
                app.input_state_question = TextInputState(question)
                app.input_state_answer = TextInputState(answer)
                app.state = AppState.EDIT_CARD
                break

def update_practice_cards(app):
    """Handle flashcard practice mode."""
    if not app.cards:
        app.state = AppState.VIEW_CARDS
        return
    
    if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        app.show_answer = not app.show_answer
    
    if pyxel.btnp(pyxel.KEY_RIGHT):
        app.card_index = (app.card_index + 1) % len(app.cards)
        app.show_answer = False
    
    if pyxel.btnp(pyxel.KEY_LEFT):
        app.card_index = (app.card_index - 1) % len(app.cards)
        app.show_answer = False

def update_add_card(app):
    """Handle adding a new flashcard."""
    # Handle input based on current field
    if app.input_field == "question":
        handle_text_input_with_cursor(app.input_state_question, 15, 60, 10, 70)
    else:  # answer field
        handle_text_input_with_cursor(app.input_state_answer, 15, 160, 10, 70)
    
    if pyxel.btnp(pyxel.KEY_TAB):
        if app.input_field == "question":
            app.input_field = "answer"
        elif app.input_field == "answer":
            app.input_field = "question"
    
    if pyxel.btnp(pyxel.KEY_RETURN):
        if app.input_field == "question":
            app.input_field = "answer"
        elif app.input_field == "answer":
            question = app.input_state_question.text
            answer = app.input_state_answer.text
            
            if question.strip() and answer.strip():
                app.db.add_card(app.current_set_id, question, answer)
                app.load_cards(app.current_set_id)
                app.state = AppState.VIEW_CARDS

def update_edit_card(app):
    """Handle editing an existing flashcard."""
    # Handle input based on current field
    if app.input_field == "question":
        handle_text_input_with_cursor(app.input_state_question, 15, 60, 10, 70)
    else:  # answer field
        handle_text_input_with_cursor(app.input_state_answer, 15, 160, 10, 70)
    
    if pyxel.btnp(pyxel.KEY_TAB):
        if app.input_field == "question":
            app.input_field = "answer"
        elif app.input_field == "answer":
            app.input_field = "question"
    
    if pyxel.btnp(pyxel.KEY_RETURN):
        if app.input_field == "question":
            app.input_field = "answer"
        elif app.input_field == "answer":
            question = app.input_state_question.text
            answer = app.input_state_answer.text
            
            if question.strip() and answer.strip():
                app.db.update_card(app.new_card["id"], question, answer)
                app.load_cards(app.current_set_id)
                app.state = AppState.VIEW_CARDS

def update_import_cards(app):
    """Handle importing cards from a file."""
    # Use the new input handling
    handle_text_input_with_cursor(app.input_state, 20, 60, 10, 70)
    
    if pyxel.btnp(pyxel.KEY_RETURN):
        if app.input_state.text.strip():
            success = app.import_cards_from_file(app.input_state.text, app.current_set_id)
            if success:
                app.load_cards(app.current_set_id)
                app.state = AppState.VIEW_CARDS