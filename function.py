import os
import re
from fontTools.ttLib import TTCollection


# 文字列の幅を先に指定して、フォントサイズを変えるための関数。名前のサイズ調整に利用できる。
def fit_text_to_width(c,
                      text,
                      x,
                      y,
                      max_width,
                      font_name,
                      max_font_size,
                      alignment='left'):
    font_size = max_font_size
    c.setFont(font_name, font_size)

    text_width = c.stringWidth(text, font_name, font_size)

    while text_width > max_width and font_size > 0:
        font_size -= 0.1
        c.setFont(font_name, font_size)
        text_width = c.stringWidth(text, font_name, font_size)

    if alignment == 'right':
        c.drawString(x + max_width - c.stringWidth(text, font_name, font_size),
                     y, text)
    elif alignment == 'center':
        c.drawString(
            x + (max_width - c.stringWidth(text, font_name, font_size)) / 2, y,
            text)
    else:
        c.drawString(x, y, text)
    return font_size


def fit_text_to_height(c, text, x, y, max_height, font_name, max_font_size):
    font_size = max_font_size
    c.setFont(font_name, font_size)

    text_height = font_size * len(text)

    while text_height > max_height and font_size > 0:
        font_size -= 0.1
        c.setFont(font_name, font_size)
        text_height = font_size * len(text)

    current_y = y + max_height

    for char in text:
        c.drawString(x, current_y - font_size, char)
        current_y -= font_size  # 次の文字の位置を下にずらす
    return font_size


# 長方形の中に、文章を適切に配置してくれる関数。左揃え、中揃え
def fit_text_to_width_height(c, text, x, y, max_width, max_height, font_name,
                             max_font_size):
    font_size = max_font_size
    c.setFont(font_name, font_size)

    text_list = text.split('\n')

    line_number = len(text_list)
    line_number_list = [1] * len(text_list)

    for i, one_sentense in enumerate(text_list):
        while (1):
            while (line_number * font_size > max_height) and font_size > 0:
                font_size -= 0.1
            if c.stringWidth(
                    one_sentense, font_name,
                    font_size) > (line_number_list[i] + 1) * max_width:
                line_number_list[i] += 1
                line_number += 1
            else:
                break

    for i, one_sentense in enumerate(text_list):
        if (line_number_list[i] + 1) * max_width > c.stringWidth(
                one_sentense, font_name,
                font_size) > line_number_list[i] * max_width:
            font_size = min(
                font_size /
                (c.stringWidth(one_sentense, font_name, font_size) /
                 (line_number_list[i] * max_width)), font_size)
            line_number_list[i] += 1
            line_number += 1
        while (line_number * font_size > max_height) and font_size > 0:
            font_size -= 0.1

    lines = []

    # Create lines of text that fit within the max_width
    for i, one_sentense in enumerate(text_list):
        current_line = ""
        for word in one_sentense:
            if c.stringWidth(current_line + word, font_name,
                             font_size) <= max_width:
                current_line += word
            #  文頭に不適切な記号が文頭にこないように
            elif word in ['、', '。', ',', '.', ';', '?', '!', ':', ' ']:
                current_line += word
            else:
                lines.append(current_line.strip())
                current_line = word
        # Add the last line
        if current_line and re.search(r'[a-zA-Zぁ-んァ-ン一-龥0-9]', current_line):
            lines.append(current_line.strip())

    # Calculate the total height of the text block
    text_height = len(lines) * font_size

    # Adjust the starting y position to center the text vertically
    start_y = y + (max_height - text_height) / 2

    # Draw the lines of text
    c.setFont(font_name, font_size)
    for i, line in enumerate(lines):
        c.drawString(x, start_y + (len(lines) - i - 1) * font_size, line)

    return font_size


