import pyxel
from add_back_button import draw_back_button

def wrap_text(text, max_chars_per_line):
    """Wrap text to fit within given character limit per line.
    
    This improved version will fill lines to their maximum length
    before starting a new line and handle very long words better.
    """
    if not text:
        return [""]
    
    # Split into words
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        # Check if adding this word would exceed the line limit
        test_line = current_line + (" " if current_line else "") + word
        
        if len(test_line) <= max_chars_per_line:
            # Word fits, add it to the current line
            current_line = test_line
        elif len(word) > max_chars_per_line:
            # Word itself is too long, need to break it
            if current_line:
                lines.append(current_line)
                current_line = ""
            
            # Break the long word across multiple lines
            start = 0
            while start < len(word):
                # If we're at the beginning of a line, take as much of the word as possible
                if not current_line:
                    chunk_size = min(max_chars_per_line, len(word) - start)
                    chunk = word[start:start + chunk_size]
                    
                    if start + chunk_size < len(word):
                        # Add a hyphen if we're breaking in the middle of the word
                        # and have room for it
                        if chunk_size < max_chars_per_line:
                            chunk += "-"
                        lines.append(chunk)
                        current_line = ""
                    else:
                        current_line = chunk
                    
                    start += chunk_size
                else:
                    # If we already have content on the line, move to the next line
                    lines.append(current_line)
                    current_line = ""
        else:
            # Word doesn't fit on current line but can fit on a new line
            lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines if lines else [""]

def draw_box(x1, y1, x2, y2):
    """Draw a box with border for visual separation."""
    # Fill background
    for y in range(y1 + 1, y2):
        pyxel.line(x1 + 1, y, x2 - 1, y, 1)  # Dark blue background
    
    # Draw border
    pyxel.rectb(x1, y1, x2 - x1, y2 - y1, 5)  # Purple border

def draw_main_menu(show_exit_confirmation=False):
    """Draw the main menu screen."""
    pyxel.text(90, 50, "Flashcard Study App", 7)
    
    if show_exit_confirmation:
        # Draw exit confirmation dialog
        draw_box(60, 80, 340, 160)
        pyxel.text(110, 100, "Do you want to exit the application?", 7)
        pyxel.text(130, 130, "[Y]es        [N]o", 11)
    else:
        # Draw normal menu options
        pyxel.text(90, 70, "[V]iew Sets", 11)
        pyxel.text(90, 90, "[C]reate New Set", 11)
        pyxel.text(150, 130, "Exit: ESC", 13)
    
    return None  # Main menu doesn't have a back button

def draw_view_sets(sets, scroll_y, max_sets_visible):
    """Draw the sets selection screen."""
    pyxel.text(20, 20, "Flashcard Sets:", 7)
    
    if not sets:
        pyxel.text(20, 40, "No sets found. Create one!", 8)
    else:
        for i, (set_id, set_name) in enumerate(sets[scroll_y:scroll_y + max_sets_visible]):
            pyxel.text(20, 40 + i * 15, f"{set_name}", 11)
    
    # Draw back button at bottom of screen
    back_button_area = draw_back_button(20, 220)
    
    pyxel.text(20, 190, "Click BACK button to return to Main Menu", 13)
    pyxel.text(20, 250, "ESC: Exit Application", 8)
    
    return back_button_area

def draw_create_set(input_text):
    """Draw the create set screen."""
    pyxel.text(20, 20, "Create New Flashcard Set", 7)
    pyxel.text(20, 40, "Set Name:", 11)
    pyxel.text(20, 60, input_text, 7)
    pyxel.text(20, 80, "_" if pyxel.frame_count % 30 < 15 else "", 7)
    pyxel.text(20, 120, "Press ENTER to create", 13)
    
    # Draw back button
    back_button_area = draw_back_button(20, 220)
    pyxel.text(20, 190, "Click BACK to cancel", 13)
    pyxel.text(20, 250, "ESC: Exit Application", 8)
    
    return back_button_area

