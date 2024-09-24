# 文字列の幅を先に指定して、フォントサイズを変えるための関数。名前のサイズ調整に利用できる。
def fit_text_to_width(c, text, x, y, max_width, font_name, max_font_size):
    font_size = max_font_size
    c.setFont(font_name, font_size)

    text_width = c.stringWidth(text, font_name, font_size)

    while text_width > max_width and font_size > 0:
        font_size -= 0.1
        c.setFont(font_name, font_size)
        text_width = c.stringWidth(text, font_name, font_size)
    
    c.drawString(x, y, text)

# 長方形の中に、文章を適切に配置してくれる関数。左揃え、中揃え
def fit_text_to_width_height(c, text, x, y, max_width, max_height, font_name, max_font_size):
    font_size = max_font_size
    c.setFont(font_name, font_size)

    line_number = 1

    while(1):
        while (line_number * font_size > max_height) and font_size > 0:
            font_size -= 0.1
        if c.stringWidth(text, font_name, font_size) > (line_number+1) * max_width:
            line_number += 1
        else:
            break

    if (line_number + 1) * max_width > c.stringWidth(text, font_name, font_size) >line_number * max_width:
        font_size = font_size / (c.stringWidth(text, font_name, font_size)/(line_number * max_width))
        line_number += 1
    while (line_number * font_size > max_height) and font_size > 0:
        font_size -= 0.1

    words = list(text)
    lines = []
    current_line = ""
    
    # Create lines of text that fit within the max_width
    for word in words:
        if c.stringWidth(current_line + word, font_name, font_size) <= max_width:
            current_line += word
        else:
            lines.append(current_line.strip())
            current_line = word
    
    # Add the last line
    if current_line:
        lines.append(current_line.strip())
    
    # Calculate the total height of the text block
    text_height = len(lines) * font_size
    
    # Adjust the starting y position to center the text vertically
    start_y = y + (max_height - text_height) / 2
    
    # Draw the lines of text
    c.setFont(font_name, font_size)
    for i, line in enumerate(lines):
        c.drawString(x, start_y + (len(lines) - i - 1) * font_size, line)
