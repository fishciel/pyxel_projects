import pyxel

def draw_back_button(x, y):
    """Draw a clickable 'Back' button at the specified position."""
    width = 60
    height = 15
    
    # Draw button background
    for iy in range(y, y + height):
        pyxel.line(x, iy, x + width - 1, iy, 1)  # Dark blue background
    
    # Draw button border
    pyxel.rectb(x, y, width, height, 5)  # Purple border
    
    # Draw button text
    pyxel.text(x + 15, y + 5, "BACK", 7)
    
    return (x, y, x + width, y + height)  # Return button area for click detection

def is_back_button_clicked(button_area):
    """Check if the back button was clicked."""
    x1, y1, x2, y2 = button_area
    return (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 
            x1 <= pyxel.mouse_x <= x2 and 
            y1 <= pyxel.mouse_y <= y2)