def draw_create_set_with_cursor(input_state):
    """Draw the create set screen with cursor support."""
    pyxel.text(20, 20, "Create New Flashcard Set", 7)
    pyxel.text(20, 40, "Set Name:", 11)
    
    # Draw box for text input
    draw_box(10, 50, 390, 90)
    
    # Get text with cursor
    text_lines = wrap_text(input_state.text, 70)
    
    # Draw text lines
    for i, line in enumerate(text_lines[:3]):  # Limit to 3 lines
        pyxel.text(15, 60 + i * 10, line, 7)
    
    # Draw cursor
    if pyxel.frame_count % 30 < 15:
        cursor_x = 15
        cursor_y = 60
        
        # Find cursor position based on wrapped text
        char_count = 0
        for i, line in enumerate(text_lines):
            if char_count + len(line) >= input_state.cursor_pos:
                # Cursor is in this line
                line_pos = input_state.cursor_pos - char_count
                cursor_x = 15 + line_pos * 4  # Assuming each char is 4 pixels wide
                cursor_y = 60 + i * 10
                break
            char_count += len(line)
        
        pyxel.text(cursor_x, cursor_y, "_", 7)
    
    pyxel.text(20, 120, "Press ENTER to create", 13)
    
    # Draw back button
    back_button_area = draw_back_button(20, 220)
    pyxel.text(20, 190, "Click BACK to cancel", 13)
    pyxel.text(20, 250, "ESC: Exit Application", 8)
    
    # Draw instructions for cursor navigation
    pyxel.text(20, 160, "Arrow keys: Move cursor | Home/End: Start/End of text", 5)
    
    return back_button_area

def draw_view_cards(current_set_name, cards, cards_scroll_y=0, max_cards_visible=8):
    """Draw the cards viewing screen with scrolling support."""
    pyxel.text(20, 20, f"Set: {current_set_name}", 7)
    
    if not cards:
        pyxel.text(20, 40, "No cards in this set yet.", 8)
    else:
        pyxel.text(20, 40, f"Cards (click to edit): {cards_scroll_y+1}-{min(cards_scroll_y+max_cards_visible, len(cards))} of {len(cards)}", 7)
        
        # Draw column headers
        pyxel.text(20, 55, "Question", 7)
        pyxel.text(280, 55, "Answer Preview", 7)
        pyxel.text(380, 55, "Del", 7)
        
        # Draw separator line
        for x in range(20, 380, 2):
            pyxel.pset(x, 65, 5)
        
        # Draw visible cards based on scroll position
        visible_cards = cards[cards_scroll_y:cards_scroll_y + max_cards_visible]
        for i, (card_id, question, answer) in enumerate(visible_cards):
            y_pos = 75 + i * 20
            
            # Question preview with improved formatting
            q_lines = wrap_text(question, 30)
            q_display = q_lines[0]
            if len(q_lines) > 1:
                q_display += "..."
            pyxel.text(20, y_pos, q_display, 11)
            
            # Answer preview 
            a_lines = wrap_text(answer, 12)
            a_display = a_lines[0]
            if len(a_lines) > 1:
                a_display += "..."
            pyxel.text(280, y_pos, a_display, 5)
            
            # Delete button
            pyxel.text(380, y_pos, "X", 8)
        
        # Draw scroll indicators if needed
        if len(cards) > max_cards_visible:
            # Up arrow if not at the top
            if cards_scroll_y > 0:
                pyxel.text(200, 55, "▲", 8)
            
            # Down arrow if not at the bottom
            if cards_scroll_y < len(cards) - max_cards_visible:
                pyxel.text(200, 235, "▼", 8)
                
            # Show scroll position indicator
            scroll_height = 170  # Height of the scrollable area
            visible_ratio = min(1.0, max_cards_visible / len(cards))
            scroll_thumb_height = max(15, int(scroll_height * visible_ratio))
            scroll_pos = int(scroll_height * (cards_scroll_y / max(1, len(cards) - max_cards_visible)))
            
            # Draw scroll track
            pyxel.line(395, 70, 395, 230, 1)
            
            # Draw scroll thumb
            for y in range(70 + scroll_pos, 70 + scroll_pos + scroll_thumb_height):
                pyxel.pset(395, y, 5)
    
    pyxel.text(20, 265, "[P]ractice", 11)
    pyxel.text(120, 265, "[A]dd Card", 11)
    pyxel.text(220, 265, "[I]mport", 11)
    
    # Draw back button
    back_button_area = draw_back_button(320, 265)
    pyxel.text(320, 285, "ESC: Exit", 8)
    
    # Add scrolling instructions
    if cards and len(cards) > max_cards_visible:
        pyxel.text(20, 245, "↑/↓: Scroll cards", 5)
    
    return back_button_area