# 長方形の中に、文章を適切に配置してくれる関数。左揃え、中揃え
def fit_text_to_width_height_2(c, text, x, y, max_width, max_height, font_name,
                               max_font_size):
    font_size = max_font_size
    c.setFont(font_name, font_size)

    text_list = text.split('\n')

    line_number = len(text_list)
    line_number_list = [1] * len(text_list)
    for i, one_sentense in enumerate(text_list):
        while (1):
            while (line_number * font_size > max_height) and font_size > 0:
                font_size -= 0.1
            if c.stringWidth(
                    one_sentense, font_name,
                    font_size) > (line_number_list[i] + 1) * max_width:
                line_number_list[i] += 1
                line_number += 1
            else:
                break

    for i, one_sentense in enumerate(text_list):
        if (line_number_list[i] + 1) * max_width > c.stringWidth(
                one_sentense, font_name,
                font_size) > line_number_list[i] * max_width:
            line_number_list[i] += 1
            line_number += 1
            font_size = min(
                font_size /
                (c.stringWidth(one_sentense, font_name, font_size) /
                 (line_number_list[i] * max_width)), font_size)
        while (line_number * font_size > max_height) and font_size > 0:
            font_size -= 0.1

    lines = []

    # Create lines of text that fit within the max_width
    for i, one_sentense in enumerate(text_list):
        current_line = ""
        for word in one_sentense:
            if c.stringWidth(current_line + word, font_name,
                             font_size) <= max_width:
                current_line += word
            #  文頭に不適切な記号が文頭にこないように
            elif word in ['、', '。', ',', '.', ';', '?', '!', ':', ' ']:
                current_line += word
            else:
                lines.append(current_line.strip())
                current_line = word
        # Add the last line
        if current_line and re.search(r'[a-zA-Zぁ-んァ-ン一-龥0-9]', current_line):
            lines.append(current_line.strip())

    # Calculate the total height of the text block
    text_height = len(lines) * font_size

    # Adjust the starting y position to center the text vertically
    start_y = y + (max_height - text_height) / 2

    # Draw the lines of text
    c.setFont(font_name, font_size)
    for i, line in enumerate(lines):
        c.drawString(x, start_y + (len(lines) - i - 1) * font_size, line)


def fit_vertical_text_to_width_height(c, text, x, y, max_width, max_height,
                                      font_name, max_font_size):
    font_size = max_font_size
    c.setFont(font_name, font_size)

    text_list = text.split('\n')

    line_number = len(text_list)
    line_number_list = [1] * len(text_list)

    for i, one_sentense in enumerate(text_list):
        while (1):
            while (line_number * font_size > max_width) and font_size > 0:
                font_size -= 0.1
            if len(one_sentense) * font_size > (
                    line_number_list[i]) * max_height:
                line_number_list[i] += 1
                line_number += 1
            else:
                break

    for i, one_sentense in enumerate(text_list):
        if (line_number_list[i] + 1) * max_height > len(
                one_sentense) * font_size > line_number_list[i] * max_height:
            font_size = min(
                font_size / (len(one_sentense) * font_size /
                             (line_number_list[i] * max_height)), font_size)
            line_number_list[i] += 1
            line_number += 1
        while (line_number * font_size > max_width) and font_size > 0:
            font_size -= 0.1

    lines = []

    for i, one_sentense in enumerate(text_list):
        current_line = ""
        for word in one_sentense:
            if len(current_line + word) * font_size <= max_height:
                current_line += word
            #  文頭に不適切な記号が文頭にこないように
            elif word in ['、', '。', ',', '.', ';', '?', '!', ':', ' ']:
                current_line += word
            else:
                lines.append(current_line.strip())
                current_line = word
        # Add the last line
        if current_line and re.search(r'[a-zA-Zぁ-んァ-ン一-龥0-9]', current_line):
            lines.append(current_line.strip())

    current_x = x + max_width
    current_y = y + max_height

    # 文字がぎゅうぎゅうにならないよう配慮
    c.setFont(font_name, font_size - 5)
    for line in lines:
        for char in line:
            char_width = c.stringWidth(char, font_name, font_size)
            c.drawString(current_x - char_width, current_y - font_size, char)
            current_y -= font_size  # 次の文字の位置を下にずらす
        current_x -= char_width
        current_y = y + max_height


def ttc_to_ttf(ttc_file_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ttc = TTCollection(ttc_file_path)

    # 各フォントをTTF形式で保存
    for i, font in enumerate(ttc.fonts):
        font_name = font['name'].getDebugName(1) or f"font_{i}"
        ttf_file = os.path.join(output_dir, f"{font_name}.ttf")
        font.save(ttf_file)
        print(f"Saved {ttf_file}")
