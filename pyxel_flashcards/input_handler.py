import pyxel

def is_mouse_in_area(x1, y1, x2, y2):
    """Check if the mouse is in a specific area."""
    return x1 <= pyxel.mouse_x <= x2 and y1 <= pyxel.mouse_y <= y2

class TextInputState:
    """Class to track text input state including cursor position."""
    def __init__(self, text=""):
        self.text = text
        self.cursor_pos = len(text)  # Start cursor at end of text

    def move_cursor_left(self):
        """Move cursor left one character."""
        if self.cursor_pos > 0:
            self.cursor_pos -= 1

    def move_cursor_right(self):
        """Move cursor right one character."""
        if self.cursor_pos < len(self.text):
            self.cursor_pos += 1
    
    def move_cursor_to_start(self):
        """Move cursor to start of text."""
        self.cursor_pos = 0
    
    def move_cursor_to_end(self):
        """Move cursor to end of text."""
        self.cursor_pos = len(self.text)
    
    def move_cursor_word_left(self):
        """Move cursor to beginning of previous word."""
        if self.cursor_pos > 0:
            # Skip any spaces immediately to the left
            pos = self.cursor_pos - 1
            while pos > 0 and self.text[pos] == ' ':
                pos -= 1
            
            # Find beginning of the word
            while pos > 0 and self.text[pos - 1] != ' ':
                pos -= 1
                
            self.cursor_pos = pos
    
    def move_cursor_word_right(self):
        """Move cursor to beginning of next word."""
        if self.cursor_pos < len(self.text):
            # Skip current word
            pos = self.cursor_pos
            while pos < len(self.text) and self.text[pos] != ' ':
                pos += 1
                
            # Skip spaces
            while pos < len(self.text) and self.text[pos] == ' ':
                pos += 1
                
            self.cursor_pos = pos
    
    def insert_char(self, char):
        """Insert character at cursor position."""
        self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
        self.cursor_pos += 1
    
    def delete_char_before(self):
        """Delete character before cursor (backspace)."""
        if self.cursor_pos > 0:
            self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
            self.cursor_pos -= 1
    
    def delete_char_after(self):
        """Delete character after cursor (delete key)."""
        if self.cursor_pos < len(self.text):
            self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
    
    def estimate_cursor_x_position(self, base_x, char_width=4):
        """Estimate the x-coordinate of the cursor based on text width."""
        return base_x + self.cursor_pos * char_width
    
    def get_text_with_cursor(self, cursor_char="_"):
        """Get text with cursor character inserted (for display purposes only)."""
        return self.text[:self.cursor_pos] + cursor_char + self.text[self.cursor_pos:]
    
    def set_cursor_position_by_click(self, click_x, base_x, char_width=4):
        """Set cursor position based on mouse click position."""
        if click_x < base_x:
            # If clicked to the left of the text
            self.cursor_pos = 0
        else:
            # Calculate the character position based on click position
            char_pos = int((click_x - base_x) / char_width)
            self.cursor_pos = min(char_pos, len(self.text))