def draw_practice_cards(cards, card_index, show_answer):
    """Draw the practice mode screen with improved text display."""
    if not cards:
        return None
    
    card_id, question, answer = cards[card_index]
    
    pyxel.text(20, 20, f"Card {card_index + 1}/{len(cards)}", 7)
    
    # Draw card box for question - increased size
    draw_box(10, 35, 390, 130)
    
    # Draw the question with improved wrapping and more lines
    lines = wrap_text(question, 70)  # Increased width for wrapping to use more horizontal space
    for i, line in enumerate(lines[:8]):  # Increased from 6 to 8 lines visible
        pyxel.text(15, 45 + i * 10, line, 11)  # Reduced vertical spacing between lines
    
    # Draw the answer area
    if show_answer:
        # Draw card box for answer - increased size
        draw_box(10, 140, 390, 260)
        
        pyxel.text(15, 150, "Answer:", 7)
        answer_lines = wrap_text(answer, 70)  # Increased width for wrapping
        for i, line in enumerate(answer_lines[:10]):  # Increased from 5 to 10 lines visible
            pyxel.text(15, 165 + i * 10, line, 14)  # Reduced vertical spacing between lines
    else:
        pyxel.text(20, 160, "Press SPACE to reveal answer", 13)
    
    pyxel.text(20, 275, "←/→: Navigate cards | SPACE: Reveal answer", 13)
    
    # Draw back button
    back_button_area = draw_back_button(320, 265)
    pyxel.text(320, 285, "ESC: Exit", 8)
    
    return back_button_area

def draw_add_card(current_set_name, input_text, input_field, new_card):
    """Draw the add card screen with improved text display."""
    pyxel.text(20, 20, f"Add Card to: {current_set_name}", 7)
    
    # Draw card boxes - made larger
    draw_box(10, 40, 390, 130)  # Question box
    draw_box(10, 140, 390, 230)  # Answer box
    
    if input_field == "question":
        pyxel.text(15, 45, "Question:", 11)
        
        # Display the question text with improved wrapping
        question_lines = wrap_text(input_text, 70)
        for i, line in enumerate(question_lines[:7]):  # Increased from 5 to 7 lines visible
            pyxel.text(15, 60 + i * 10, line, 7)  # Reduced spacing between lines
        
        # Only show cursor at the end of the last line
        if question_lines:
            last_line = question_lines[-1]
            cursor_x = 15 + len(last_line) * 4  # Approximate character width
            cursor_y = 60 + (len(question_lines) - 1) * 10
            
            # Make sure cursor is visible within the box
            if cursor_x > 380:
                cursor_x = 380
            
            if pyxel.frame_count % 30 < 15:
                pyxel.text(cursor_x, cursor_y, "_", 7)
        else:
            if pyxel.frame_count % 30 < 15:
                pyxel.text(15, 60, "_", 7)
        
        pyxel.text(15, 145, "Answer:", 8)
        answer_lines = wrap_text(new_card["answer"], 70)
        for i, line in enumerate(answer_lines[:7]):  # Increased visible lines
            pyxel.text(15, 160 + i * 10, line, 5)
    else:  # answer field
        pyxel.text(15, 45, "Question:", 8)
        question_lines = wrap_text(new_card["question"], 70)
        for i, line in enumerate(question_lines[:7]):
            pyxel.text(15, 60 + i * 10, line, 5)
        
        pyxel.text(15, 145, "Answer:", 11)
        answer_lines = wrap_text(input_text, 70)
        for i, line in enumerate(answer_lines[:7]):
            pyxel.text(15, 160 + i * 10, line, 7)
        
        # Only show cursor at the end of the last line
        if answer_lines:
            last_line = answer_lines[-1]
            cursor_x = 15 + len(last_line) * 4  # Approximate character width
            cursor_y = 160 + (len(answer_lines) - 1) * 10
            
            # Make sure cursor is visible within the box
            if cursor_x > 380:
                cursor_x = 380
            
            if pyxel.frame_count % 30 < 15:
                pyxel.text(cursor_x, cursor_y, "_", 7)
        else:
            if pyxel.frame_count % 30 < 15:
                pyxel.text(15, 160, "_", 7)
    
    pyxel.text(20, 240, "TAB to switch fields | ENTER to save", 13)
    
    # Draw back button
    back_button_area = draw_back_button(320, 240)
    pyxel.text(320, 260, "ESC: Exit", 8)
    
    return back_button_area

