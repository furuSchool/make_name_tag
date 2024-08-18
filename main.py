from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import pandas as pd

# 文字列の幅を先に指定して、フォントサイズを変えるための関数。名前のサイズ調整に利用できる。
def fit_text_to_width_height(c, text, x, y, max_width, font_name, max_font_size):
    font_size = max_font_size
    c.setFont(font_name, font_size)

    text_width = c.stringWidth(text, font_name, font_size)

    while text_width > max_width and font_size > 0:
        font_size -= 0.1
        c.setFont(font_name, font_size)
        text_width = c.stringWidth(text, font_name, font_size)
    
    c.drawString(x, y, text)


def draw_card(c, x, y, name, furigana, title, bg_image):
    # 背景画像を描く。A4の8分割よりも小さいことを想定している（横長）
    c.drawImage(bg_image, x, y, width=card_width, height=card_height)

    # テキストの色を設定
    c.setFillColor(colors.black)

    # 肩書きの分解（長い人向け）
    title1 = title[0:15]
    title2 = title[15:30]

    # 名刺の背景によって文字のサイズを変える。
    c.setFont("ipaexm", 12)
    c.drawString(x + 90, y + card_height - 40, title1)
    c.drawString(x + 100, y + card_height - 60, title2)
    # fit_text_to_width_height(c, title, x + 110, y + card_height - 40, 170, "ipaexm", 15)
    fit_text_to_width_height(c, furigana, x + 120, y + card_height - 90, 150, "ipaexm", 15)
    fit_text_to_width_height(c, name, x + 110, y + card_height - 130, 170, "ipaexm", 40)


def generate_business_cards(output_pdf, data, bg_image_path):
    # A4サイズ
    width, height = A4
    global card_width, card_height
    card_width = width / 2
    card_height = height / 4

    # キャンバスを作成
    c = canvas.Canvas(output_pdf, pagesize=A4)

    pdfmetrics.registerFont(TTFont('ipaexm', 'ipaexm.ttf'))

    # 背景画像を読み込む
    bg_image = ImageReader(bg_image_path)

    for i, row in data.iterrows():
        title = row['title']
        name = row['name']
        furigana = row['furigana']
        x = (i % 2) * card_width
        y = height - ((i % 8 )// 2 + 1) * card_height
        draw_card(c, x, y, name, furigana, title, bg_image)

        # 8枚ごとに新しいページを開始
        if (i + 1) % 8 == 0 and i != len(data) - 1:
            c.showPage()

    # PDFを保存
    c.save()

data = pd.read_csv('data.csv')
data.columns = ['title', 'name', 'furigana']

generate_business_cards("name_tag.pdf", data, "data.png")