def handle_text_input_with_cursor(input_state, base_x, base_y, line_height, max_chars_per_line):
    """Handle text input with cursor navigation.
    
    Args:
        input_state: TextInputState object tracking the input text and cursor
        base_x: Base x-coordinate of the text display
        base_y: Base y-coordinate of the text display
        line_height: Height of each line of text
        max_chars_per_line: Maximum characters per line for wrapping
        
    Returns:
        Updated TextInputState object
    """
    # Handle mouse clicks to set cursor position
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        # Check if click is in the text area (approximate bounds)
        lines = wrap_text(input_state.text, max_chars_per_line)
        
        # Calculate the text area bounds
        area_height = len(lines) * line_height
        
        if is_mouse_in_area(base_x, base_y, base_x + max_chars_per_line * 4, base_y + area_height):
            # Determine which line was clicked
            line_idx = min((pyxel.mouse_y - base_y) // line_height, len(lines) - 1)
            
            # Handle cursor positioning within the line
            if line_idx < len(lines) - 1:
                # For all lines except the last, cursor can be within the line's length
                char_position = input_state.text.find(lines[line_idx])
                relative_position = min(int((pyxel.mouse_x - base_x) / 4), len(lines[line_idx]))
                input_state.cursor_pos = char_position + relative_position
            else:
                # For the last line, we can just use the standard click positioning
                char_position = input_state.text.find(lines[line_idx])
                relative_position = min(int((pyxel.mouse_x - base_x) / 4), len(lines[line_idx]))
                input_state.cursor_pos = char_position + relative_position
    
    # Handle keyboard input for cursor movement
    if pyxel.btnp(pyxel.KEY_LEFT):
        input_state.move_cursor_left()
    
    if pyxel.btnp(pyxel.KEY_RIGHT):
        input_state.move_cursor_right()
    
    if pyxel.btnp(pyxel.KEY_HOME) or (pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_A)):
        input_state.move_cursor_to_start()
    
    if pyxel.btnp(pyxel.KEY_END) or (pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_E)):
        input_state.move_cursor_to_end()
    
    # Ctrl+Left/Right for word navigation
    if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_LEFT):
        input_state.move_cursor_word_left()
    
    if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btnp(pyxel.KEY_RIGHT):
        input_state.move_cursor_word_right()
    
    # Handle backspace and delete
    if pyxel.btnp(pyxel.KEY_BACKSPACE):
        input_state.delete_char_before()
    
    if pyxel.btnp(pyxel.KEY_DELETE):
        input_state.delete_char_after()
    
    # Process printable characters
    # Alphabet keys (A-Z)
    for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
        if pyxel.btnp(key):
            char = chr(key - pyxel.KEY_A + ord('a'))
            if pyxel.btn(pyxel.KEY_SHIFT):
                char = char.upper()
            input_state.insert_char(char)
    
    # Number keys (0-9)
    for key in range(pyxel.KEY_0, pyxel.KEY_9 + 1):
        if pyxel.btnp(key):
            num_char = chr(key - pyxel.KEY_0 + ord('0'))
            if pyxel.btn(pyxel.KEY_SHIFT):
                shift_chars = {
                    '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
                    '6': '^', '7': '&', '8': '*', '9': '(', '0': ')'
                }
                input_state.insert_char(shift_chars.get(num_char, num_char))
            else:
                input_state.insert_char(num_char)
    
    # Space key
    if pyxel.btnp(pyxel.KEY_SPACE):
        input_state.insert_char(" ")
    
    # Period, comma
    if pyxel.btnp(pyxel.KEY_PERIOD):
        input_state.insert_char(".")
    if pyxel.btnp(pyxel.KEY_COMMA):
        input_state.insert_char(",")
    
    # Slash
    if pyxel.btnp(pyxel.KEY_SLASH):
        if pyxel.btn(pyxel.KEY_SHIFT):
            input_state.insert_char("?")
        else:
            input_state.insert_char("/")
    
    # Semicolon
    if pyxel.btnp(pyxel.KEY_SEMICOLON):
        if pyxel.btn(pyxel.KEY_SHIFT):
            input_state.insert_char(":")
        else:
            input_state.insert_char(";")
    
    # Minus/underscore
    if pyxel.btnp(pyxel.KEY_MINUS):
        if pyxel.btn(pyxel.KEY_SHIFT):
            input_state.insert_char("_")
        else:
            input_state.insert_char("-")
    
    # Equals/plus
    if pyxel.btnp(pyxel.KEY_EQUALS):
        if pyxel.btn(pyxel.KEY_SHIFT):
            input_state.insert_char("+")
        else:
            input_state.insert_char("=")
    
    # Try to handle other special keys safely
    try:
        # Quotes/apostrophe
        if hasattr(pyxel, 'KEY_QUOTE') and pyxel.btnp(pyxel.KEY_QUOTE):
            if pyxel.btn(pyxel.KEY_SHIFT):
                input_state.insert_char('"')
            else:
                input_state.insert_char("'")
    except:
        pass
        
    try:
        # Left bracket
        if hasattr(pyxel, 'KEY_LEFTBRACKET') and pyxel.btnp(pyxel.KEY_LEFTBRACKET):
            if pyxel.btn(pyxel.KEY_SHIFT):
                input_state.insert_char("{")
            else:
                input_state.insert_char("[")
    except:
        pass
        
    try:
        # Right bracket
        if hasattr(pyxel, 'KEY_RIGHTBRACKET') and pyxel.btnp(pyxel.KEY_RIGHTBRACKET):
            if pyxel.btn(pyxel.KEY_SHIFT):
                input_state.insert_char("}")
            else:
                input_state.insert_char("]")
    except:
        pass
        
    try:
        # Backslash
        if hasattr(pyxel, 'KEY_BACKSLASH') and pyxel.btnp(pyxel.KEY_BACKSLASH):
            if pyxel.btn(pyxel.KEY_SHIFT):
                input_state.insert_char("|")
            else:
                input_state.insert_char("\\")
    except:
        pass
        
    try:
        # Grave/tilde
        if hasattr(pyxel, 'KEY_GRAVE') and pyxel.btnp(pyxel.KEY_GRAVE):
            if pyxel.btn(pyxel.KEY_SHIFT):
                input_state.insert_char("~")
            else:
                input_state.insert_char("`")
    except:
        pass
    
    return input_state

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