def draw_add_card_with_cursor(current_set_name, input_field, input_state_question, input_state_answer):
    """Draw the add card screen with cursor support."""
    pyxel.text(20, 20, f"Add Card to: {current_set_name}", 7)
    
    # Draw card boxes - made larger
    draw_box(10, 40, 390, 130)  # Question box
    draw_box(10, 140, 390, 230)  # Answer box
    
    if input_field == "question":
        pyxel.text(15, 45, "Question:", 11)
        
        # Display the question text with improved wrapping
        question_lines = wrap_text(input_state_question.text, 70)
        for i, line in enumerate(question_lines[:7]):  # Increased from 5 to 7 lines visible
            pyxel.text(15, 60 + i * 10, line, 7)  # Reduced spacing between lines
        
        # Draw cursor for question
        if pyxel.frame_count % 30 < 15:
            cursor_x = 15
            cursor_y = 60
            
            # Find cursor position based on wrapped text
            char_count = 0
            for i, line in enumerate(question_lines):
                if i >= 7:  # Don't check beyond visible lines
                    break
                if char_count + len(line) >= input_state_question.cursor_pos:
                    # Cursor is in this line
                    line_pos = input_state_question.cursor_pos - char_count
                    cursor_x = 15 + line_pos * 4  # Assuming each char is 4 pixels wide
                    cursor_y = 60 + i * 10
                    break
                char_count += len(line)
            
            pyxel.text(cursor_x, cursor_y, "_", 7)
        
        pyxel.text(15, 145, "Answer:", 8)
        answer_lines = wrap_text(input_state_answer.text, 70)
        for i, line in enumerate(answer_lines[:7]):  # Increased visible lines
            pyxel.text(15, 160 + i * 10, line, 5)
    else:  # answer field
        pyxel.text(15, 45, "Question:", 8)
        question_lines = wrap_text(input_state_question.text, 70)
        for i, line in enumerate(question_lines[:7]):
            pyxel.text(15, 60 + i * 10, line, 5)
        
        pyxel.text(15, 145, "Answer:", 11)
        answer_lines = wrap_text(input_state_answer.text, 70)
        for i, line in enumerate(answer_lines[:7]):
            pyxel.text(15, 160 + i * 10, line, 7)
        
        # Draw cursor for answer
        if pyxel.frame_count % 30 < 15:
            cursor_x = 15
            cursor_y = 160
            
            # Find cursor position based on wrapped text
            char_count = 0
            for i, line in enumerate(answer_lines):
                if i >= 7:  # Don't check beyond visible lines
                    break
                if char_count + len(line) >= input_state_answer.cursor_pos:
                    # Cursor is in this line
                    line_pos = input_state_answer.cursor_pos - char_count
                    cursor_x = 15 + line_pos * 4  # Assuming each char is 4 pixels wide
                    cursor_y = 160 + i * 10
                    break
                char_count += len(line)
            
            pyxel.text(cursor_x, cursor_y, "_", 7)
    
    pyxel.text(20, 240, "TAB to switch fields | ENTER to save", 13)
    
    # Draw back button
    back_button_area = draw_back_button(320, 240)
    pyxel.text(320, 260, "ESC: Exit", 8)
    
    # Draw instructions for cursor navigation
    pyxel.text(200, 240, "Arrow keys: Navigate cursor", 5)
    
    return back_button_area

