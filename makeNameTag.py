from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import pandas as pd

from function import fit_text_to_width, fit_text_to_width_height_2

def draw_business_card(c, x, y, name, furigana, title, bg_image):
    # 背景画像を描く。A4の8分割よりも小さいことを想定している（横長）
    c.drawImage(bg_image, x, y, width=card_width, height=card_height)

    # テキストの色を設定
    c.setFillColor(colors.black)

    # c.rect(x + 90, y + card_height - 60,190,40)
    # 名刺の背景によって文字のサイズを変える。
    fit_text_to_width_height_2(c, title, x + 90, y + card_height - 60,190,40, "ipaexm", 15)
    font_size = fit_text_to_width(c, name, x + 110, y + card_height - 130, 170, "ipaexm", 40)
    fit_text_to_width(c, furigana, x + 120, y + card_height - 130 + font_size, 130, "ipaexm", 15)
    


def generate_business_cards(output_pdf, data, bg_image_path):
    # A4サイズ
    width, height = A4
    global card_width, card_height
    card_width = width / 2
    card_height = height / 4

    # キャンバスを作成
    c = canvas.Canvas(output_pdf, pagesize=A4)
    # フォントを読み込む
    pdfmetrics.registerFont(TTFont('ipaexm', 'ipaexm.ttf'))
    # 背景画像を読み込む
    bg_image = ImageReader(bg_image_path)
    # 1ページ8枚のカードを作成
    for i, row in data.iterrows():
        title = row['title']
        name = row['name']
        furigana = row['furigana']
        x = (i % 2) * card_width
        y = height - ((i % 8 )// 2 + 1) * card_height
        draw_business_card(c, x, y, name, furigana, title, bg_image)

        # 8枚ごとに新しいページを開始
        if (i + 1) % 8 == 0 and i != len(data) - 1:
            c.showPage()

    # PDFを保存
    c.save()

data = pd.read_csv('./csv/name_tag.csv',header=None)
data.columns = ['title', 'name', 'furigana']
generate_business_cards("./pdf/name_tag.pdf", data, "./png/name_tag.png")