def draw_edit_card(current_set_name, input_text, input_field, new_card):
    """Draw the edit card screen with improved text display."""
    pyxel.text(20, 20, f"Edit Card in: {current_set_name}", 7)
    
    # Draw card boxes - made larger
    draw_box(10, 40, 390, 130)  # Question box
    draw_box(10, 140, 390, 230)  # Answer box
    
    if input_field == "question":
        pyxel.text(15, 45, "Question:", 11)
        
        # Display the question text with improved wrapping
        question_lines = wrap_text(input_text, 70)
        for i, line in enumerate(question_lines[:7]):  # Increased visible lines
            pyxel.text(15, 60 + i * 10, line, 7)  # Reduced spacing
        
        # Only show cursor at the end of the last line
        if question_lines:
            last_line = question_lines[-1]
            cursor_x = 15 + len(last_line) * 4  # Approximate character width
            cursor_y = 60 + (len(question_lines) - 1) * 10
            
            # Make sure cursor is visible within the box
            if cursor_x > 380:
                cursor_x = 380
            
            if pyxel.frame_count % 30 < 15:
                pyxel.text(cursor_x, cursor_y, "_", 7)
        else:
            if pyxel.frame_count % 30 < 15:
                pyxel.text(15, 60, "_", 7)
        
        pyxel.text(15, 145, "Answer:", 8)
        answer_lines = wrap_text(new_card["answer"], 70)
        for i, line in enumerate(answer_lines[:7]):
            pyxel.text(15, 160 + i * 10, line, 5)
    else:  # answer field
        pyxel.text(15, 45, "Question:", 8)
        question_lines = wrap_text(new_card["question"], 70)
        for i, line in enumerate(question_lines[:7]):
            pyxel.text(15, 60 + i * 10, line, 5)
        
        pyxel.text(15, 145, "Answer:", 11)
        answer_lines = wrap_text(input_text, 70)
        for i, line in enumerate(answer_lines[:7]):
            pyxel.text(15, 160 + i * 10, line, 7)
        
        # Only show cursor at the end of the last line
        if answer_lines:
            last_line = answer_lines[-1]
            cursor_x = 15 + len(last_line) * 4  # Approximate character width
            cursor_y = 160 + (len(answer_lines) - 1) * 10
            
            # Make sure cursor is visible within the box
            if cursor_x > 380:
                cursor_x = 380
            
            if pyxel.frame_count % 30 < 15:
                pyxel.text(cursor_x, cursor_y, "_", 7)
        else:
            if pyxel.frame_count % 30 < 15:
                pyxel.text(15, 160, "_", 7)
    
    pyxel.text(20, 240, "TAB to switch fields | ENTER to save", 13)
    
    # Draw back button
    back_button_area = draw_back_button(320, 240)
    pyxel.text(320, 260, "ESC: Exit", 8)
    
    return back_button_area

def draw_edit_card_with_cursor(current_set_name, input_field, input_state_question, input_state_answer):
    """Draw the edit card screen with cursor support."""
    pyxel.text(20, 20, f"Edit Card in: {current_set_name}", 7)
    
    # Draw card boxes - made larger
    draw_box(10, 40, 390, 130)  # Question box
    draw_box(10, 140, 390, 230)  # Answer box
    
    if input_field == "question":
        pyxel.text(15, 45, "Question:", 11)
        
        # Display the question text with improved wrapping
        question_lines = wrap_text(input_state_question.text, 70)
        for i, line in enumerate(question_lines[:7]):  # Increased visible lines
            pyxel.text(15, 60 + i * 10, line, 7)  # Reduced spacing
        
        # Draw cursor for question
        if pyxel.frame_count % 30 < 15:
            cursor_x = 15
            cursor_y = 60
            
            # Find cursor position based on wrapped text
            char_count = 0
            for i, line in enumerate(question_lines):
                if i >= 7:  # Don't check beyond visible lines
                    break
                if char_count + len(line) >= input_state_question.cursor_pos:
                    # Cursor is in this line
                    line_pos = input_state_question.cursor_pos - char_count
                    cursor_x = 15 + line_pos * 4  # Assuming each char is 4 pixels wide
                    cursor_y = 60 + i * 10
                    break
                char_count += len(line)
            
            pyxel.text(cursor_x, cursor_y, "_", 7)
        
        pyxel.text(15, 145, "Answer:", 8)
        answer_lines = wrap_text(input_state_answer.text, 70)
        for i, line in enumerate(answer_lines[:7]):
            pyxel.text(15, 160 + i * 10, line, 5)
    else:  # answer field
        pyxel.text(15, 45, "Question:", 8)
        question_lines = wrap_text(input_state_question.text, 70)
        for i, line in enumerate(question_lines[:7]):
            pyxel.text(15, 60 + i * 10, line, 5)
        
        pyxel.text(15, 145, "Answer:", 11)
        answer_lines = wrap_text(input_state_answer.text, 70)
        for i, line in enumerate(answer_lines[:7]):
            pyxel.text(15, 160 + i * 10, line, 7)
        
        # Draw cursor for answer
        if pyxel.frame_count % 30 < 15:
            cursor_x = 15
            cursor_y = 160
            
            # Find cursor position based on wrapped text
            char_count = 0
            for i, line in enumerate(answer_lines):
                if i >= 7:  # Don't check beyond visible lines
                    break
                if char_count + len(line) >= input_state_answer.cursor_pos:
                    # Cursor is in this line
                    line_pos = input_state_answer.cursor_pos - char_count
                    cursor_x = 15 + line_pos * 4  # Assuming each char is 4 pixels wide
                    cursor_y = 160 + i * 10
                    break
                char_count += len(line)
            
            pyxel.text(cursor_x, cursor_y, "_", 7)
    
    pyxel.text(20, 240, "TAB to switch fields | ENTER to save", 13)
    
    # Draw back button
    back_button_area = draw_back_button(320, 240)
    pyxel.text(320, 260, "ESC: Exit", 8)
    
    # Draw instructions for cursor navigation
    pyxel.text(200, 240, "Arrow keys: Navigate cursor", 5)
    
    return back_button_area

def draw_import_cards(current_set_name, input_text):
    """Draw the import cards screen."""
    pyxel.text(20, 20, f"Import Cards to: {current_set_name}", 7)
    pyxel.text(20, 40, "Enter file path:", 11)
    pyxel.text(20, 60, input_text, 7)
    pyxel.text(20, 80, "_" if pyxel.frame_count % 30 < 15 else "", 7)
    pyxel.text(20, 120, "Format: Q: Question text A: Answer text", 13)
    pyxel.text(20, 140, "Cards separated by blank lines", 13)
    pyxel.text(20, 180, "Press ENTER to import", 13)
    
    # Draw back button
    back_button_area = draw_back_button(320, 220)
    pyxel.text(320, 240, "ESC: Exit", 8)
    
    return back_button_area

def draw_import_cards_with_cursor(current_set_name, input_state):
    """Draw the import cards screen with cursor support."""
    pyxel.text(20, 20, f"Import Cards to: {current_set_name}", 7)
    pyxel.text(20, 40, "Enter file path:", 11)
    
    # Draw text box
    draw_box(10, 50, 390, 90)
    
    # Get text with cursor
    text_lines = wrap_text(input_state.text, 70)
    
    # Draw text lines
    for i, line in enumerate(text_lines[:3]):  # Limit to 3 lines
        pyxel.text(15, 60 + i * 10, line, 7)
    
    # Draw cursor
    if pyxel.frame_count % 30 < 15:
        cursor_x = 15
        cursor_y = 60
        
        # Find cursor position based on wrapped text
        char_count = 0
        for i, line in enumerate(text_lines):
            if char_count + len(line) >= input_state.cursor_pos:
                # Cursor is in this line
                line_pos = input_state.cursor_pos - char_count
                cursor_x = 15 + line_pos * 4  # Assuming each char is 4 pixels wide
                cursor_y = 60 + i * 10
                break
            char_count += len(line)
        
        pyxel.text(cursor_x, cursor_y, "_", 7)
    
    pyxel.text(20, 120, "Format: Q: Question text A: Answer text", 13)
    pyxel.text(20, 140, "Cards separated by blank lines", 13)
    pyxel.text(20, 180, "Press ENTER to import", 13)
    
    # Draw back button
    back_button_area = draw_back_button(320, 220)
    pyxel.text(320, 240, "ESC: Exit", 8)
    
    # Draw instructions for cursor navigation
    pyxel.text(20, 160, "Arrow keys: Move cursor | Home/End: Start/End of text", 5)
    
    return back_button_area